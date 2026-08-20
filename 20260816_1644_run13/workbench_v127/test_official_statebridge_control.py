"""Run the released StateBridge alignment function under a fixed-token intervention."""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import torch


REPOSITORY = Path(__file__).resolve().parent / "StateBridge"
sys.path.insert(0, str(REPOSITORY))

# The alignment kernel does not use dataset loading, but the released module imports
# it eagerly.  Provide a fail-fast local stub instead of installing an unused package.
datasets_stub = types.ModuleType("datasets")


def unavailable_dataset(*_args: object, **_kwargs: object) -> None:
    raise RuntimeError("Dataset loading is outside this model-free control.")


datasets_stub.load_dataset = unavailable_dataset
sys.modules.setdefault("datasets", datasets_stub)

from methods.state_bridge import StateBridge  # noqa: E402


def make_bridge(embedding: torch.nn.Embedding, snap_ratio: float) -> StateBridge:
    bridge = StateBridge.__new__(StateBridge)
    bridge.device = torch.device("cpu")
    bridge.embedding_layer = embedding
    bridge.hidden_size = embedding.embedding_dim
    bridge.dtype = embedding.weight.dtype
    bridge.vocab_embeds = embedding.weight.detach().float()
    bridge.target_norm = bridge.vocab_embeds.norm(dim=-1).mean().item()
    bridge.snap_ratio = snap_ratio
    bridge.adaptive_reg = 1e-3
    return bridge


def relative_change(first: torch.Tensor, second: torch.Tensor) -> float:
    return float(torch.linalg.norm(first - second) / torch.linalg.norm(first))


def main() -> None:
    torch.manual_seed(20260817)
    k, d, vocabulary_size = 16, 128, 2048
    embedding = torch.nn.Embedding(vocabulary_size, d)
    token_ids = torch.arange(k).unsqueeze(0)
    token_embeddings = embedding(token_ids).detach()
    hidden_a = torch.randn(1, k, d)
    hidden_b = torch.randn(1, k, d)

    report = {}
    for snap_ratio in (0.0, 0.3):
        bridge = make_bridge(embedding, snap_ratio)
        aligned_a = bridge._align_hidden_sequence(hidden_a, token_ids).detach()
        aligned_b = bridge._align_hidden_sequence(hidden_b, token_ids).detach()
        cosine = torch.nn.functional.cosine_similarity(aligned_a, token_embeddings, dim=-1)
        report[str(snap_ratio)] = {
            "mean_cosine_to_fixed_token_embeddings": float(cosine.mean()),
            "relative_change_when_all_hidden_states_replaced": relative_change(aligned_a, aligned_b),
            "relative_error_to_raw_token_embeddings": relative_change(token_embeddings, aligned_a),
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
