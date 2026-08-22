import re
from tqdm import tqdm
from typing import List, Tuple, Dict, Optional, Union
import math
import json
import numpy as np
import copy
# from transformers import AutoTokenizer, PreTrainedTokenizer, PreTrainedTokenizerFast
from flashrag.utils import get_retriever, get_generator, selfask_pred_parse, ircot_pred_parse
from flashrag.pipeline import BasicPipeline
from flashrag.pipeline.pipeline import SequentialPipeline
from flashrag.pipeline.ReaRAG_utils import AgentUtils
from flashrag.dataset.utils import get_batch_dataset, merge_batch_dataset
from flashrag.prompt import PromptTemplate
from flashrag.prompt import get_generate_final_answer_message, get_generate_intermediate_answer_message, get_generate_subquery_message
from flashrag.utils.utils import extract_between, extract_between_all

class JudgmentSequentialPipeline(SequentialPipeline):
    # Define judgment prompt templates with forced reasoning and answer structure
    judgment_user_prompt = (
        "Answer the given question. "
        "You must conduct reasoning inside <think> and </think> first every time you get new information. "
        "After reasoning, since you have all the information needed, you must directly provide the answer inside <answer> and </answer>, without detailed illustrations or further searches. "
        "If you do not know or are unsure, output <answer><Unknown></answer>. "
        "For example, <answer>Beijing</answer>. "
        "Question: {question}\n"
    )
    
    judgment_user_prompt_with_rag = (
        "Answer the given question based on the provided information below. "
        "You must conduct reasoning inside <think> and </think> first every time you get new information. "
        "After reasoning, since you have all the information needed, you must directly provide the answer inside <answer> and </answer>, without detailed illustrations or further searches. "
        "If you do not know or are unsure, output <answer><Unknown></answer>. "
        "For example, <answer>Beijing</answer>. "
        "Provided information: {reference}\n"
        "Question: {question}\n"
    )

    def __init__(self, config, prompt_template=None, retriever=None, generator=None):
        super().__init__(config, prompt_template, retriever, generator)
        
        # Create judgment prompt templates
        self.judgment_prompt_template = PromptTemplate(
            config=config,
            system_prompt=self.prompt_template.system_prompt if self.prompt_template.system_prompt else "",
            user_prompt=self.judgment_user_prompt
        )
        
        self.judgment_prompt_template_with_rag = PromptTemplate(
            config=config,
            system_prompt=self.prompt_template.system_prompt if self.prompt_template.system_prompt else "",
            user_prompt=self.judgment_user_prompt_with_rag
        )

    def naive_run(self, dataset, do_eval=True, pred_process_fun=None):
        # Standard direct generation (unchanged)
        input_prompts = [self.prompt_template.get_string(question=q) for q in dataset.question]
        dataset.update_output("prompt", input_prompts)
        
        pred_answer_list = self.generator.generate(input_prompts)
        dataset.update_output("pred", pred_answer_list)
        
        # Add judgment simulation
        judgment_prompts = [self.judgment_prompt_template.get_string(question=q) for q in dataset.question]
        judgment_outputs = self.generator.generate(judgment_prompts)
        
        # Parse judgment outputs
        judgment_preds = []
        for output in judgment_outputs:
            # Extract answer between <answer> and </answer>
            answer = extract_between(output, "<answer>", "</answer>")
            if answer:
                judgment_preds.append(answer.strip())
            else:
                judgment_preds.append("<Unknown>")
        
        dataset.update_output("judgment_pred", judgment_preds)
        dataset.update_output("judgment_prompt", judgment_prompts)
        dataset.update_output("judgment_raw_output", judgment_outputs)

        dataset = self.evaluate(dataset, do_eval=do_eval, pred_process_fun=pred_process_fun)
        return dataset

    def run(self, dataset, do_eval=True, pred_process_fun=None):
        input_query = dataset.question
        retrieval_results = self.retriever.batch_search(input_query)
        dataset.update_output("retrieval_result", retrieval_results)

        if self.refiner:
            input_prompt_flag = self.refiner.input_prompt_flag
            if "llmlingua" in self.refiner.name and input_prompt_flag:
                # Input prompt
                input_prompts = [
                    self.prompt_template.get_string(question=q, retrieval_result=r)
                    for q, r in zip(dataset.question, dataset.retrieval_result)
                ]
                dataset.update_output("prompt", input_prompts)
                input_prompts = self.refiner.batch_run(dataset)
            else:
                # Input retrieval docs
                refine_results = self.refiner.batch_run(dataset)
                dataset.update_output("refine_result", refine_results)
                input_prompts = [
                    self.prompt_template.get_string(question=q, formatted_reference=r)
                    for q, r in zip(dataset.question, refine_results)
                ]
        else:
            if not self.use_fid:
                input_prompts = [
                    self.prompt_template.get_string(question=q, retrieval_result=r)
                    for q, r in zip(dataset.question, dataset.retrieval_result)
                ]

        if self.use_fid:
            print("Use FiD generation")
            input_prompts = []
            for item in dataset:
                q = item.question
                docs = item.retrieval_result
                input_prompts.append([q + " " + doc['contents'] for doc in docs])
        dataset.update_output("prompt", input_prompts)

        # Delete used refiner to release memory
        if self.refiner:
            del self.refiner
        pred_answer_list = self.generator.generate(input_prompts)
        dataset.update_output("pred", pred_answer_list)
        
        # Add judgment simulation with RAG
        if self.use_fid:
            print("Skipping judgment for FiD mode")
            judgment_preds = ["Skipped for FiD"] * len(dataset)
            judgment_prompts = ["Skipped for FiD"] * len(dataset)
            judgment_outputs = ["Skipped for FiD"] * len(dataset)
        else:
            judgment_prompts = [
                self.judgment_prompt_template_with_rag.get_string(question=q, retrieval_result=r)
                for q, r in zip(dataset.question, dataset.retrieval_result)
            ]
            judgment_outputs = self.generator.generate(judgment_prompts)
            
            # Parse judgment outputs
            judgment_preds = []
            for output in judgment_outputs:
                # Extract answer between <answer> and </answer>
                answer = extract_between(output, "<answer>", "</answer>")
                if answer:
                    judgment_preds.append(answer.strip())
                else:
                    judgment_preds.append("<Unknown>")
            
            dataset.update_output("judgment_prompt", judgment_prompts)
            dataset.update_output("judgment_raw_output", judgment_outputs)
        
        dataset.update_output("judgment_pred", judgment_preds)

        dataset = self.evaluate(dataset, do_eval=do_eval, pred_process_fun=pred_process_fun)

        return dataset