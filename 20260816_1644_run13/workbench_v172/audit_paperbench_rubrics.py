from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = (
    Path(__file__).parent
    / "external"
    / "frontier-evals"
    / "project"
    / "paperbench"
    / "data"
    / "papers"
)

CATEGORIES = {
    "implementation_fidelity": re.compile(
        r"\b(implement(?:ed|ation)?|code|algorithm|architecture|equation|procedure|pipeline)\b",
        re.IGNORECASE,
    ),
    "published_ablation": re.compile(r"\bablation(?:s| study| studies)?\b", re.IGNORECASE),
    "published_robustness_or_generalization": re.compile(
        r"\b(robust(?:ness)?|generalization|generalisation|out-of-distribution|ood)\b",
        re.IGNORECASE,
    ),
    "explicit_unseen_or_held_out": re.compile(
        r"\b(unseen|held[- ]out|counterfactual|intervention|metamorphic|hidden test)\b",
        re.IGNORECASE,
    ),
    "sensitivity_or_perturbation": re.compile(
        r"\b(sensitivit(?:y|ies)|perturb(?:ation|ations|ed)?)\b",
        re.IGNORECASE,
    ),
}


def flatten(node: dict, paper: str, depth: int = 0) -> list[dict]:
    requirement = str(node.get("requirements", ""))
    children = node.get("sub_tasks") or []
    current = {
        "paper": paper,
        "id": str(node.get("id", "")),
        "depth": depth,
        "weight": node.get("weight"),
        "is_leaf": not children,
        "requirement": requirement,
    }
    rows = [current]
    for child in children:
        rows.extend(flatten(child, paper, depth + 1))
    return rows


def main() -> None:
    rubric_paths = sorted(ROOT.glob("*/rubric.json"))
    rows: list[dict] = []
    for path in rubric_paths:
        with path.open("r", encoding="utf-8") as handle:
            rows.extend(flatten(json.load(handle), path.parent.name))

    leaves = [row for row in rows if row["is_leaf"]]
    category_summary: dict[str, dict] = {}
    for name, pattern in CATEGORIES.items():
        hits = [row for row in rows if pattern.search(row["requirement"])]
        leaf_hits = [row for row in leaves if pattern.search(row["requirement"])]
        category_summary[name] = {
            "node_hits": len(hits),
            "leaf_hits": len(leaf_hits),
            "papers_with_hits": sorted({row["paper"] for row in hits}),
            "examples": [
                {
                    "paper": row["paper"],
                    "id": row["id"],
                    "requirement": row["requirement"],
                }
                for row in hits[:8]
            ],
        }

    paper_node_counts = Counter(row["paper"] for row in rows)
    paper_leaf_counts = Counter(row["paper"] for row in leaves)
    report = {
        "source_root": str(ROOT),
        "rubric_files": len(rubric_paths),
        "total_nodes": len(rows),
        "leaf_nodes": len(leaves),
        "per_paper": {
            paper: {
                "nodes": paper_node_counts[paper],
                "leaves": paper_leaf_counts[paper],
            }
            for paper in sorted(paper_node_counts)
        },
        "categories": category_summary,
        "interpretation_boundary": (
            "This is a lexical audit of explicit rubric text. Absence of a term does not prove "
            "absence of an equivalent judgment performed implicitly by an LLM judge."
        ),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
