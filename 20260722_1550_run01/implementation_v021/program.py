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
    spec = importlib.util.spec_from_file_location("v021_base_v020_program", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load v020 program")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extended_feature_matrices(
    current: sparse.csr_matrix,
    reference: sparse.csr_matrix,
    numeric: sparse.csr_matrix,
    original: Callable[[sparse.csr_matrix, sparse.csr_matrix, sparse.csr_matrix], dict[str, sparse.csr_matrix]],
) -> dict[str, sparse.csr_matrix]:
    matrices = original(current, reference, numeric)
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
    base_path = here / "base_v020_program.py"
    config = json.loads(config_path_from_argv().read_text(encoding="utf-8"))
    if sha256_path(base_path) != config["base_v020_program_sha256"]:
        raise ValueError("v020 base program SHA mismatch")
    base = load_module(base_path)
    original_features = base.feature_matrices
    original_write_json = base.write_json

    base.METHODS = METHODS
    base.COMPARATORS = COMPARATORS
    base.feature_matrices = lambda current, reference, numeric: extended_feature_matrices(
        current, reference, numeric, original_features
    )

    def write_json(path: Path, value: Any) -> None:
        if isinstance(value, dict) and value.get("experiment_id") == "v020":
            value = {**value, "experiment_id": "v021"}
        original_write_json(path, value)

    base.write_json = write_json
    return int(base.main())


if __name__ == "__main__":
    raise SystemExit(main())
