"""Run the trained policy in a fixed HTTP retrieval environment."""

from __future__ import annotations

import argparse
import json
import math
import os
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import Any

from cli.evaluate import normalize
from context import append_and_deduplicate
from jsonl_io import read_jsonl, write_jsonl
from prompts import render_student_prompt
from schema import Action, SearchState


class RetrievalError(RuntimeError):
    """Raised when the retrieval backend cannot return a valid response."""


class MalformedActionError(RuntimeError):
    """Raised when the policy output does not match the public action protocol."""

    def __init__(self, message: str, raw_output: str) -> None:
        super().__init__(message)
        self.raw_output = raw_output


def retrieval_payload(
    query: str,
    top_k: int,
    question: str | None = None,
    history: list[dict[str, object]] | None = None,
    reasoning: str | None = None,
) -> dict[str, object]:
    """Build the generic request, optionally adding contextual-retriever fields."""

    query = str(query).strip()
    if not query:
        raise ValueError("retrieval query must be non-empty")
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    payload: dict[str, object] = {
        "query": query,
        "top_k": top_k,
    }

    if question is not None:
        payload["question"] = str(question)
    if history is not None:
        payload["history"] = history
    if reasoning is not None:
        payload["reasoning"] = str(reasoning)

    return payload


def _parse_retrieval_response(raw: bytes) -> list[dict[str, Any]]:
    """Validate the HTTP retriever response without silently repairing it."""

    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RetrievalError("retriever returned invalid JSON") from exc

    if not isinstance(value, dict):
        raise RetrievalError("retriever response must be a JSON object")

    documents = value.get("documents")
    if not isinstance(documents, list):
        raise RetrievalError("retriever response must contain a documents list")

    validated: list[dict[str, Any]] = []
    for index, document in enumerate(documents):
        if not isinstance(document, dict):
            raise RetrievalError(
                f"retriever document {index} must be a JSON object"
            )
        validated.append(dict(document))

    return validated


def retrieve(
    url: str,
    query: str,
    top_k: int,
    question: str | None = None,
    history: list[dict[str, object]] | None = None,
    reasoning: str | None = None,
    *,
    timeout: float = 60.0,
    retries: int = 2,
    retry_backoff: float = 1.0,
) -> list[dict[str, Any]]:
    """Retrieve documents with bounded retries and strict response validation."""

    if timeout <= 0:
        raise ValueError("retriever timeout must be positive")
    if retries < 0:
        raise ValueError("retriever retries must be non-negative")
    if retry_backoff < 0:
        raise ValueError("retriever retry backoff must be non-negative")

    body = json.dumps(
        retrieval_payload(
            query,
            top_k,
            question,
            history,
            reasoning,
        ),
        ensure_ascii=False,
    ).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(
                request,
                timeout=timeout,
            ) as response:
                raw = response.read()

            return _parse_retrieval_response(raw)

        except (
            urllib.error.HTTPError,
            urllib.error.URLError,
            TimeoutError,
            OSError,
            RetrievalError,
        ) as exc:
            last_error = exc

            if attempt >= retries:
                break

            if retry_backoff:
                time.sleep(retry_backoff * (2**attempt))

    raise RetrievalError(
        f"retrieval failed after {retries + 1} attempt(s): {last_error}"
    ) from last_error


def document_text(document: dict[str, Any]) -> str:
    """Render a retrieved document into text for E5 passage scoring."""

    title = str(document.get("title", "")).strip()

    body = ""
    for key in ("text", "contents", "content", "passage", "snippet"):
        value = document.get(key)
        if value is not None and str(value).strip():
            body = str(value).strip()
            break

    if title and body:
        return f"{title}\n{body}"
    if body:
        return body
    if title:
        return title

    # Deterministic fallback for an unexpected but still valid document schema.
    return json.dumps(
        document,
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )


class RerouteScorer:
    """Score rerouting-query / passage similarity with E5-base-v2."""

    def __init__(
        self,
        model_name: str,
        device: str,
    ) -> None:
        import torch
        from transformers import AutoModel, AutoTokenizer

        self.torch = torch
        self.device = torch.device(device)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

    def _average_pool(
        self,
        last_hidden_state,
        attention_mask,
    ):
        masked_hidden = last_hidden_state.masked_fill(
            ~attention_mask[..., None].bool(),
            0.0,
        )

        denominator = attention_mask.sum(dim=1)[..., None].clamp(min=1)

        return masked_hidden.sum(dim=1) / denominator

    def _encode(
        self,
        texts: list[str],
        *,
        is_query: bool,
    ):
        if not texts:
            raise ValueError("cannot encode an empty text batch")

        prefix = "query: " if is_query else "passage: "
        prefixed = [prefix + str(text) for text in texts]

        batch = self.tokenizer(
            prefixed,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors="pt",
        ).to(self.device)

        with self.torch.no_grad():
            outputs = self.model(**batch)

            embeddings = self._average_pool(
                outputs.last_hidden_state,
                batch["attention_mask"],
            )

            embeddings = self.torch.nn.functional.normalize(
                embeddings,
                p=2,
                dim=1,
            )

        return embeddings

    def similarities(
        self,
        query: str,
        documents: list[dict[str, Any]],
    ) -> list[float]:
        """Return cosine similarities between one query and passages."""

        if not str(query).strip():
            raise ValueError("reroute query must be non-empty")

        if not documents:
            return []

        query_embedding = self._encode(
            [query],
            is_query=True,
        )

        passage_embeddings = self._encode(
            [document_text(document) for document in documents],
            is_query=False,
        )

        # Embeddings are L2-normalized, so dot product equals cosine similarity.
        scores = query_embedding @ passage_embeddings.T

        result = [
            float(score)
            for score in scores[0].detach().cpu().tolist()
        ]

        if len(result) != len(documents):
            raise RuntimeError(
                "reroute scorer returned a score count inconsistent with documents"
            )

        if any(not math.isfinite(score) for score in result):
            raise RuntimeError("reroute scorer returned a non-finite similarity")

        return result


def filter_previous_retrieval(
    query: str,
    documents: list[dict[str, Any]],
    scorer: RerouteScorer,
    threshold: float,
) -> list[dict[str, Any]]:
    """Filter only the immediately preceding retrieval for Reroute.

    Passages below the similarity threshold are removed. If every
    passage falls below the threshold, retain the highest-scoring one.
    """

    if not math.isfinite(threshold):
        raise ValueError("reroute threshold must be finite")

    if not documents:
        return []

    scores = scorer.similarities(
        query,
        documents,
    )

    if not scores:
        raise RuntimeError(
            "reroute scorer returned no scores for a non-empty document batch"
        )

    retained = [
        document
        for document, score in zip(documents, scores)
        if score >= threshold
    ]

    if retained:
        return retained

    # Preserve one passage when every score is below the threshold.
    best_index = max(
        range(len(scores)),
        key=lambda index: scores[index],
    )

    return [documents[best_index]]


def build_context(
    retrieval_batches: list[list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Flatten retrieval batches with deterministic deduplication."""

    context: list[dict[str, Any]] = []

    for batch in retrieval_batches:
        context = append_and_deduplicate(
            context,
            batch,
        )

    return context


def execute_search_action(
    action: Action,
    old_context: list[dict[str, Any]],
    retrieval_batches: list[list[dict[str, Any]]],
    retrieve_documents: Callable[[str], list[dict[str, Any]]],
    *,
    reroute_scorer: RerouteScorer | None,
    reroute_threshold: float,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    """Execute one search-control action transactionally.

    Continue:
        Preserve all evidence and append a new retrieval batch.

    Reroute:
        Filter only the immediately preceding retrieval batch,
        preserve all earlier evidence, then execute the rerouting
        query and append its retrieval result.

    Answer:
        Perform no retrieval.

    The shared retrieval-batch state is committed only after retrieval
    succeeds, avoiding a partially modified state after an HTTP failure.
    """

    if action.action == "Answer":
        return list(old_context), []

    if not action.parameter.strip():
        raise ValueError(f"{action.action} requires a non-empty retrieval query")

    next_batches = [
        list(batch)
        for batch in retrieval_batches
    ]

    if action.action == "Reroute":
        if reroute_scorer is None:
            raise ValueError(
                "Reroute requires an initialized reroute scorer"
            )

        # Only the immediately preceding retrieval batch is filtered.
        # Earlier retrieval batches remain unchanged.
        if next_batches:
            next_batches[-1] = filter_previous_retrieval(
                action.parameter,
                next_batches[-1],
                reroute_scorer,
                reroute_threshold,
            )

    # Continue and Reroute both issue the current retrieval query.
    documents = retrieve_documents(
        action.parameter
    )

    next_batches.append(
        list(documents)
    )

    new_context = build_context(
        next_batches
    )

    # Commit only after filtering + retrieval + context construction succeed.
    retrieval_batches[:] = next_batches

    return new_context, list(documents)


def _extract_answers(item: dict[str, Any]) -> list[str]:
    """Normalize common answer schemas without iterating over scalar strings."""

    raw_answers = item.get("answers")

    if raw_answers is None:
        raw_answers = item.get("answer", [])

    if isinstance(raw_answers, (str, int, float, bool)):
        values = [raw_answers]
    elif isinstance(raw_answers, list):
        values = raw_answers
    else:
        values = []

    return [
        str(answer).strip()
        for answer in values
        if str(answer).strip()
    ]


def _generate_action(
    model,
    tokenizer,
    sampling_params,
    state: SearchState,
) -> tuple[Action, str]:
    """Generate exactly one strict student continuation."""

    messages = render_student_prompt(
        state
    )

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    generated = model.generate(
        [prompt],
        sampling_params,
        use_tqdm=False,
    )

    if (
        not generated
        or not getattr(generated[0], "outputs", None)
        or not generated[0].outputs
    ):
        raise RuntimeError("vLLM returned no generation output")

    decoded = str(generated[0].outputs[0].text)

    try:
        action = Action.parse(decoded)
    except (TypeError, ValueError) as exc:
        raise MalformedActionError(
            "policy output does not match the required three-line action protocol",
            decoded,
        ) from exc

    return action, decoded


def _atomic_write_jsonl(
    output_path: str,
    rows: list[dict[str, Any]],
) -> None:
    """Write a checkpoint atomically so an interrupted write does not corrupt it."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_name(path.name + ".tmp")
    write_jsonl(
        str(temporary),
        rows,
    )
    os.replace(
        temporary,
        path,
    )


def _validate_args(args: argparse.Namespace) -> None:
    if args.top_k < 1:
        raise ValueError("--top-k must be at least 1")
    if args.max_search_steps < 1:
        raise ValueError("--max-search-steps must be at least 1")
    if args.temperature < 0:
        raise ValueError("--temperature must be non-negative")
    if args.tensor_parallel_size < 1:
        raise ValueError("--tensor-parallel-size must be at least 1")
    if not 0 < args.gpu_memory_utilization <= 1:
        raise ValueError("--gpu-memory-utilization must be in (0, 1]")
    if args.max_model_len is not None and args.max_model_len < 1:
        raise ValueError("--max-model-len must be positive")
    if args.retriever_timeout <= 0:
        raise ValueError("--retriever-timeout must be positive")
    if args.retriever_retries < 0:
        raise ValueError("--retriever-retries must be non-negative")
    if args.retriever_retry_backoff < 0:
        raise ValueError("--retriever-retry-backoff must be non-negative")
    if not math.isfinite(args.reroute_threshold):
        raise ValueError("--reroute-threshold must be finite")
    if args.checkpoint_every < 0:
        raise ValueError("--checkpoint-every must be non-negative")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model",
        required=True,
    )
    parser.add_argument(
        "--questions",
        required=True,
    )
    parser.add_argument(
        "--output",
        required=True,
    )
    parser.add_argument(
        "--retriever-url",
        required=True,
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--max-search-steps",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.6,
    )

    parser.add_argument(
        "--include-retrieval-context",
        action="store_true",
        help=(
            "send question, prior actions, and current Thought "
            "to a contextual retriever"
        ),
    )

    # Retriever robustness settings. Defaults preserve the same retrieval
    # semantics while preventing one transient HTTP failure from aborting a run.
    parser.add_argument(
        "--retriever-timeout",
        type=float,
        default=60.0,
        help="HTTP timeout in seconds for each retrieval attempt",
    )
    parser.add_argument(
        "--retriever-retries",
        type=int,
        default=2,
        help="number of retries after a failed retrieval attempt",
    )
    parser.add_argument(
        "--retriever-retry-backoff",
        type=float,
        default=1.0,
        help="base exponential backoff in seconds between retrieval attempts",
    )

    # vLLM settings.
    parser.add_argument(
        "--tensor-parallel-size",
        type=int,
        default=1,
        help="number of GPUs used for tensor parallelism",
    )
    parser.add_argument(
        "--gpu-memory-utilization",
        type=float,
        default=0.90,
        help="fraction of GPU memory available to the vLLM engine",
    )
    parser.add_argument(
        "--max-model-len",
        type=int,
        default=None,
        help="optional vLLM maximum model context length",
    )

    # Full BOUND rerouting settings.
    parser.add_argument(
        "--reroute-model",
        default="intfloat/e5-base-v2",
        help="embedding model used for Reroute passage filtering",
    )
    parser.add_argument(
        "--reroute-threshold",
        type=float,
        default=0.2,
        help="cosine-similarity threshold for Reroute filtering",
    )
    parser.add_argument(
        "--reroute-device",
        default="cpu",
        help=(
            "device for E5 reroute scoring, e.g. cpu, cuda, cuda:0; "
            "the scorer is loaded lazily on the first Reroute"
        ),
    )

    # Run-level robustness.
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=25,
        help=(
            "atomically save accumulated outputs every N questions; "
            "set 0 to disable intermediate checkpoints"
        ),
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="raise item-level runtime errors instead of recording and continuing",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _validate_args(args)

    from vllm import LLM, SamplingParams

    llm_kwargs: dict[str, Any] = {
        "model": args.model,
        "tensor_parallel_size": args.tensor_parallel_size,
        "gpu_memory_utilization": args.gpu_memory_utilization,
        "dtype": "auto",
    }

    if args.max_model_len is not None:
        llm_kwargs["max_model_len"] = args.max_model_len

    # Initialization failures are intentionally fatal: a run cannot proceed
    # meaningfully without a model/tokenizer.
    model = LLM(
        **llm_kwargs
    )

    tokenizer = model.get_tokenizer()

    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=1.0,
        max_tokens=256,
    )

    # Loaded only when the policy actually selects Reroute.
    reroute_scorer: RerouteScorer | None = None

    outputs: list[dict[str, Any]] = []

    for item_index, item in enumerate(
        read_jsonl(args.questions),
        start=1,
    ):
        if not isinstance(item, dict):
            item = {}

        item_id = item.get("id")
        trajectory_id = (
            str(item_id)
            if item_id is not None
            else f"item-{item_index}"
        )

        question = str(item.get("question", "")).strip()

        if not question:
            outputs.append(
                {
                    "id": item_id,
                    "trajectory_id": trajectory_id,
                    "question": "",
                    "prediction": "",
                    "outcome": {"success": False},
                    "termination_reason": "invalid_input",
                    "error": "question must be a non-empty string",
                    "steps": [],
                }
            )

            if args.checkpoint_every and item_index % args.checkpoint_every == 0:
                _atomic_write_jsonl(args.output, outputs)
            continue

        state = SearchState(
            question=question,
            history=[],
            context=[],
        )

        # Retrieval batches are stored separately because Reroute modifies
        # only the immediately preceding retrieval batch.
        retrieval_batches: list[list[dict[str, Any]]] = []

        final_answer = ""
        rollout_steps: list[dict[str, Any]] = []
        termination_reason = "max_steps"
        item_error: str | None = None

        try:
            for step_number in range(
                1,
                args.max_search_steps + 1,
            ):
                # Student-visible state before the current action.
                decision_state = state

                try:
                    action, raw_output = _generate_action(
                        model,
                        tokenizer,
                        sampling_params,
                        state,
                    )
                except MalformedActionError as exc:
                    rollout_steps.append(
                        {
                            "step": step_number,
                            "state": decision_state.to_dict(),
                            "raw_model_output": exc.raw_output,
                            "error": "malformed_action",
                        }
                    )
                    termination_reason = "malformed_action"
                    item_error = str(exc)
                    break
                except Exception as exc:
                    if args.fail_fast:
                        raise
                    rollout_steps.append(
                        {
                            "step": step_number,
                            "state": decision_state.to_dict(),
                            "error": "generation_error",
                            "error_message": f"{type(exc).__name__}: {exc}",
                        }
                    )
                    termination_reason = "generation_error"
                    item_error = f"{type(exc).__name__}: {exc}"
                    break

                history_before_current_action = list(
                    state.history
                )

                history = state.history + [
                    {
                        "step": step_number,
                        "action": action.action,
                        "parameter": action.parameter,
                    }
                ]

                if action.action == "Answer":
                    final_answer = action.parameter

                def retrieve_documents(query: str) -> list[dict[str, Any]]:
                    return retrieve(
                        args.retriever_url,
                        query,
                        args.top_k,
                        question=(
                            state.question
                            if args.include_retrieval_context
                            else None
                        ),
                        history=(
                            history_before_current_action
                            if args.include_retrieval_context
                            else None
                        ),
                        reasoning=(
                            action.thought
                            if args.include_retrieval_context
                            else None
                        ),
                        timeout=args.retriever_timeout,
                        retries=args.retriever_retries,
                        retry_backoff=args.retriever_retry_backoff,
                    )

                try:
                    # E5 is loaded only if Reroute is actually selected.
                    if (
                        action.action == "Reroute"
                        and reroute_scorer is None
                    ):
                        reroute_scorer = RerouteScorer(
                            model_name=args.reroute_model,
                            device=args.reroute_device,
                        )

                    new_context, documents = execute_search_action(
                        action,
                        state.context,
                        retrieval_batches,
                        retrieve_documents,
                        reroute_scorer=reroute_scorer,
                        reroute_threshold=args.reroute_threshold,
                    )

                except RetrievalError as exc:
                    if args.fail_fast:
                        raise
                    rollout_steps.append(
                        {
                            "step": step_number,
                            "state": decision_state.to_dict(),
                            "student_action": action.to_dict(),
                            "raw_model_output": raw_output,
                            "observation": [],
                            "error": "retrieval_error",
                            "error_message": str(exc),
                        }
                    )
                    termination_reason = "retrieval_error"
                    item_error = str(exc)
                    break

                except Exception as exc:
                    if args.fail_fast:
                        raise
                    rollout_steps.append(
                        {
                            "step": step_number,
                            "state": decision_state.to_dict(),
                            "student_action": action.to_dict(),
                            "raw_model_output": raw_output,
                            "observation": [],
                            "error": "execution_error",
                            "error_message": f"{type(exc).__name__}: {exc}",
                        }
                    )
                    termination_reason = "execution_error"
                    item_error = f"{type(exc).__name__}: {exc}"
                    break

                state = SearchState(
                    state.question,
                    history,
                    new_context,
                )

                rollout_steps.append(
                    {
                        "step": step_number,
                        "state": decision_state.to_dict(),
                        "student_action": action.to_dict(),
                        "observation": documents,
                    }
                )

                if action.action == "Answer":
                    termination_reason = "answer"
                    break

        except Exception as exc:
            # Optional strict debugging mode.
            if args.fail_fast:
                raise

            termination_reason = "unexpected_error"
            item_error = f"{type(exc).__name__}: {exc}"

        answers = _extract_answers(item)

        success = bool(final_answer) and any(
            normalize(final_answer)
            == normalize(answer)
            for answer in answers
        )

        output_record: dict[str, Any] = {
            "id": item_id,
            "trajectory_id": trajectory_id,
            "question": question,
            "prediction": final_answer,
            "outcome": {
                "success": success,
            },
            "termination_reason": termination_reason,
            "steps": rollout_steps,
        }

        if item_error is not None:
            output_record["error"] = item_error

        outputs.append(
            output_record
        )

        if (
            args.checkpoint_every
            and item_index % args.checkpoint_every == 0
        ):
            _atomic_write_jsonl(
                args.output,
                outputs,
            )

    _atomic_write_jsonl(
        args.output,
        outputs,
    )


if __name__ == "__main__":
    main()
