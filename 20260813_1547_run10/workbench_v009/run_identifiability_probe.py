from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "identifiability_probe_results.json"
REPORT = ROOT / "identifiability_probe_report.md"


def canonical_partition(labels: tuple[int, ...]) -> tuple[int, ...]:
    remap: dict[int, int] = {}
    next_label = 0
    canonical: list[int] = []
    for label in labels:
        if label not in remap:
            remap[label] = next_label
            next_label += 1
        canonical.append(remap[label])
    return tuple(canonical)


def partitions(n: int) -> Iterable[tuple[int, ...]]:
    if n <= 0:
        return
    labels = [0] * n

    def visit(index: int, maximum: int) -> Iterable[tuple[int, ...]]:
        if index == n:
            yield tuple(labels)
            return
        for label in range(maximum + 2):
            labels[index] = label
            yield from visit(index + 1, max(maximum, label))

    yield from visit(1, 0)


def satisfies(
    partition: tuple[int, ...],
    must_link: set[tuple[int, int]],
    must_separate: set[tuple[int, int]],
) -> bool:
    for left, right in must_link:
        if partition[left] != partition[right]:
            return False
    for left, right in must_separate:
        if partition[left] == partition[right]:
            return False
    return True


def feasible_root_counts(
    n: int,
    must_link: set[tuple[int, int]] | None = None,
    must_separate: set[tuple[int, int]] | None = None,
) -> list[int]:
    links = must_link or set()
    separates = must_separate or set()
    counts = {
        len(set(partition))
        for partition in partitions(n)
        if satisfies(partition, links, separates)
    }
    return sorted(counts)


@dataclass(frozen=True)
class ConstraintCase:
    case_id: str
    n: int
    must_link: frozenset[tuple[int, int]] = frozenset()
    must_separate: frozenset[tuple[int, int]] = frozenset()

    def evaluate(self) -> dict[str, object]:
        counts = feasible_root_counts(
            self.n,
            set(self.must_link),
            set(self.must_separate),
        )
        return {
            "case_id": self.case_id,
            "document_count": self.n,
            "must_link": sorted([list(edge) for edge in self.must_link]),
            "must_separate": sorted([list(edge) for edge in self.must_separate]),
            "feasible_root_counts": counts,
            "lower_root_bound": min(counts),
            "upper_root_bound": max(counts),
            "safe_to_claim_two_independent_roots": min(counts) >= 2,
        }


def main() -> None:
    cases = [
        ConstraintCase("two-docs-no-provenance", 2),
        ConstraintCase("eight-docs-no-provenance", 8),
        ConstraintCase(
            "eight-docs-explicit-same-root",
            8,
            must_link=frozenset((0, index) for index in range(1, 8)),
        ),
        ConstraintCase(
            "eight-docs-one-proven-independent-pair",
            8,
            must_separate=frozenset({(0, 1)}),
        ),
        ConstraintCase(
            "eight-docs-independent-chain-only",
            8,
            must_separate=frozenset((index, index + 1) for index in range(7)),
        ),
        ConstraintCase(
            "eight-docs-four-way-independent-clique",
            8,
            must_separate=frozenset(
                (left, right)
                for left in range(4)
                for right in range(left + 1, 4)
            ),
        ),
    ]
    case_results = [case.evaluate() for case in cases]

    observable_payload = {
        "claim": "Company N won the 2025 contract.",
        "documents": [
            {
                "url": "https://source-a.example/report",
                "published": "2025-04-03",
                "text": "Company N won the 2025 contract.",
            },
            {
                "url": "https://source-b.example/story",
                "published": "2025-04-04",
                "text": "The 2025 contract was awarded to Company N.",
            },
        ],
        "explicit_citation_edges": [],
    }
    indistinguishable_worlds = [
        {
            "world_id": "hidden-copy-world",
            "observable_payload_sharessame": True,
            "latent_root_partition": [0, 0],
            "true_root_resilience": 1,
            "stop_if_resilience_gt_1": False,
        },
        {
            "world_id": "hidden-independent-world",
            "observable_payload_sharessame": True,
            "latent_root_partition": [0, 1],
            "true_root_resilience": 2,
            "stop_if_resilience_gt_1": True,
        },
    ]

    output = {
        "artifact_class": "scratch_identifiability_killer_probe",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "hypothesis_id": "h-v009-001",
        "pre_registered_decision_rule": (
            "A hard two-root stopping certificate is sound only when every provenance "
            "partition consistent with visible constraints contains at least two roots."
        ),
        "observable_payload": observable_payload,
        "observationally_indistinguishable_worlds": indistinguishable_worlds,
        "constraint_cases": case_results,
        "derived_findings": {
            "non_identifiability_witness": (
                "The same observable payload admits a one-root copy world and a two-root "
                "independent world, but rho>1 differs between them."
            ),
            "no_constraint_lower_bound": next(
                item["lower_root_bound"]
                for item in case_results
                if item["case_id"] == "eight-docs-no-provenance"
            ),
            "chain_is_not_four_independent_roots": next(
                item["lower_root_bound"]
                for item in case_results
                if item["case_id"] == "eight-docs-independent-chain-only"
            ),
            "four_way_clique_lower_bound": next(
                item["lower_root_bound"]
                for item in case_results
                if item["case_id"] == "eight-docs-four-way-independent-clique"
            ),
        },
        "interpretation_boundary": (
            "This probe is combinatorial, not an end-to-end LLM result. It falsifies a "
            "distribution-free hard certificate from ordinary visible documents. It does "
            "not rule out probabilistic source-dependence estimation under explicit assumptions."
        ),
    }
    OUTPUT.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    rows = []
    for item in case_results:
        rows.append(
            "| {case_id} | {document_count} | {lower_root_bound} | "
            "{upper_root_bound} | {safe} |".format(
                case_id=item["case_id"],
                document_count=item["document_count"],
                lower_root_bound=item["lower_root_bound"],
                upper_root_bound=item["upper_root_bound"],
                safe="是" if item["safe_to_claim_two_independent_roots"] else "否",
            )
        )
    report = "\n".join(
        [
            "# v009 证据根不可识别性杀手检查",
            "",
            "## 结论",
            "",
            "普通网页可见量不足以支持分布无关的硬性‘两个独立记录根’证书。存在两个观测完全相同的潜在世界：一个是两文档同根转载，另一个是两个独立生成源；前者根韧性为 1，后者为 2。任何只读取相同观测的控制器都不能同时给出正确的硬停止决定。",
            "",
            "若把所有与可见约束相容的来源分区都纳入可能世界，八篇文档且无来源约束时，独立根数的安全下界仍为 1。只有可审计的 `must-separate`（必异根）证据才能提高下界；同根线索和近重复聚类只能合并，不能证明独立。",
            "",
            "## 枚举结果",
            "",
            "| 条件 | 文档数 | 安全下界 | 可能上界 | 可硬证至少两根 |",
            "|---|---:|---:|---:|---|",
            *rows,
            "",
            "## 对 h-v009-001 的影响",
            "",
            "- 若使用单一点估计谱系，所谓证书退化为经典的概率复制检测或聚类特征，不能声称硬复制不变性。",
            "- 若使用最坏可能世界保证而没有必异根证据，方法安全但在一般网页上几乎总是弃答。",
            "- 若引入显式必异根证明，真正的新计算应转向‘如何检索和验证独立生成证明’，而不是数据库最小删除割。该问题仍需新的先行审计。",
            "",
            "本检查只反证分布无关硬证书，不排除在明确生成模型和校准假设下做概率化来源依赖估计。",
            "",
        ]
    )
    REPORT.write_text(report, encoding="utf-8", newline="\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
