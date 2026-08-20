from __future__ import annotations

import numpy as np
from scipy import sparse

from program import signed_channels


def test_signed_channels_preserve_direction_and_reconstruct() -> None:
    current = sparse.csr_matrix([[0.4, 0.0, 0.6, 0.2]])
    reference = sparse.csr_matrix([[0.1, 0.5, 0.6, 0.0]])
    novel, missing, absolute = signed_channels(current, reference)
    assert np.allclose(novel.toarray(), [[0.3, 0.0, 0.0, 0.2]])
    assert np.allclose(missing.toarray(), [[0.0, 0.5, 0.0, 0.0]])
    assert np.allclose(absolute.toarray(), novel.toarray() + missing.toarray())
    assert np.allclose(current.toarray() - reference.toarray(), novel.toarray() - missing.toarray())


def test_identical_vectors_have_zero_residuals() -> None:
    value = sparse.csr_matrix([[0.0, 0.2, 0.8]])
    novel, missing, absolute = signed_channels(value, value)
    assert novel.nnz == 0
    assert missing.nnz == 0
    assert absolute.nnz == 0
