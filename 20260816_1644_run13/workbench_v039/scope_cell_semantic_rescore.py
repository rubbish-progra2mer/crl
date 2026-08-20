import json
from itertools import product
from pathlib import Path


HERE = Path(__file__).parent
SOURCE = HERE / "scope_cell_synthesis_qwen2_5_7b.json"
OUT = HERE / "scope_cell_synthesis_semantic_rescore.json"
ANY = "任意"
UNKNOWN = "未报告"


def expand_cell(cell, dimensions):
    values = []
    for dim, levels in dimensions.items():
        value = cell["conditions"].get(dim, UNKNOWN)
        if value == ANY:
            values.append(list(levels))
        else:
            values.append([value])
    expanded = []
    for combination in product(*values):
        expanded.append(
            {
                "state": tuple(zip(dimensions, combination)),
                "direction": cell.get("direction", ""),
                "status": cell.get("status", ""),
                "sources": tuple(sorted(cell.get("source_ids", []))),
            }
        )
    return expanded


def semantic_items(output, dimensions):
    items = []
    for cell in output.get("cells", []):
        items.extend(expand_cell(cell, dimensions))
    return items


def semantic_key(item):
    return item["state"], item["direction"], item["status"]


def source_coverage(output, gold_atoms, dimensions):
    predicted = semantic_items(output, dimensions)
    covered = 0
    for atom in gold_atoms:
        state = tuple((dim, atom["conditions"].get(dim, UNKNOWN)) for dim in dimensions)
        matches = [
            item
            for item in predicted
            if item["state"] == state
            and atom["source_id"] in item["sources"]
            and (
                item["direction"] == atom["direction"]
                or (item["direction"] == "混合" and item["status"] == "未解决")
            )
        ]
        covered += bool(matches)
    return covered / len(gold_atoms) if gold_atoms else 1.0


def score(output, gold, gold_atoms, dimensions):
    pred_items = semantic_items(output, dimensions)
    gold_items = semantic_items(gold, dimensions)
    pred_set = {semantic_key(item) for item in pred_items}
    gold_set = {semantic_key(item) for item in gold_items}
    overlap = len(pred_set & gold_set)
    precision = overlap / len(pred_set) if pred_set else 0.0
    recall = overlap / len(gold_set) if gold_set else 1.0
    exact_semantics = pred_set == gold_set
    global_safe = output.get("global_claim") == gold.get("global_claim")
    evidence_coverage = source_coverage(output, gold_atoms, dimensions)
    return {
        "semantic_precision": precision,
        "semantic_recall": recall,
        "exact_semantics": exact_semantics,
        "global_safe": global_safe,
        "evidence_coverage": evidence_coverage,
        "cell_count": len(output.get("cells", [])),
        "gold_cell_count": len(gold.get("cells", [])),
        "compactness_ratio": len(gold.get("cells", [])) / len(output.get("cells", [])) if output.get("cells") else 0.0,
        "semantic_full_success": exact_semantics and global_safe and evidence_coverage == 1.0,
    }


def summarize(records):
    strategies = ["direct", "strong_two_stage", "auto_partition", "oracle_partition"]
    summary = {}
    for strategy in strategies:
        scores = [record["strategies"][strategy] for record in records]
        summary[strategy] = {
            "tasks": len(scores),
            "semantic_full_success": sum(score["semantic_full_success"] for score in scores),
            "exact_semantics": sum(score["exact_semantics"] for score in scores),
            "global_safe": sum(score["global_safe"] for score in scores),
            "mean_semantic_precision": sum(score["semantic_precision"] for score in scores) / len(scores),
            "mean_semantic_recall": sum(score["semantic_recall"] for score in scores) / len(scores),
            "mean_evidence_coverage": sum(score["evidence_coverage"] for score in scores) / len(scores),
            "mean_compactness_ratio": sum(score["compactness_ratio"] for score in scores) / len(scores),
        }
    return summary


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = []
    for record in data["records"]:
        strategies = {}
        gold = record["gold_partition"]
        for name, value in record["strategies"].items():
            strategies[name] = score(value["output"], gold, record["gold_atoms"], record["dimensions"])
        records.append({"task_id": record["task_id"], "strategies": strategies})
    result = {
        "source": SOURCE.name,
        "model_rerun": False,
        "scoring_change": "将任意范围展开为原子状态，允许语义等价但粒度不同的分割；证据来源覆盖与紧凑度分开计分。",
        "summary": summarize(records),
        "records": records,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
