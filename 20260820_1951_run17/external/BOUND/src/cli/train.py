"""Standard DPO training entry point."""

from __future__ import annotations

import argparse
import gc
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default="Qwen/Qwen3-4B-Instruct-2507")
    parser.add_argument("--per-device-batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=16)
    parser.add_argument(
        "--question-mapping",
        action="append",
        default=[],
        help="JSON/JSONL question table; repeat for multiple sources",
    )
    parser.add_argument(
        "--resolved-dataset-output",
        help="optional path for the reconstructed three-field DPO JSONL",
    )
    parser.add_argument(
        "--preprocess-only",
        action="store_true",
        help="validate/reconstruct the dataset and exit before loading a model",
    )
    parser.add_argument(
        "--validate-tokenization",
        action="store_true",
        help="apply the model chat template to every chosen/rejected example",
    )
    parser.add_argument("--max-train-samples", type=int)
    parser.add_argument("--max-steps", type=int, default=-1)
    parser.add_argument("--max-length", type=int, default=8192)
    parser.add_argument(
        "--max-prompt-length",
        type=int,
        default=7936,
        help="maximum templated prompt length before DPO collation",
    )
    parser.add_argument(
        "--max-completion-length",
        type=int,
        default=256,
        help="maximum templated chosen/rejected completion length",
    )
    parser.add_argument(
        "--truncation-mode",
        choices=("keep_start", "keep_end"),
        default="keep_end",
        help="TRL fallback when a final sequence still exceeds max-length",
    )
    parser.add_argument(
        "--fp32",
        action="store_true",
        help="disable the default BF16 setting for a CPU or compatibility smoke test",
    )
    return parser.parse_args()


def _validate_length_settings(
    *, max_length: int, max_prompt_length: int, max_completion_length: int
) -> None:
    for name, value in (
        ("max_length", max_length),
        ("max_prompt_length", max_prompt_length),
        ("max_completion_length", max_completion_length),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{name} must be a positive integer")
    if max_prompt_length + max_completion_length > max_length:
        raise ValueError(
            "max_prompt_length + max_completion_length must not exceed max_length"
        )


def validate_tokenization(
    records,
    tokenizer,
    *,
    max_length: int = 8192,
    max_prompt_length: int = 7936,
    max_completion_length: int = 256,
    truncation_mode: str = "keep_end",
    trl_preprocessing=None,
) -> dict[str, int]:
    """Audit the exact conversational preprocessing used by TRL's DPOTrainer."""

    _validate_length_settings(
        max_length=max_length,
        max_prompt_length=max_prompt_length,
        max_completion_length=max_completion_length,
    )
    if truncation_mode not in {"keep_start", "keep_end"}:
        raise ValueError("truncation_mode must be keep_start or keep_end")
    use_dataset_pipeline = trl_preprocessing is None
    if use_dataset_pipeline:
        from datasets import Dataset
        from trl import DPOTrainer
        from trl.data_utils import maybe_apply_chat_template, maybe_extract_prompt
    else:
        DPOTrainer, maybe_apply_chat_template, maybe_extract_prompt = trl_preprocessing

    from prompts import SEARCH_POLICY_SYSTEM
    from schema import Action

    maximum_prompt = 0
    maximum_completion = 0
    maximum_sequence = 0
    if use_dataset_pipeline:
        tokenized_records = Dataset.from_list(records)
        tokenized_records = tokenized_records.map(
            maybe_extract_prompt, writer_batch_size=10
        )
        tokenized_records = tokenized_records.map(
            maybe_apply_chat_template,
            fn_kwargs={"tokenizer": tokenizer, "tools": None},
            writer_batch_size=10,
        )
        tokenized_records = tokenized_records.map(
            DPOTrainer.tokenize_row,
            remove_columns=["chosen", "rejected"],
            fn_kwargs={
                "processing_class": tokenizer,
                "max_prompt_length": max_prompt_length,
                "max_completion_length": max_completion_length,
                "add_special_tokens": False,
            },
            writer_batch_size=10,
        )
    else:
        tokenized_records = []
        for record in records:
            formatted = maybe_apply_chat_template(
                maybe_extract_prompt(dict(record)), tokenizer=tokenizer, tools=None
            )
            tokenized_records.append(
                DPOTrainer.tokenize_row(
                    formatted,
                    processing_class=tokenizer,
                    max_prompt_length=max_prompt_length,
                    max_completion_length=max_completion_length,
                    add_special_tokens=False,
                )
            )

    for index, (record, tokenized) in enumerate(
        zip(records, tokenized_records), 1
    ):
        prompt_ids = tokenized["prompt_input_ids"]
        prompt_text = tokenizer.decode(prompt_ids, skip_special_tokens=False)
        if SEARCH_POLICY_SYSTEM not in prompt_text:
            raise ValueError(
                f"row {index} loses the student system prompt after TRL prompt truncation"
            )
        maximum_prompt = max(maximum_prompt, len(prompt_ids))
        for field in ("chosen", "rejected"):
            completion_ids = tokenized[f"{field}_input_ids"]
            sequence_ids = [*prompt_ids, *completion_ids]
            if len(sequence_ids) > max_length:
                sequence_ids = (
                    sequence_ids[:max_length]
                    if truncation_mode == "keep_start"
                    else sequence_ids[-max_length:]
                )
            completion_text = tokenizer.decode(
                completion_ids, skip_special_tokens=False
            )
            sequence_text = tokenizer.decode(sequence_ids, skip_special_tokens=False)
            action = Action.parse(record[field][0]["content"])
            required = (
                f"[Action]: {action.action}",
                f"[Parameter]: {action.parameter}",
                tokenizer.eos_token,
            )
            if not completion_ids or any(
                marker not in completion_text or marker not in sequence_text
                for marker in required
            ):
                raise ValueError(
                    f"row {index} {field} loses its action, parameter, or assistant end marker "
                    "after TRL preprocessing"
                )
            maximum_completion = max(maximum_completion, len(completion_ids))
            maximum_sequence = max(maximum_sequence, len(sequence_ids))
        if index % 50 == 0:
            gc.collect()
    return {
        "max_prompt_tokens": maximum_prompt,
        "max_completion_tokens": maximum_completion,
        "max_sequence_tokens": maximum_sequence,
    }


def main() -> None:
    args = parse_args()

    _validate_length_settings(
        max_length=args.max_length,
        max_prompt_length=args.max_prompt_length,
        max_completion_length=args.max_completion_length,
    )

    from jsonl_io import read_jsonl, write_jsonl
    from preferences import validate_training_record
    from questions import load_question_mapping, resolve_training_record

    raw_dataset = list(read_jsonl(args.dataset))
    question_mapping = load_question_mapping(args.question_mapping)
    records = []
    modes = {}
    chosen_modified = 0
    rejected_modified = 0
    for index, record in enumerate(raw_dataset):
        try:
            resolved, metadata = resolve_training_record(dict(record), question_mapping)
            validate_training_record(resolved)
        except (KeyError, ValueError) as exc:
            raise ValueError(f"invalid DPO row {index + 1}: {exc}") from exc
        chosen_modified += int(resolved["chosen"] != record.get("chosen"))
        rejected_modified += int(resolved["rejected"] != record.get("rejected"))
        mode = metadata["mode"]
        modes[mode] = modes.get(mode, 0) + 1
        records.append(resolved)
    if not records:
        raise ValueError("DPO dataset is empty")
    if chosen_modified or rejected_modified:
        raise AssertionError("question reconstruction modified chosen/rejected content")
    if args.resolved_dataset_output:
        write_jsonl(args.resolved_dataset_output, records)

    tokenizer = None
    if args.validate_tokenization or not args.preprocess_only:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(args.model)
    tokenization_summary = None
    if args.validate_tokenization:
        tokenization_summary = validate_tokenization(
            records,
            tokenizer,
            max_length=args.max_length,
            max_prompt_length=args.max_prompt_length,
            max_completion_length=args.max_completion_length,
            truncation_mode=args.truncation_mode,
        )

    summary = {
        "records": len(records),
        "resolution_modes": modes,
        "question_mapping_entries": len(question_mapping),
        "chosen_modified": chosen_modified,
        "rejected_modified": rejected_modified,
        "tokenization_validated": bool(args.validate_tokenization),
        "length_settings": {
            "max_length": args.max_length,
            "max_prompt_length": args.max_prompt_length,
            "max_completion_length": args.max_completion_length,
            "truncation_mode": args.truncation_mode,
        },
        "tokenization_summary": tokenization_summary,
    }
    print(json.dumps(summary, ensure_ascii=False))
    if args.preprocess_only:
        return

    from datasets import Dataset
    from trl import DPOConfig, DPOTrainer

    train_records = records
    if args.max_train_samples is not None:
        if args.max_train_samples < 1:
            raise ValueError("--max-train-samples must be positive")
        train_records = records[: args.max_train_samples]
    dataset = Dataset.from_list(train_records)
    config = DPOConfig(
        output_dir=args.output_dir,
        num_train_epochs=1,
        learning_rate=1e-6,
        beta=0.1,
        max_length=args.max_length,
        max_prompt_length=args.max_prompt_length,
        max_completion_length=args.max_completion_length,
        truncation_mode=args.truncation_mode,
        bf16=not args.fp32,
        seed=42,
        per_device_train_batch_size=args.per_device_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        report_to="none",
        max_steps=args.max_steps,
    )
    trainer = DPOTrainer(
        model=args.model,
        ref_model=args.model,
        args=config,
        train_dataset=dataset,
        processing_class=tokenizer,
    )
    trainer.train()
    trainer.save_model(args.output_dir)


if __name__ == "__main__":
    main()
