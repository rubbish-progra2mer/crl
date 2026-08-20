"""Test whether per-message whitening/Procrustes retains sender-state information.

This is a synthetic, model-free audit of the released StateBridge alignment equations.
For each fixed reference-embedding sequence E, independent hidden-state sequences H are
aligned with the same implementation order as methods/state_bridge.py.  If the output
contains information beyond token identity, changing H while holding E fixed should
materially change the aligned prefix.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import torch


@dataclass
class Result:
    k: int
    d: int
    reg: float
    mean_cosine_to_reference: float
    relative_error_to_reference: float
    relative_change_across_hidden_states: float
    nearest_reference_identity_rate: float
    whitened_gram_relative_gap: float


def symmetric_power(matrix: torch.Tensor, power: float, eps: float = 1e-6) -> torch.Tensor:
    matrix = (matrix + matrix.T) * 0.5
    values, vectors = torch.linalg.eigh(matrix)
    values = values.clamp_min(eps).pow(power)
    return (vectors * values.unsqueeze(0)) @ vectors.T


def align(hidden: torch.Tensor, reference: torch.Tensor, reg: float) -> tuple[torch.Tensor, torch.Tensor]:
    n, d = hidden.shape
    hidden_centered = hidden - hidden.mean(dim=0, keepdim=True)
    reference_centered = reference - reference.mean(dim=0, keepdim=True)
    identity = torch.eye(d, dtype=hidden.dtype, device=hidden.device)
    hidden_cov = hidden_centered.T @ hidden_centered / n + reg * identity
    reference_cov = reference_centered.T @ reference_centered / n + reg * identity
    hidden_white = hidden_centered @ symmetric_power(hidden_cov, -0.5)
    reference_white = reference_centered @ symmetric_power(reference_cov, -0.5)
    left, _, right_t = torch.linalg.svd(hidden_white.T @ reference_white, full_matrices=False)
    rotation = left @ right_t
    if torch.det(rotation) < 0:
        left[:, -1] *= -1
        rotation = left @ right_t
    aligned = hidden_white @ rotation @ symmetric_power(reference_cov, 0.5)
    aligned += reference.mean(dim=0, keepdim=True)
    gram_gap = torch.linalg.norm(hidden_white @ hidden_white.T - reference_white @ reference_white.T)
    gram_gap /= torch.linalg.norm(reference_white @ reference_white.T).clamp_min(1e-12)
    return aligned, gram_gap


def audit(k: int, d: int, reg: float, seed: int) -> Result:
    generator = torch.Generator().manual_seed(seed)
    reference = torch.randn(k, d, generator=generator, dtype=torch.float64)
    hidden_a = torch.randn(k, d, generator=generator, dtype=torch.float64)
    hidden_b = torch.randn(k, d, generator=generator, dtype=torch.float64)

    aligned_a, gram_gap_a = align(hidden_a, reference, reg)
    aligned_b, gram_gap_b = align(hidden_b, reference, reg)

    cosines = torch.nn.functional.cosine_similarity(aligned_a, reference, dim=-1)
    relative_error = torch.linalg.norm(aligned_a - reference) / torch.linalg.norm(reference)
    hidden_sensitivity = torch.linalg.norm(aligned_a - aligned_b) / torch.linalg.norm(aligned_a)
    similarities = torch.nn.functional.normalize(aligned_a, dim=-1) @ torch.nn.functional.normalize(
        reference, dim=-1
    ).T
    identity_rate = (similarities.argmax(dim=-1) == torch.arange(k)).double().mean()

    return Result(
        k=k,
        d=d,
        reg=reg,
        mean_cosine_to_reference=float(cosines.mean()),
        relative_error_to_reference=float(relative_error),
        relative_change_across_hidden_states=float(hidden_sensitivity),
        nearest_reference_identity_rate=float(identity_rate),
        whitened_gram_relative_gap=float((gram_gap_a + gram_gap_b) / 2),
    )


def main() -> None:
    results = []
    for k, d in ((8, 64), (16, 128), (32, 256), (64, 512)):
        for reg in (1e-1, 1e-2, 1e-3, 1e-4):
            results.append(asdict(audit(k, d, reg, seed=20260817 + k + d)))
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
