from __future__ import annotations

import numpy as np
from scipy import sparse

from program import extended_feature_matrices


def test_capacity_controls_match_candidate_dimension_and_information() -> None:
    current = sparse.csr_matrix([[0.4, 0.0, 0.6]])
    reference = sparse.csr_matrix([[0.1, 0.5, 0.6]])
    numeric = sparse.csr_matrix([[1.0]])

    def original(x, r, n):
        return {"text": x, "signed_residual": sparse.hstack([x, x, r], format="csr")}

    matrices = extended_feature_matrices(current, reference, numeric, original)
    assert matrices["triple_text"].shape[1] == 9
    assert matrices["duplicated_absolute"].shape[1] == 9
    assert matrices["signed_residual"].shape[1] == 9
    assert np.allclose(
        matrices["triple_text"].toarray(),
        np.hstack([current.toarray()] * 3),
    )
    absolute = np.abs(current.toarray() - reference.toarray())
    assert np.allclose(
        matrices["duplicated_absolute"].toarray(),
        np.hstack([current.toarray(), absolute, absolute]),
    )
