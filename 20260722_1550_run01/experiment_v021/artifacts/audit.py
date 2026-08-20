from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Callable

from scipy import sparse


METHODS = (
    "text",
    "reference_concat",
    "absolute_delta",
    "rced",
    "triple_text",
    "duplicated_absolute",
    "signed_residual",
)
COMPARATORS = METHODS[:-1]


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("v021_base_v020_audit", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load v020 audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extended_feature_matrices(
    examples: list[dict[str, Any]],
    vectorizer: Any,
    scaler: Any,
    original: Callable[[list[dict[str, Any]], Any, Any], dict[str, sparse.csr_matrix]],
) -> dict[str, sparse.csr_matrix]:
    matrices = original(examples, vectorizer, scaler)
    current = vectorizer.transform([item["text"] for item in examples]).tocsr()
    reference = vectorizer.transform(
        [item["reference_text"] for item in examples]
    ).tocsr()
    absolute = (current - reference).tocsr()
    absolute.data = abs(absolute.data)
    absolute.eliminate_zeros()
    matrices["triple_text"] = sparse.hstack([current, current, current], format="csr")
    matrices["duplicated_absolute"] = sparse.hstack(
        [current, absolute, absolute], format="csr"
    )
    return matrices


def config_path_from_argv() -> Path:
    index = sys.argv.index("--config")
    return Path(sys.argv[index + 1])


def main() -> int:
    here = Path(__file__).resolve().parent
    base_path = here / "base_v020_audit.py"
    config = json.loads(config_path_from_argv().read_text(encoding="utf-8"))
    if sha256_path(base_path) != config["base_v020_audit_sha256"]:
        raise ValueError("v020 base audit SHA mismatch")
    base = load_module(base_path)
    original_features = base.feature_matrices
    base.METHODS = METHODS
    base.COMPARATORS = COMPARATORS
    base.feature_matrices = lambda examples, vectorizer, scaler: extended_feature_matrices(
        examples, vectorizer, scaler, original_features
    )
    return int(base.main())


if __name__ == "__main__":
    raise SystemExit(main())
