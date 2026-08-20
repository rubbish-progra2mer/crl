"""The audited Poincaré-ball implementation, extracted for the §9 machine check.

These are the actual objects the audited pipeline computes with — the general
curvature-``c`` Poincaré geodesic distance and the exponential map at the
origin — extracted verbatim in their math from the audited system's own source
(first-party code; no third-party code is redistributed here). ``proposition.py``
checks the paper's closed form against ``geodesic_distance`` across multiple
curvatures and dimensionalities.
"""

import torch
from torch.autograd import Function


class Arcosh(Function):
    """Numerically stable inverse hyperbolic cosine (no NaN gradients at x=1)."""

    @staticmethod
    def forward(ctx, x, eps=1e-15):
        x = x.clamp(min=1.0 + eps)
        ctx.save_for_backward(x)
        return torch.log(x + torch.sqrt(x**2 - 1.0))

    @staticmethod
    def backward(ctx, grad_output):
        (x,) = ctx.saved_tensors
        return grad_output / torch.sqrt(x**2 - 1.0), None


class PoincareManifold:
    """The curvature-c Poincaré ball, with the shipped distance formula."""

    def __init__(self, curvature=1.0, eps=1e-5):
        self.c = curvature
        self.eps = eps

    def geodesic_distance(self, u: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        """d_c(u, v) = (1/sqrt(c)) * arcosh(1 + 2c|u-v|^2 / ((1-c|u|^2)(1-c|v|^2))).

        The denominator clamp (``min=self.eps``) is preserved from the shipped
        code; ``proposition.py`` shows it cannot rescue the no-op because on
        constant-radius inputs it is a function of the norm only, hence a
        constant.
        """
        sq_dist = torch.norm(u - v, p=2, dim=-1) ** 2
        u_norm_sq = torch.norm(u, p=2, dim=-1) ** 2
        v_norm_sq = torch.norm(v, p=2, dim=-1) ** 2

        u_denom = (1.0 - self.c * u_norm_sq).clamp(min=self.eps)
        v_denom = (1.0 - self.c * v_norm_sq).clamp(min=self.eps)

        delta = 1.0 + 2.0 * self.c * sq_dist / (u_denom * v_denom)
        return (1.0 / (self.c**0.5)) * Arcosh.apply(delta)


def poincare_exp_map(
    euclidean_z: torch.Tensor, manifold: PoincareManifold
) -> torch.Tensor:
    """Exponential map at the origin: exp_0(v) = tanh(sqrt(c)*|v|) * v / (sqrt(c)*|v|).

    Maps Euclidean vectors into the ball's interior (unit vectors land at
    tanh(sqrt(c))/sqrt(c)). Norms are compressed monotonically — which is
    exactly why, on inputs whose norms are ALL 1.0, every image lands at one
    radius and the hyperbolic structure carries nothing (the §9 proposition).
    """
    sqrt_c = manifold.c**0.5
    norm = torch.norm(euclidean_z, p=2, dim=-1, keepdim=True).clamp(min=1e-12)
    scale = torch.tanh(sqrt_c * norm) / (sqrt_c * norm)
    return scale * euclidean_z
