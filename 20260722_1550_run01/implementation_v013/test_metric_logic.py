import importlib.util
import math
from pathlib import Path


def load_module():
    path = Path(__file__).with_name("audit.py")
    spec = importlib.util.spec_from_file_location("v013_audit", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def fixed_rows(policy: str, k: int, hits: int, total: int = 120):
    return [
        {
            "query_id": f"q{index}",
            "policy": policy,
            "seed": None,
            "gold_rank": 1 if index < hits else k + 1,
            "k": k,
            "n": 370,
            "hit": index < hits,
            "target_reward": math.log2(370 / k) if index < hits else 0.0,
            "chance_probability": k / 370,
        }
        for index in range(total)
    ]


def test_fixed_k_reversal():
    module = load_module()
    k1 = fixed_rows("fk_1", 1, 72)
    k3 = fixed_rows("fk_3", 3, 94)
    m1 = module.aggregate_rows(k1)
    m3 = module.aggregate_rows(k3)
    assert m3["notebook_statistic"] > m1["notebook_statistic"]
    assert m3["defined_bor"] < m1["defined_bor"]


def test_stored_reward_recompute():
    module = load_module()
    rows = fixed_rows("fk_3", 3, 94)
    metrics = module.aggregate_rows(rows)
    assert abs(
        metrics["notebook_statistic"] - metrics["notebook_direct_recompute"]
    ) <= 1e-12
