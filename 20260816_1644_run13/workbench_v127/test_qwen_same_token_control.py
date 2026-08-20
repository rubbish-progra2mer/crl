"""Same-token intervention using locally cached Qwen3-0.6B activations.

Two distinct prompts are teacher-forced through the same response tokens.  The released
StateBridge alignment is then applied to each context-specific hidden-state sequence while
the reference token embeddings remain fixed.
"""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


WORKBENCH = Path(__file__).resolve().parent
REPOSITORY = WORKBENCH / "StateBridge"
MODEL_PATH = Path(
    r"C:\Users\g\.cache\huggingface\hub\models--Qwen--Qwen3-0.6B\snapshots\c1899de289a04d12100db370d81485cdf75e47ca"
)
sys.path.insert(0, str(REPOSITORY))

datasets_stub = types.ModuleType("datasets")
datasets_stub.load_dataset = lambda *_args, **_kwargs: (_ for _ in ()).throw(
    RuntimeError("Dataset loading is outside this local activation control.")
)
sys.modules.setdefault("datasets", datasets_stub)

from methods.state_bridge import StateBridge  # noqa: E402


def captured_message_states(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    prompt: str,
    message_ids: torch.Tensor,
) -> torch.Tensor:
    prompt_ids = tokenizer(prompt, return_tensors="pt", add_special_tokens=True).input_ids.to(model.device)
    full_ids = torch.cat([prompt_ids, message_ids], dim=1)
    captured: list[torch.Tensor] = []

    def hook(_module: torch.nn.Module, _inputs: tuple[torch.Tensor, ...], output: object) -> None:
        hidden = output[0] if isinstance(output, tuple) else output
        captured.append(hidden.detach())

    handle = model.model.layers[-1].register_forward_hook(hook)
    try:
        with torch.no_grad():
            model(input_ids=full_ids, use_cache=False)
    finally:
        handle.remove()
    all_states = captured[0]
    start = prompt_ids.shape[1] - 1
    end = start + message_ids.shape[1]
    return all_states[:, start:end, :]


def relative_change(first: torch.Tensor, second: torch.Tensor) -> float:
    return float(torch.linalg.norm(first.float() - second.float()) / torch.linalg.norm(first.float()))


def receiver_digit_probabilities(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    prefix: torch.Tensor,
) -> list[float]:
    receiver_prompt = (
        "A sender read one private digit from 0 to 3 before producing the latent prefix. "
        "Infer the digit from the prefix and return exactly that one digit.\nDigit:"
    )
    receiver_ids = tokenizer(
        receiver_prompt, return_tensors="pt", add_special_tokens=True
    ).input_ids.to(model.device)
    receiver_embeddings = model.get_input_embeddings()(receiver_ids)
    inputs = torch.cat([prefix.to(receiver_embeddings.dtype), receiver_embeddings], dim=1)
    attention_mask = torch.ones(inputs.shape[:2], dtype=torch.long, device=model.device)
    with torch.no_grad():
        logits = model(inputs_embeds=inputs, attention_mask=attention_mask, use_cache=False).logits[:, -1, :]
    digit_ids = [tokenizer(str(digit), add_special_tokens=False).input_ids for digit in range(4)]
    if any(len(ids) != 1 for ids in digit_ids):
        raise RuntimeError(f"Expected single-token digits, received {digit_ids}")
    candidate_logits = logits[0, [ids[0] for ids in digit_ids]]
    return torch.softmax(candidate_logits.float(), dim=0).cpu().tolist()


def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        local_files_only=True,
        dtype=torch.float16 if device.type == "cuda" else torch.float32,
    ).to(device)
    model.eval()

    message = (
        "First identify the relevant facts, compare the options, eliminate contradictions, "
        "and choose the best-supported answer."
    )
    message_ids = tokenizer(message, return_tensors="pt", add_special_tokens=False).input_ids.to(device)
    message_ids = message_ids[:, -16:]
    prompt_a = "Question: Which planet is closest to the Sun? Prepare a concise solution plan.\nPlan:"
    prompt_b = "Question: A patient has fever, cough, and a lobar infiltrate. Prepare a concise diagnostic plan.\nPlan:"
    hidden_a = captured_message_states(model, tokenizer, prompt_a, message_ids)
    hidden_b = captured_message_states(model, tokenizer, prompt_b, message_ids)

    bridge = StateBridge.__new__(StateBridge)
    bridge.device = device
    bridge.embedding_layer = model.get_input_embeddings()
    bridge.hidden_size = bridge.embedding_layer.embedding_dim
    bridge.dtype = bridge.embedding_layer.weight.dtype
    bridge.vocab_embeds = bridge.embedding_layer.weight.detach().float()
    bridge.target_norm = bridge.vocab_embeds.norm(dim=-1).mean().item()
    bridge.snap_ratio = 0.3
    bridge.adaptive_reg = 1e-3

    aligned_a = bridge._align_hidden_sequence(hidden_a, message_ids).detach()
    aligned_b = bridge._align_hidden_sequence(hidden_b, message_ids).detach()
    reference = bridge.embedding_layer(message_ids).detach()
    report = {
        "model": "Qwen3-0.6B local cache",
        "vocabulary_anchoring_ratio": 0.3,
        "message_token_count": int(message_ids.shape[1]),
        "raw_hidden_relative_change_between_contexts": relative_change(hidden_a, hidden_b),
        "aligned_relative_change_between_contexts": relative_change(aligned_a, aligned_b),
        "aligned_mean_cosine_to_token_embeddings_a": float(
            torch.nn.functional.cosine_similarity(aligned_a.float(), reference.float(), dim=-1).mean()
        ),
        "aligned_mean_cosine_to_token_embeddings_b": float(
            torch.nn.functional.cosine_similarity(aligned_b.float(), reference.float(), dim=-1).mean()
        ),
        "aligned_relative_error_to_token_embeddings_a": relative_change(reference, aligned_a),
        "aligned_relative_error_to_token_embeddings_b": relative_change(reference, aligned_b),
    }

    digit_rows = []
    for digit in range(4):
        sender_prompt = (
            f"Private digit: {digit}. Keep it in mind while preparing a generic reasoning plan.\nPlan:"
        )
        digit_hidden = captured_message_states(model, tokenizer, sender_prompt, message_ids)
        digit_prefix = bridge._align_hidden_sequence(digit_hidden, message_ids).detach()
        probabilities = receiver_digit_probabilities(model, tokenizer, digit_prefix)
        digit_rows.append(
            {
                "gold_digit": digit,
                "candidate_probabilities_0_to_3": probabilities,
                "predicted_digit": int(max(range(4), key=probabilities.__getitem__)),
            }
        )
    token_only_probabilities = receiver_digit_probabilities(model, tokenizer, reference)
    report["private_digit_receiver_control"] = {
        "aligned_prefix_rows": digit_rows,
        "aligned_prefix_accuracy": sum(
            int(row["gold_digit"] == row["predicted_digit"]) for row in digit_rows
        )
        / len(digit_rows),
        "token_only_candidate_probabilities_0_to_3": token_only_probabilities,
        "token_only_predicted_digit": int(
            max(range(4), key=token_only_probabilities.__getitem__)
        ),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
