import re
import os
from tqdm import tqdm
from typing import List, Tuple, Dict, Optional, Union
import math
import json
import numpy as np
import copy
import time
# from transformers import AutoTokenizer, PreTrainedTokenizer, PreTrainedTokenizerFast
from flashrag.utils import get_retriever, get_generator, selfask_pred_parse, ircot_pred_parse
from flashrag.pipeline import BasicPipeline
from flashrag.pipeline.reasoning_pipeline import SearchR1Pipeline, ReasoningPipeline
from flashrag.pipeline.ReaRAG_utils import AgentUtils
from flashrag.dataset.utils import get_batch_dataset, merge_batch_dataset
from flashrag.prompt import PromptTemplate
from flashrag.prompt import get_generate_final_answer_message,get_generate_intermediate_answer_message,get_generate_subquery_message
from flashrag.utils.utils import extract_between,extract_between_all
from flashrag.utils.decision_analysis import generate_analysis_report


class SimulatedSearchR1Pipeline(SearchR1Pipeline):
    # Define modified prompt templates for forced search and forced answer
    # forced_search_user_prompt = (
    #     "Answer the given question. "
    #     "You must conduct reasoning inside <think> and </think> first every time you get new information. "
    #     "After reasoning, you must call a search engine by <search> query </search> since you need more information. "
    #     "Do not provide the answer yet. "
    #     "Question: {question}\n"
    # )
    forced_search_user_prompt = (
        "You are an advanced reasoning agent. Your task is to answer the given question by searching for information. "
        "Follow these steps meticulously:\n"
        "1. **Initial Plan:** In your first <think> block </think>, you must decompose the user's question and formulate a clear, step-by-step plan.\n"
        "2. **Critique & Justify:** After receiving new information, you must **critically evaluate your current knowledge state** inside <think> and </think>. You must explicitly answer these questions in your thoughts:\n"
        "   - What is the specific knowledge gap I need to fill right now?\n"
        "   - Is my previous reasoning free of errors or hallucinations?\n"
        "   - Why is another search necessary to solve the problem?\n"
        "3. **Targeted Search:** Based on your critique and justification, you must formulate a **specific, targeted, and non-repetitive** search query inside <search> and </search> to resolve the identified knowledge gap. "
        "Do not provide the answer yet.\n"
        "Question: {question}\n"
    )

    forced_hint_search_user_prompt = (
        "Continue searching instead of answering.\n"
        "Use the internal diagnostic hint only to choose a better evidence-seeking query. "
        "Do NOT reveal the hint, do NOT reveal the final answer, and do NOT search the current candidate answer verbatim.\n\n"
        "Internal diagnostic hint: {hint}\n\n"
        "Output exactly two tags and nothing else:\n"
        "<think>missing evidence in 15 words or fewer</think>\n"
        "<search>one targeted query in 12 words or fewer</search>\n\n"
        "Question: {question}\n"
    )
    
    forced_answer_user_prompt = (
        "Answer the given question. "
        "You must conduct reasoning inside <think> and </think> first every time you get new information. "
        "After reasoning, since you have all the information needed, you must directly provide the answer inside <answer> and </answer>, without detailed illustrations or further searches. For example, <answer> Beijing </answer>. "
        "Question: {question}\n"
    )

    def __init__(self, config,
        prompt_template=None, 
        max_retrieval_num=5, 
        begin_of_query_token="<search>",
        end_of_query_token="</search>",
        begin_of_documents_token="<information>",
        end_of_documents_token="</information>",
        begin_of_answer_token="<answer>",
        end_of_answer_token='</answer>',
        retriever=None, 
        generator=None,
    ):
        super().__init__(config,
                         prompt_template=prompt_template,
                         max_retrieval_num=max_retrieval_num, 
                         begin_of_query_token=begin_of_query_token,
                         end_of_query_token=end_of_query_token,
                         begin_of_documents_token=begin_of_documents_token,
                         end_of_documents_token=end_of_documents_token,
                         begin_of_answer_token=begin_of_answer_token,
                         end_of_answer_token=end_of_answer_token,
                         retriever=retriever, 
                         generator=generator,
                         )
        
        # Create separate prompt templates for forced modes
        self.forced_search_prompt_template = PromptTemplate(
            config=config,
            system_prompt=self.system_prompt,
            user_prompt=self.forced_search_user_prompt
        )
        
        self.forced_answer_prompt_template = PromptTemplate(
            config=config,
            system_prompt=self.system_prompt,
            user_prompt=self.forced_answer_user_prompt
        )
        self.forced_hint_search_prompt_template = PromptTemplate(
            config=config,
            system_prompt=self.system_prompt,
            user_prompt=self.forced_hint_search_user_prompt
        )
        self.under_hint_opd = bool(self._config_get(config, "under_hint_opd", False))

    @staticmethod
    def _config_get(config, key, default=None):
        try:
            return config[key]
        except Exception:
            return getattr(config, key, default)

    @staticmethod
    def _normalize_answer_text(text):
        text = (text or "").lower()
        text = re.sub(r"\b(a|an|the)\b", " ", text)
        text = re.sub(r"[^\w\s]", " ", text)
        return " ".join(text.split())

    def _get_gold_answers(self, item):
        for key in ("golden_answers", "golden_answer", "answers", "answer"):
            value = getattr(item, key, None)
            if value:
                if isinstance(value, str):
                    return [value]
                return list(value)
        return []

    def _answer_kind(self, answer):
        answer = (answer or "").strip()
        if re.fullmatch(r"\d{3,4}([-/]\d{1,2}([-/]\d{1,2})?)?", answer):
            return "date or year"
        if re.search(r"\b(city|county|province|state|country|island|river|mount|lake)\b", answer, re.I):
            return "location"
        if re.search(r"\d", answer):
            return "number"
        if len(answer.split()) >= 2 and answer[:1].isupper():
            return "named entity"
        return "specific fact"

    def _mask_gold_leakage(self, hint, gold_answers):
        safe_hint = hint
        for gold in gold_answers:
            gold = (gold or "").strip()
            if not gold:
                continue
            norm_gold = self._normalize_answer_text(gold)
            if norm_gold in {"yes", "no"} or len(norm_gold) <= 2:
                continue
            pattern = re.escape(gold)
            if re.fullmatch(r"[\w\s]+", gold):
                pattern = r"\b" + pattern + r"\b"
            safe_hint = re.sub(pattern, "[hidden answer]", safe_hint, flags=re.IGNORECASE)
        return safe_hint

    def _question_focus_hint(self, question):
        question = (question or "").strip()
        question = re.sub(r"\s+", " ", question)
        if not question:
            return "the exact fact requested by the question"
        if len(question) > 180:
            question = question[:180].rsplit(" ", 1)[0]
        return f"the exact relation asked in: {question}"

    def _build_oracle_hint(self, item, original_output):
        gold_answers = self._get_gold_answers(item)
        if not gold_answers:
            return None
        wrong_answer = extract_between(original_output, self.begin_of_answer_token, self.end_of_answer_token)
        gold_kind = self._answer_kind(gold_answers[0])
        gold_token_count = len(self._normalize_answer_text(gold_answers[0]).split())
        question_focus = self._question_focus_hint(getattr(item, "question", ""))
        hint = (
            f"The hidden target answer is a {gold_kind}"
            f"{' with ' + str(gold_token_count) + ' normalized token(s)' if gold_token_count else ''}. "
            f"The current candidate may be related but wrong; verify {question_focus} using external evidence. "
            "Form a query for evidence, not for the answer string itself."
        )
        if wrong_answer:
            hint += f" Avoid searching the current candidate answer verbatim: {wrong_answer.strip()}."
        return self._mask_gold_leakage(hint, gold_answers)

    # def run(self, dataset, do_eval=True, pred_process_fun=None):
    #     import re, copy

    #     # 1) 初始化
    #     prompts = [self.prompt_template.get_string(question=question) for question in dataset.question]
    #     dataset.update_output('prompt', prompts)
    #     dataset.update_output('finish_flag', [False] * len(prompts))
    #     dataset.update_output('retrieval_results', [{} for _ in range(len(prompts))])
    #     dataset.update_output('retrieved_times', [0] * len(prompts))
    #     dataset.update_output('simulated_outputs', [[] for _ in range(len(prompts))])  # 存每步的模拟结果

    #     batch_size = getattr(self, "batch_size", 10000)

    #     # 2) 逐步检索/生成循环
    #     for current_step_idx in range(self.max_retrieval_num + 1):
    #         exist_items = [item for item in dataset if item.finish_flag == False]
    #         print(f"Current step: {current_step_idx}, exist_items: {len(exist_items)}")

    #         if len(exist_items) == 0:
    #             print("All prompts are finished")
    #             break

    #         if current_step_idx == self.max_retrieval_num:
    #             print("Max retrieval number reached")
    #             for item in exist_items:
    #                 item.pred = 'No valid answer found'
    #                 item.finish_flag = True
    #                 item.finish_reason = 'Reach max retrieval number'
    #             break

    #         # ---- 关键更改：对 exist_items 分批处理 ----
    #         for start in range(0, len(exist_items), batch_size):
    #             batch_items = exist_items[start:start + batch_size]
    #             batch_prompts = [it.prompt for it in batch_items]

    #             # 2.1 本批生成（带指标）
    #             step_outputs, step_scores, step_perplexities, step_entropies = self.generator.generate(
    #                 batch_prompts, stop=self.stop_tokens, return_scores=True
    #             )

    #             step_query_list = []   # [{'item': item, 'query': query}, ...]
    #             answer_items = []      # [(item, step_output, ppl, ent), ...]
    #             query_items = []       # [(item, step_output, ppl, ent), ...]

    #             # 2.2 解析生成结果、分类
    #             for item, step_output, perplexity, entropy in zip(batch_items, step_outputs, step_perplexities, step_entropies):
    #                 out = step_output.strip()
    #                 if self.end_of_answer_token in out and (out.endswith(self.end_of_answer_token) or out.endswith("<|endoftext|>")):
    #                     item.pred = str(extract_between(out, self.begin_of_answer_token, self.end_of_answer_token))
    #                     item.finish_flag = True
    #                     item.finish_reason = "Finished"
    #                     answer_items.append((item, out, perplexity, entropy))

    #                 elif self.begin_of_query_token in out and out.endswith(self.end_of_query_token):
    #                     query = extract_between(out, self.begin_of_query_token, self.end_of_query_token)
    #                     if query is not None:
    #                         step_query_list.append({'item': item, 'query': query})
    #                         query_items.append((item, out, perplexity, entropy))
    #                     else:
    #                         item.pred = 'No valid answer found'
    #                         item.finish_flag = True
    #                         item.finish_reason = 'Query instruction error'
    #                 else:
    #                     item.pred = out
    #                     item.finish_flag = True
    #                     item.finish_reason = 'Normal finish without answer pattern'

    #             # 2.3 对“需要查询”的样本做强制回答模拟（仅本批）
    #             if query_items:
    #                 simulated_answer_prompts = []
    #                 for item, _, _, _ in query_items:
    #                     question_match = re.search(r"Question: (.*)\n", item.prompt)
    #                     question = question_match.group(1) if question_match else item.question
    #                     forced_answer_base = self.forced_answer_prompt_template.get_string(question=question)
    #                     accumulated_suffix = item.prompt[item.prompt.find("\n", item.prompt.rfind("Question: ")) + 1:] if "<information>" in item.prompt else ""
    #                     simulated_answer_prompts.append(forced_answer_base + accumulated_suffix)

    #                 simulated_answer_outputs, _, _, _ = self.generator.generate(
    #                     simulated_answer_prompts, stop=self.stop_tokens, return_scores=True
    #                 )
    #                 for (item, original_output, perplexity, entropy), answer_out in zip(query_items, simulated_answer_outputs):
    #                     item.simulated_outputs.append({
    #                         'step': current_step_idx,
    #                         'original_output': original_output,
    #                         'answer_only_output': answer_out.strip(),
    #                         'original_perplexity': perplexity,
    #                         'original_entropy': entropy
    #                     })

    #             # 2.4 对“已回答”的样本做强制检索模拟（仅本批）
    #             if answer_items:
    #                 simulated_search_prompts = []
    #                 for item, _, _, _ in answer_items:
    #                     question_match = re.search(r"Question: (.*)\n", item.prompt)
    #                     question = question_match.group(1) if question_match else item.question
    #                     forced_search_base = self.forced_search_prompt_template.get_string(question=question)
    #                     accumulated_suffix = item.prompt[item.prompt.find("\n", item.prompt.rfind("Question: ")) + 1:] if "<information>" in item.prompt else ""
    #                     simulated_search_prompts.append(forced_search_base + accumulated_suffix)

    #                 simulated_search_outputs, _, _, _ = self.generator.generate(
    #                     simulated_search_prompts, stop=self.stop_tokens, return_scores=True
    #                 )
    #                 for (item, original_output, perplexity, entropy), search_out in zip(answer_items, simulated_search_outputs):
    #                     item.simulated_outputs.append({
    #                         'step': current_step_idx,
    #                         'original_output': original_output,
    #                         'search_only_output': search_out.strip(),
    #                         'original_perplexity': perplexity,
    #                         'original_entropy': entropy
    #                     })

    #             # 2.5 把本批生成的 token 追加回各自的 prompt（保持与原逻辑一致）
    #             for item, step_output in zip(batch_items, step_outputs):
    #                 item.prompt = item.prompt + step_output.strip()

    #             # 2.6 仅对本批的查询样本做检索并拼接文档
    #             if len(step_query_list) > 0:
    #                 # 可按批进一步切小（如 retriever 对 batch 大小也有限制），这里直接一批送入
    #                 retrieved_docs_batches = self.retriever.batch_search([it['query'] for it in step_query_list])
    #                 for it, item_retrieved_docs in zip(step_query_list, retrieved_docs_batches):
    #                     item = it['item']
    #                     query = it['query']
    #                     item.retrieval_results[item.retrieved_times] = {
    #                         'query': query,
    #                         'docs': copy.copy(item_retrieved_docs)
    #                     }
    #                     format_doc_string = self._retrieved_docs_to_string(item_retrieved_docs)
    #                     item.prompt += format_doc_string
    #                     item.retrieved_times += 1

    #         # —— 一个 step 的所有小批处理完毕，进入下一个 step ——

    #     dataset = self.evaluate(dataset, do_eval=do_eval, pred_process_fun=pred_process_fun)
    #     return dataset

    # def _retrieved_docs_to_string(self, retrieved_docs: List[Dict], max_content_len=100):
    #     format_doc_string = ""
    #     for idx, doc in enumerate(retrieved_docs):
    #         contents = doc['contents']
    #         title = contents.split('\n')[0]
    #         text = '\n'.join(contents.split('\n')[1:])
    #         text = text[:max_content_len]
    #         format_doc_string += f"Doc {idx+1}(Title: {title}) {text}\n"
    #     format_doc_string = f'\n\n{self.begin_of_documents_token}\n{format_doc_string}\n{self.end_of_documents_token}\n\n'
    #     return format_doc_string

    # def decision_boundary_metric(self, metric_file="metric_score.txt", intermediate_data_file="intermediate_data.json"):
    #     """
    #     生成决策边界分析报告，并将其追加到指定的指标文件中。
    #     """
    #     save_path = os.path.join(self.evaluator.save_dir, metric_file)
    #     decision_boundary_text = generate_analysis_report(self.evaluator.save_dir)
    #     try:
    #         with open(save_path, 'a', encoding="utf-8") as f:
    #             f.write("\n\n--- Decision Boundary Analysis Report ---\n")
    #             f.write(decision_boundary_text)

    #         print(f"Analysis report has been successfully appended to: {save_path}")

    #     except Exception as e:
    #         print(f"An error occurred while writing to {save_path}: {e}")        
    def decision_boundary_metric(self, metric_file="metric_score.txt", time_info=None):
        save_path = os.path.join(self.evaluator.save_dir, metric_file)
        decision_boundary_text = generate_analysis_report(self.evaluator.save_dir)
        
        try:
            with open(save_path, 'a', encoding="utf-8") as f:
                # 写入决策边界报告
                f.write("\n\n--- Decision Boundary Analysis Report ---\n")
                f.write(decision_boundary_text)
                
                # 如果有时间信息，则写入时间信息
                if time_info:
                    f.write("\n\n--- Time Consumption Report ---\n")
                    f.write(f"Total processing time: {time_info['total_time']:.2f} seconds\n")
                    f.write(f"Average time per sample: {time_info['avg_time_per_sample']:.4f} seconds\n")

            print(f"Analysis report and time info have been successfully appended to: {save_path}")

        except Exception as e:
            print(f"An error occurred while writing to {save_path}: {e}")

    def run(self, dataset, do_eval=True, pred_process_fun=None):
        start_time = time.time()
        num_samples = len(dataset.question)

        prompts = [self.prompt_template.get_string(question=question) for question in dataset.question]
        dataset.update_output('prompt', prompts)
        dataset.update_output('finish_flag', [False] * len(prompts))
        dataset.update_output('retrieval_results', [{} for _ in range(len(prompts))])
        dataset.update_output('retrieved_times', [0] * len(prompts))
        dataset.update_output('simulated_outputs', [[] for _ in range(len(prompts))])  # New field to store simulated results per step

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

            # 调用生成器时返回额外指标
            step_outputs, step_scores, step_perplexities, step_entropies = self.generator.generate(
                exist_prompts, stop=self.stop_tokens, return_scores=True
            )

            step_query_list = []  # store generated queries for retrieval
            answer_items = []    # store items with answer tokens
            query_items = []     # store items with query tokens

            # Parse each sample's step output and categorize items
            for item, step_output, perplexity, entropy in zip(exist_items, step_outputs, step_perplexities, step_entropies):
                if self.end_of_answer_token in step_output and (step_output.endswith(self.end_of_answer_token) or step_output.endswith("<|endoftext|>")):
                    item.pred = str(extract_between(step_output, self.begin_of_answer_token, self.end_of_answer_token))
                    item.finish_flag = True
                    item.finish_reason = "Finished"
                    answer_items.append((item, step_output.strip(), perplexity, entropy))
                elif self.begin_of_query_token in step_output and step_output.endswith(self.end_of_query_token):
                    query = extract_between(step_output, self.begin_of_query_token, self.end_of_query_token)
                    if query is not None:
                        step_query_list.append({'item': item, 'query': query})
                        query_items.append((item, step_output.strip(), perplexity, entropy))
                    else:
                        item.pred = 'No valid answer found'
                        item.finish_flag = True
                        item.finish_reason = 'Query instruction error'
                else:
                    item.pred = step_output.strip()
                    item.finish_flag = True
                    item.finish_reason = 'Normal finish without answer pattern'

            # Handle query items: construct prompts and perform forced search
            if query_items:
                simulated_answer_prompts = []
                for item, _, _, _ in query_items:
                    question_match = re.search(r"Question: (.*)\n", item.prompt)
                    question = question_match.group(1) if question_match else item.question
                    forced_answer_base = self.forced_answer_prompt_template.get_string(question=question)
                    accumulated_suffix = item.prompt[item.prompt.find("\n", item.prompt.rfind("Question: ")) + 1:] if "<information>" in item.prompt else ""
                    simulated_answer_prompt = forced_answer_base + accumulated_suffix
                    simulated_answer_prompts.append(simulated_answer_prompt)

                simulated_answer_outputs, _, _, _ = self.generator.generate(simulated_answer_prompts, stop=self.stop_tokens, return_scores=True)
                for (item, original_output, perplexity, entropy), answer_out in zip(query_items, simulated_answer_outputs):
                    item.simulated_outputs.append({
                        'step': current_step_idx,
                        'original_output': original_output,
                        'answer_only_output': answer_out.strip(),
                        'original_perplexity': perplexity,
                        'original_entropy': entropy
                    })

            # Handle answer items: construct prompts and perform forced answer
            if answer_items:
                simulated_search_prompts = []
                simulated_search_hints = []
                for item, original_output, _, _ in answer_items:
                    question_match = re.search(r"Question: (.*)\n", item.prompt)
                    question = question_match.group(1) if question_match else item.question
                    oracle_hint = None
                    if self.under_hint_opd:
                        oracle_hint = self._build_oracle_hint(item, original_output)
                    if oracle_hint:
                        forced_search_base = self.forced_hint_search_prompt_template.get_string(
                            question=question,
                            hint=oracle_hint,
                        )
                        # OPD hint search must not inherit retrieved passages because they may
                        # contain the gold answer. The hint is the only oracle signal here.
                        accumulated_suffix = ""
                    else:
                        forced_search_base = self.forced_search_prompt_template.get_string(question=question)
                        accumulated_suffix = item.prompt[item.prompt.find("\n", item.prompt.rfind("Question: ")) + 1:] if "<information>" in item.prompt else ""
                    simulated_search_prompt = forced_search_base + accumulated_suffix
                    simulated_search_prompts.append(simulated_search_prompt)
                    simulated_search_hints.append(oracle_hint)

                simulated_search_outputs, _, _, _ = self.generator.generate(simulated_search_prompts, stop=self.stop_tokens, return_scores=True)
                for (item, original_output, perplexity, entropy), search_out, oracle_hint in zip(answer_items, simulated_search_outputs, simulated_search_hints):
                    item.simulated_outputs.append({
                        'step': current_step_idx,
                        'original_output': original_output,
                        'search_only_output': search_out.strip(),
                        'oracle_hint': oracle_hint,
                        'under_hint_opd': bool(oracle_hint),
                        'original_perplexity': perplexity,
                        'original_entropy': entropy
                    })

            for item, step_output in zip(exist_items, step_outputs):
                item.prompt = item.prompt + step_output.strip()

            # Do retrieval and add retrieved docs to prompt for query items
            if len(step_query_list) > 0:
                retrieved_docs = self.retriever.batch_search([it['query'] for it in step_query_list])
                for it, item_retrieved_docs in zip(step_query_list, retrieved_docs):
                    item = it['item']
                    query = it['query']
                    item.retrieval_results[item.retrieved_times] = {'query': query, 'docs': copy.copy(item_retrieved_docs)}
                    format_doc_string = self._retrieved_docs_to_string(item_retrieved_docs)
                    item.prompt += format_doc_string
                    item.retrieved_times += 1

        dataset = self.evaluate(dataset, do_eval=do_eval, pred_process_fun=pred_process_fun)
        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_sample = total_time / num_samples if num_samples > 0 else 0
        
        time_info = {
            "total_time": total_time,
            "avg_time_per_sample": avg_time_per_sample
        }
        
        self.decision_boundary_metric(time_info=time_info)
        # self.decision_boundary_metric()
        return dataset


class SimulatedReasoningPipeline(ReasoningPipeline):
    # Forced search prompt: instructs the model to always generate a search query
    forced_search_system_prompt = ""
    forced_search_user_prompt = (
        "The User asks a question, and the Assistant solves it.\n"
        "The Assistant first thinks about the reasoning process in the mind.\n"
        "The Assistant MUST perform a search for uncertain knowledge.\n"
        "Generate the reasoning process and a search query with the format of "
        "\"<think> reasoning process here </think><|begin_of_query|> search query (only keywords) here <|end_of_query|>\". **A query must involve only a single triple**.\n\n"
        "User:{question}\n"
        "Assistant: <think>"
    )

    # Forced answer prompt: instructs the model to always provide a final answer without searching
    forced_answer_system_prompt = ""
    forced_answer_user_prompt = (
        "The User asks a question, and the Assistant solves it.\n"
        "The Assistant first thinks about the reasoning process in the mind and then provides the User with the final answer WITHOUT performing any search.\n"
        "The output format of reasoning process and final answer are enclosed within <think> </think> and <answer> </answer> tags, "
        "respectively, i.e., \"<think> reasoning process here </think>\\n\\n<answer> final answer here </answer>\".\n\n"
        "User:{question}\n"
        "Assistant: <think>"
    )

    def __init__(self, config, 
                 prompt_template=None, 
                 forced_search_prompt_template=None,
                 forced_answer_prompt_template=None,
                 max_retrieval_num=5, 
                 begin_of_query_token="<|begin_of_query|>",
                 end_of_query_token="<|end_of_query|>",
                 begin_of_documents_token="<|begin_of_documents|>",
                 end_of_documents_token="<|end_of_documents|>",
                 begin_of_answer_token="<answer>",
                 end_of_answer_token='</answer>',
                 retriever=None, 
                 generator=None):
        super().__init__(config, prompt_template, max_retrieval_num, begin_of_query_token, end_of_query_token,
                         begin_of_documents_token, end_of_documents_token, begin_of_answer_token, end_of_answer_token,
                         retriever, generator)

        if forced_search_prompt_template is None:
            self.forced_search_prompt_template = PromptTemplate(
                config=config,
                system_prompt=self.forced_search_system_prompt,
                user_prompt=self.forced_search_user_prompt
            )
        else:
            self.forced_search_prompt_template = forced_search_prompt_template

        if forced_answer_prompt_template is None:
            self.forced_answer_prompt_template = PromptTemplate(
                config=config,
                system_prompt=self.forced_answer_system_prompt,
                user_prompt=self.forced_answer_user_prompt
            )
        else:
            self.forced_answer_prompt_template = forced_answer_prompt_template

        self.framework = config.framework
        self.stop_tokens = [self.end_of_query_token, "<|im_end|>", "<|endoftext|>", self.end_of_answer_token]

    def _update_prompt(self, item, new_content):
        """Update the prompt with new content, handling OpenAI message format if needed."""
        if self.framework == "openai" and isinstance(item.prompt, list):
            item.prompt[-1]['content'] += new_content
        else:
            item.prompt += new_content

    def _get_prompt_content(self, prompt):
        """Extract content from prompt, handling both string and OpenAI message formats."""
        if self.framework == "openai" and isinstance(prompt, list) and prompt:
            return prompt[-1]['content'] if 'content' in prompt[-1] else ""
        return prompt

    def _create_message_prompt(self, content, role='user'):
        """Create a prompt in OpenAI message format."""
        return [{'role': "system", 'content': ""}, {'role': role, 'content': content}]

    def run(self, dataset, do_eval=True, pred_process_fun=None):
        # Initialize main prompts
        prompts = []
        for question in dataset.question:
            prompt_template_output = self.prompt_template.get_string(question=question)
            if self.framework == "openai" and isinstance(prompt_template_output, list):
                prompts.append(prompt_template_output)
            else:
                prompts.append(prompt_template_output)
        
        dataset.update_output('prompt', prompts)
        dataset.update_output('finish_flag', [False] * len(prompts))
        dataset.update_output('retrieval_results', [{} for _ in range(len(prompts))])
        dataset.update_output('retrieved_times', [0] * len(prompts))
        dataset.update_output('simulated_outputs', [[] for _ in range(len(prompts))])

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
                    item.simulated_outputs.append({
                        'step': current_step_idx,
                        'original_output': 'No valid answer found'
                    })
                break

            # Generate main step outputs
            step_outputs = self.generator.generate(exist_prompts, stop=self.stop_tokens)
            step_query_list = []  # store generated queries for retrieval
            
            # Prepare simulated prompts for forced search and answer
            simulated_search_prompts = []
            simulated_answer_prompts = []
            for item in exist_items:
                current_content = self._get_prompt_content(item.prompt)
                print("current prompt")
                print(item.prompt)
                
                question = item.question
                # Get forced prompt content from template
                forced_search_template = self.forced_search_prompt_template.get_string(question=question)
                forced_answer_template = self.forced_answer_prompt_template.get_string(question=question)
                print("forced_search_template")
                print(forced_search_template)
                # Extract content if template returns list of dicts (OpenAI format)
                forced_search_content = forced_search_template[-1]['content'] if self.framework == "openai" and isinstance(forced_search_template, list) else forced_search_template
                print("forced_search_content")
                print(forced_search_content)
                forced_answer_content = forced_answer_template[-1]['content'] if self.framework == "openai" and isinstance(forced_answer_template, list) else forced_answer_template
                # Replace the main prompt content with forced content, keeping any appended docs
                main_prompt_content = self._get_prompt_content(self.prompt_template.get_string(question=question))
                forced_search_content = current_content.replace(main_prompt_content, forced_search_content)
                print("forced_search_content")
                print(forced_search_content)
                forced_answer_content = current_content.replace(main_prompt_content, forced_answer_content)
                if self.framework == "openai":
                    simulated_search_prompts.append(self._create_message_prompt(forced_search_content))
                    simulated_answer_prompts.append(self._create_message_prompt(forced_answer_content))
                else:
                    simulated_search_prompts.append(forced_search_content)
                    simulated_answer_prompts.append(forced_answer_content)

            simulated_search_outputs = []
            simulated_answer_outputs = []
            if simulated_search_prompts:
                simulated_search_outputs = self.generator.generate(simulated_search_prompts, stop=self.stop_tokens)
                simulated_answer_outputs = self.generator.generate(simulated_answer_prompts, stop=self.stop_tokens)
            
            # normalize simulated outputs
            if simulated_search_outputs is None:
                simulated_search_outputs = []
            elif isinstance(simulated_search_outputs, (str, dict)):
                simulated_search_outputs = [simulated_search_outputs]

            if simulated_answer_outputs is None:
                simulated_answer_outputs = []
            elif isinstance(simulated_answer_outputs, (str, dict)):
                simulated_answer_outputs = [simulated_answer_outputs]

            # Save simulated outputs to each item — iterate by index to avoid index lookup issues
            for idx, item in enumerate(exist_items):
                orig_raw = step_outputs[idx] if idx < len(step_outputs) else ""
                search_raw = simulated_search_outputs[idx] if idx < len(simulated_search_outputs) else ""
                answer_raw = simulated_answer_outputs[idx] if idx < len(simulated_answer_outputs) else ""

                orig_content = self._get_prompt_content(orig_raw).strip()
                search_content = self._get_prompt_content(search_raw).strip()
                answer_content = self._get_prompt_content(answer_raw).strip()

                item.simulated_outputs.append({
                    'step': current_step_idx,
                    'original_output': copy.copy(orig_content),
                    'search_only_output': search_content,
                    'answer_only_output': answer_content
                })

            # Parse each sample's step output
            for item, step_output in zip(exist_items, step_outputs):
                # Extract content for processing
                step_output_content = step_output['content'] if self.framework == "openai" and isinstance(step_output, dict) else step_output
                self._update_prompt(item, step_output_content.strip())

                if self.begin_of_answer_token in step_output_content and (step_output_content.endswith(self.end_of_query_token) or step_output_content.endswith("<|endoftext|>")):
                    item.pred = str(extract_between(step_output_content, self.begin_of_answer_token, self.end_of_query_token))
                    item.finish_flag = True
                    item.finish_reason = "Finished"
                
                elif self.begin_of_query_token in step_output_content and step_output_content.endswith(self.end_of_query_token):
                    query = extract_between(step_output_content, self.begin_of_query_token, self.end_of_query_token)
                    if query is not None:
                        step_query_list.append({'item': item, 'query': query})
                    else:
                        item.pred = 'No valid answer found'
                        item.finish_flag = True
                        item.finish_reason = 'Query instruction error'
                
                else:
                    item.pred = step_output_content.strip()
                    item.finish_flag = True
                    item.finish_reason = 'Normal finish without answer pattern'

            # Do retrieval and add retrieved docs to prompt
            if len(step_query_list) > 0:
                retrieved_docs = self.retriever.batch_search([it['query'] for it in step_query_list])
                for it, item_retrieved_docs in zip(step_query_list, retrieved_docs):
                    item = it['item']
                    query = it['query']
                    item.retrieval_results[item.retrieved_times] = {'query': query, 'docs': copy.copy(item_retrieved_docs)}
                    format_doc_string = self._retrieved_docs_to_string(item_retrieved_docs)
                    self._update_prompt(item, format_doc_string.strip())
                    item.retrieved_times += 1

        dataset = self.evaluate(dataset, do_eval=do_eval, pred_process_fun=pred_process_fun)
        return dataset


class SimulatedSearchO1(ReasoningPipeline):
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

    forced_answer_user_prompt = (
        "Given the related query: <|begin_search_query|> your query here <|end_search_query|>.\n"
        "The system search and analyze relevant web pages, then provide you with helpful information in the format <|begin_search_result|> ...search results... <|end_search_result|>.\n\n"
        "Please answer the following question. You should think step by step to solve it.\n\n"
        'Now, provide your final answer in the format \\boxed{{YOUR_ANSWER}}.\n\n'
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

        self.forced_answer_prompt_template = PromptTemplate(
            config=config,
            system_prompt=self.system_prompt,
            user_prompt=self.forced_answer_user_prompt
        )

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

    def _append_to_answer_prompt(self, item, content: str):
        if self.is_openai:
            if len(item.answer_prompt) > 0 and isinstance(item.answer_prompt[0], dict) and 'content' in item.answer_prompt[0]:
                item.answer_prompt[0]['content'] += content
            else:
                # Fallback if not in expected format
                item.answer_prompt += content
        else:
            item.answer_prompt += content

    def decision_boundary_metric(self, metric_file="metric_score.txt", time_info=None):
        save_path = os.path.join(self.evaluator.save_dir, metric_file)
        decision_boundary_text = generate_analysis_report(self.evaluator.save_dir)
        
        try:
            with open(save_path, 'a', encoding="utf-8") as f:
                # 写入决策边界报告
                f.write("\n\n--- Decision Boundary Analysis Report ---\n")
                f.write(decision_boundary_text)
                
                # 如果有时间信息，则写入时间信息
                if time_info:
                    f.write("\n\n--- Time Consumption Report ---\n")
                    f.write(f"Total processing time: {time_info['total_time']:.2f} seconds\n")
                    f.write(f"Average time per sample: {time_info['avg_time_per_sample']:.4f} seconds\n")

            print(f"Analysis report and time info have been successfully appended to: {save_path}")

        except Exception as e:
            print(f"An error occurred while writing to {save_path}: {e}")

    def run(self, dataset, do_eval=True, pred_process_fun=None):
        start_time = time.time()
        num_samples = len(dataset.question)

        prompts = [self.prompt_template.get_string(question=question) for question in dataset.question]
        answer_prompts = [self.forced_answer_prompt_template.get_string(question=question) for question in dataset.question]
        dataset.update_output('prompt', prompts)
        dataset.update_output('answer_prompt', [copy.deepcopy(p) for p in answer_prompts])
        dataset.update_output('finish_flag', [False] * len(prompts))
        dataset.update_output('retrieval_results', [{} for _ in range(len(prompts))])
        dataset.update_output('retrieved_times', [0] * len(prompts))
        dataset.update_output('searched_queries', [[] for _ in range(len(prompts))])
        dataset.update_output('simulated_outputs', [[] for _ in range(len(prompts))])

        # Logic of reasoning
        for current_step_idx in range(self.max_retrieval_num + 1):
            exist_items = [item for item in dataset if item.finish_flag == False]
            exist_prompts = [item.prompt for item in exist_items]
            exist_answer_prompts = [item.answer_prompt for item in exist_items]
            
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
            answer_step_outputs = self.generator.generate(exist_answer_prompts, stop=self.stop_tokens)

            step_query_list = []  # store generated queries for retrieval

            # parse each sample's step output
            for item, step_output, answer_step_output in zip(exist_items, step_outputs, answer_step_outputs):
                orig_content = step_output.strip()
                answer_content = answer_step_output.strip()
                item.simulated_outputs.append({
                    'step': current_step_idx,
                    'original_output': copy.copy(orig_content),
                    'answer_only_output': answer_content,
                })

                self._append_to_prompt(item, orig_content)
                self._append_to_answer_prompt(item, orig_content)

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
                        self._append_to_answer_prompt(item, format_result_string)
                        item.searched_queries.append(query)
                        item.retrieval_results[item.retrieved_times] = {'query': query, 'docs': copy.copy(retrieved_docs), 'summary': info}
                        item.retrieved_times += 1

        dataset = self.evaluate(dataset, do_eval=do_eval, pred_process_fun=pred_process_fun)
        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_sample = total_time / num_samples if num_samples > 0 else 0
        
        time_info = {
            "total_time": total_time,
            "avg_time_per_sample": avg_time_per_sample
        }
        
        self.decision_boundary_metric(time_info=time_info)
        return dataset
