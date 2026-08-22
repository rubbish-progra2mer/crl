import re
import copy
from typing import List, Dict, Optional
from tqdm import tqdm
from flashrag.utils import get_retriever, get_generator
from flashrag.pipeline import BasicPipeline, ReasoningPipeline
from flashrag.prompt import PromptTemplate
from flashrag.dataset import Dataset
from flashrag.utils.utils import extract_between,extract_between_all


class SearchO1Pipeline(ReasoningPipeline):
    system_prompt = ""
    user_prompt = (
        "You are a reasoning assistant with the ability to perform web searches to help "
        "you answer the user's question accurately. You have special tools:\n\n"
        "- To perform a search: write <|begin_search_query|> your query here <|end_search_query|>.\n"
        "Then, the system will search and analyze relevant web pages, then provide you with helpful information in the format <|begin_search_result|> ...search results... <|end_search_result|>.\n\n"
        "You can repeat the search process multiple times if necessary. The maximum number of search attempts is limited to 5.\n\n"
        "Once you have all the information you need, continue your reasoning.\n\n"
        "Example:\n"
        "Question: \"Alice David is the voice of Lara Croft in a video game developed by which company?\"\n"
        "Assistant thinking steps:\n"
        "- I need to find out who voices Lara Croft in the video game.\n"
        "- Then, I need to determine which company developed that video game.\n\n"
        "Assistant:\n"
        "<|begin_search_query|>Alice David Lara Croft voice<|end_search_query|>\n\n"
        "(System returns processed information from relevant web pages)\n\n"
        "Assistant thinks: The search results indicate that Alice David is the voice of Lara Croft in a specific video game. Now, I need to find out which company developed that game.\n\n"
        "Assistant:\n"
        "<|begin_search_query|>video game developed by Alice David Lara Croft<|end_search_query|>\n\n"
        "(System returns processed information from relevant web pages)\n\n"
        "Assistant continues reasoning with the new information...\n\n"
        "Remember:\n"
        "- Use <|begin_search_query|> to request a web search and end with <|end_search_query|>.\n"
        "- When done searching, continue your reasoning.\n\n"
        'Please answer the following question. You should think step by step to solve it.\n\n'
        'Provide your final answer in the format \\boxed{{YOUR_ANSWER}}.\n\n'
        'Question:\n{question}\n\n'
    )

    def __init__(self, config, 
                 prompt_template=None, 
                 max_retrieval_num=5, 
                 begin_search_query="<|begin_search_query|>",
                 end_search_query="<|end_search_query|>",
                 begin_search_result="<|begin_search_result|>",
                 end_search_result="<|end_search_result|>",
                 begin_of_answer_token="\\boxed{",
                 end_of_answer_token="}",
                 retriever=None, 
                 generator=None,
                 reason_in_doc_prompt=None):
        if prompt_template is None:
            prompt_template = PromptTemplate(
                config=config,
                system_prompt=self.system_prompt,
                user_prompt=self.user_prompt
            )
        super().__init__(config, prompt_template)

        if generator is None:
            self.generator = get_generator(config)
        else:
            self.generator = generator
        if retriever is None:
            self.retriever = get_retriever(config)
        else:
            self.retriever = retriever

        self.max_retrieval_num = max_retrieval_num

        self.begin_search_query = begin_search_query
        self.end_search_query = end_search_query
        self.begin_search_result = begin_search_result
        self.end_search_result = end_search_result
        self.begin_of_answer_token = begin_of_answer_token
        self.end_of_answer_token = end_of_answer_token

        self.stop_tokens = [self.end_search_query, "<|im_end|>", "<|endoftext|>"]

        self.is_openai = config['framework'] == 'openai'

        if reason_in_doc_prompt is None:
            self.reason_in_doc_prompt = (
                "**Task Instruction:**\n\n"
                "You are tasked with reading and analyzing web pages based on the following inputs: **Previous Reasoning Steps**, **Current Search Query**, and **Searched Web Pages**. Your objective is to extract relevant and helpful information for **Current Search Query** from the **Searched Web Pages** and seamlessly integrate this information into the **Previous Reasoning Steps** to continue reasoning for the original question.\n\n"
                "**Guidelines:**\n\n"
                "1. **Analyze the Searched Web Pages:**\n"
                "- Carefully review the content of each searched web page.\n"
                "- Identify factual information that is relevant to the **Current Search Query** and can aid in the reasoning process for the original question.\n\n"
                "2. **Extract Relevant Information:**\n"
                "- Select the information from the Searched Web Pages that directly contributes to advancing the **Previous Reasoning Steps**.\n"
                "- Ensure that the extracted information is accurate and relevant.\n\n"
                "3. **Output Format:**\n"
                "- **If the web pages provide helpful information for current search query:** Present the information beginning with `**Final Information**` as shown below.\n"
                "**Final Information**\n\n"
                "[Helpful information]\n\n"
                "- **If the web pages do not provide any helpful information for current search query:** Output the following text.\n\n"
                "**Final Information**\n\n"
                "No helpful information found.\n\n"
                "**Inputs:**\n"
                "- **Previous Reasoning Steps:**  \n"
                "{prev_reasoning}\n\n"
                "- **Current Search Query:**  \n"
                "{search_query}\n\n"
                "- **Searched Web Pages:**  \n"
                "{document}\n\n"
                'Now you should analyze each web page and find helpful information based on the current search query "{search_query}" and previous reasoning steps.'
            )
        else:
            self.reason_in_doc_prompt = reason_in_doc_prompt

    def _search_result_to_string(self, info: str):
        format_result_string = f'\n{self.begin_search_result}\n{info}\n{self.end_search_result}\n'
        return format_result_string

    def _get_summary_from_docs(self, prev_reasoning: str, search_query: str, retrieved_docs: List[Dict]):
        document = '\n\n'.join([doc['contents'] for doc in retrieved_docs])
        prompt = self.reason_in_doc_prompt.format(
            prev_reasoning=prev_reasoning,
            search_query=search_query,
            document=document
        )
        output = self.generator.generate([prompt], stop=["<|endoftext|>", "<|im_end|>"])[0].strip()
        # Extract the content after **Final Information**
        if "**Final Information**" in output:
            info = output.split("**Final Information**")[1].strip()
        else:
            info = "No helpful information found."
        return info

    def _append_to_prompt(self, item, content: str):
        if self.is_openai:
            if len(item.prompt) > 0 and isinstance(item.prompt[0], dict) and 'content' in item.prompt[0]:
                item.prompt[0]['content'] += content
            else:
                # Fallback if not in expected format
                item.prompt += content
        else:
            item.prompt += content

    def run(self, dataset, do_eval=True, pred_process_fun=None):
        prompts = [self.prompt_template.get_string(question=question) for question in dataset.question]
        dataset.update_output('prompt', prompts)
        dataset.update_output('finish_flag', [False] * len(prompts))
        dataset.update_output('retrieval_results', [{} for _ in range(len(prompts))])
        dataset.update_output('retrieved_times', [0] * len(prompts))
        dataset.update_output('searched_queries', [[] for _ in range(len(prompts))])

        # Logic of reasoning
        for current_step_idx in range(self.max_retrieval_num + 1):
            exist_items = [item for item in dataset if item.finish_flag == False]
            exist_prompts = [item.prompt for item in exist_items]
            
            print(f"Current step: {current_step_idx}, exist_items: {len(exist_items)}")

            if len(exist_items) == 0:
                print("All prompts are finished")
                break
            if current_step_idx == self.max_retrieval_num:
                print("Max retrieval number reached")
                for item in exist_items:
                    item.pred = 'No valid answer found'
                    item.finish_flag = True
                    item.finish_reason = 'Reach max retrieval number'
                break

            step_outputs = self.generator.generate(exist_prompts, stop=self.stop_tokens)
            step_query_list = []  # store generated queries for retrieval

            # parse each sample's step output
            for item, step_output in zip(exist_items, step_outputs):
                self._append_to_prompt(item, step_output.strip())
                if self.begin_of_answer_token in step_output:
                    # Extract the boxed answer
                    pred = extract_between(step_output, self.begin_of_answer_token, self.end_of_answer_token)
                    if pred is not None:
                        item.pred = pred
                        item.finish_flag = True
                        item.finish_reason = "Finished"
                    else:
                        item.pred = step_output.strip()
                        item.finish_flag = True
                        item.finish_reason = 'Answer pattern error'
                
                elif self.begin_search_query in step_output and (step_output.endswith(self.end_search_query) or step_output.endswith("<|endoftext|>")):
                    query = extract_between(step_output, self.begin_search_query, self.end_search_query)
                    if query is not None:
                        step_query_list.append({'item': item, 'query': query})
                    else:
                        item.pred = 'No valid answer found'
                        item.finish_flag = True
                        item.finish_reason = 'Query instruction error'

                else:
                    item.pred = step_output.strip()
                    item.finish_flag = True
                    item.finish_reason = 'Normal finish without answer pattern'
                
            # do retrieval and add search results to prompt
            if len(step_query_list) > 0:
                need_search_list = []
                for it in step_query_list:
                    item = it['item']
                    query = it['query'].strip()
                    if item.retrieved_times >= self.max_retrieval_num:
                        info = "The maximum search limit is exceeded. You are not allowed to search."
                        format_result_string = self._search_result_to_string(info)
                        self._append_to_prompt(item, format_result_string)
                        continue

                    if query in item.searched_queries:
                        info = "You have searched this query. Please refer to previous results."
                        format_result_string = self._search_result_to_string(info)
                        self._append_to_prompt(item, format_result_string)
                        continue

                    # Collect for batch processing
                    need_search_list.append(it)

                if len(need_search_list) > 0:
                    queries = [it['query'].strip() for it in need_search_list]
                    retrieved_docs_list = self.retriever.batch_search(queries)
                    prev_reasonings = [it['item'].prompt for it in need_search_list]

                    # Batch construct reason prompts
                    reason_prompts = []
                    for prev, query, retrieved_docs in zip(prev_reasonings, queries, retrieved_docs_list):
                        document = '\n\n'.join([doc['contents'] for doc in retrieved_docs])
                        prompt = self.reason_in_doc_prompt.format(
                            prev_reasoning=prev,
                            search_query=query,
                            document=document
                        )
                        if self.is_openai:
                            reason_prompts.append([{'role': 'user', 'content': prompt}])
                        else:
                            reason_prompts.append(prompt)
                    # Batch generate summaries
                    summaries = self.generator.generate(reason_prompts)

                    # Batch update items
                    for i, it in enumerate(need_search_list):
                        item = it['item']
                        query = queries[i]
                        retrieved_docs = retrieved_docs_list[i]
                        output = summaries[i].strip()
                        # Extract the content after **Final Information**
                        if "**Final Information**" in output:
                            info = output.split("**Final Information**")[1].strip()
                        else:
                            info = "No helpful information found."
                        format_result_string = self._search_result_to_string(info)
                        self._append_to_prompt(item, format_result_string)
                        item.searched_queries.append(query)
                        item.retrieval_results[item.retrieved_times] = {'query': query, 'docs': copy.copy(retrieved_docs), 'summary': info}
                        item.retrieved_times += 1

        # for item in dataset:
            # print(item.prompt)
            # item.prompt = item.prompt[0]["content"]
            # print(item.pred)
        dataset = self.evaluate(dataset, do_eval=do_eval, pred_process_fun=pred_process_fun)
        return dataset