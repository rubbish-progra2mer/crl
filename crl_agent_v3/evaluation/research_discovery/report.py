from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping


def render_markdown_report(report: Mapping[str, Any]) -> str:
    task = report["task"]
    lines = [
        "# CRL 时间截断研究发现评测",
        "",
        f"- 任务：`{task['task_id']}`",
        f"- 智能体子领域：{task['agent_subfield']}",
        f"- 研究问题：{task['research_question']}",
        f"- 合成夹具：`{str(task['synthetic_fixture']).lower()}`",
    ]
    if task["synthetic_notice"]:
        lines.append(f"- 声明：{task['synthetic_notice']}")
    lines.extend(
        [
            "",
            "自动指标只描述可观察记录；新颖性、意义和技术正确性只读取盲化专家标注。",
            "大语言模型裁判仅作辅助分析。本报告没有总分、排名或冠军。",
            "",
        ]
    )
    for system in report["systems"]:
        axes = system["axes"]
        lines.extend(
            [
                f"## 系统 `{system['system_id']}`（`{system['system_type']}`）",
                "",
                f"- 候选数：{system['candidate_count']}",
                f"- 配置 SHA-256：`{system['system_configuration_sha256']}`",
                f"- 输出 SHA-256：`{system['candidate_payload_sha256']}`",
                f"- 成本记录：{_json_inline(system['cost'])}",
                "",
                "### 探索与多样性",
                "",
                _metric_line("可见先行碰撞率", axes["exploration"]["visible_prior_collision_rate"]),
                _metric_line("最近先行审计覆盖率", axes["exploration"]["nearest_prior_audit_coverage"]),
                _metric_line("结构重复率", axes["diversity"]["structure_duplicate_rate"]),
                _metric_line("描述符覆盖率", axes["diversity"]["descriptor_coverage"]),
                "",
                "### 可证伪性",
                "",
                _metric_line("变化计算完整度", axes["falsifiability"]["changed_computation_completeness"]),
                _metric_line("反证条件完整度", axes["falsifiability"]["falsifier_completeness"]),
                _metric_line("杀手实验完整度", axes["falsifiability"]["killer_experiment_completeness"]),
                "",
                "### 实现与实证存活",
                "",
                _metric_line("实现转化率", axes["implementation"]["implementation_conversion_rate"]),
                _metric_line("早杀效率", axes["implementation"]["early_kill_efficiency"]),
                _metric_line(
                    "匹配强基线下实证存活率",
                    axes["empirical_survival"]["under_matched_strong_baselines"],
                ),
                (
                    "- 每个存活假设成本："
                    + _json_inline(
                        axes["empirical_survival"]["cost_per_surviving_hypothesis"]
                    )
                ),
                "",
                "### 留出机制与盲化专家标注",
                "",
                _metric_line(
                    "留出机制再发现率",
                    system["heldout_evaluation"]["mechanism_rediscovery"],
                ),
                _metric_line(
                    "简单文本相似度（独立披露）",
                    system["heldout_evaluation"]["simple_text_similarity"],
                ),
                _metric_line(
                    "专家新颖性",
                    system["expert_blind_assessment"]["novelty"],
                ),
                _metric_line(
                    "专家意义",
                    system["expert_blind_assessment"]["significance"],
                ),
                _metric_line(
                    "专家技术正确性",
                    system["expert_blind_assessment"]["technical_correctness"],
                ),
                (
                    "- 大语言模型辅助标注数："
                    f"{system['expert_blind_assessment']['llm_judge_auxiliary_annotation_count']}"
                    "（不进入主结论）"
                ),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_report_files(
    report: Mapping[str, Any], json_path: str | Path, markdown_path: str | Path
) -> None:
    json_target = Path(json_path)
    markdown_target = Path(markdown_path)
    if json_target == markdown_target:
        raise ValueError("JSON and Markdown report paths must differ")
    for target in (json_target, markdown_target):
        if target.exists():
            raise FileExistsError(f"report already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
    json_data = (
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    markdown_data = render_markdown_report(report).encode("utf-8")
    _exclusive_write(json_target, json_data)
    try:
        _exclusive_write(markdown_target, markdown_data)
    except Exception:
        json_target.unlink(missing_ok=True)
        raise


def _exclusive_write(path: Path, data: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
    except Exception:
        path.unlink(missing_ok=True)
        raise


def _metric_line(label: str, metric: Mapping[str, Any]) -> str:
    value = "未知" if metric["value"] is None else f"{metric['value']:.6g}"
    interval = metric["confidence_interval"]
    interval_text = ""
    if interval is not None:
        interval_text = (
            f"；{interval['confidence_level']:.1%} 自助法置信区间 "
            f"[{interval['lower']:.6g}, {interval['upper']:.6g}]，"
            f"抽样单位 `{interval['sampling_unit']}`"
        )
    eligibility_text = ""
    if "eligible_count" in metric:
        eligibility_text = (
            f"；合格数 {metric['eligible_count']} / 总体 {metric['population_count']}，"
            f"规则 `{metric['eligibility_rule']}`"
        )
    return (
        f"- {label}：{value}（分子 {metric['numerator']:.6g} / "
        f"分母 {metric['denominator']}；抽样单位 `{metric['sampling_unit']}`"
        f"{eligibility_text}{interval_text}）"
    )


def _json_inline(value: object) -> str:
    return "`" + json.dumps(value, ensure_ascii=False, sort_keys=True) + "`"
