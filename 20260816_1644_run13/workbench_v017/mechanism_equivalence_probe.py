from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.request
from collections import defaultdict
from pathlib import Path


PAIRS = [
    {
        "id": "same_verify_reconcile",
        "label": True,
        "a": "工具超时后先查询业务状态；只有确认原作用没有落地时才重试。",
        "b": "把不确定返回当成待对账事务，读取后置状态并在未提交分支重新发起调用。",
        "sig_a": {"operator": "postcondition_query", "timing": "before_retry", "decision": "retry_only_if_absent"},
        "sig_b": {"operator": "postcondition_query", "timing": "before_retry", "decision": "retry_only_if_absent"},
    },
    {
        "id": "diff_verify_timing",
        "label": False,
        "a": "工具超时后先查询业务状态；只有确认原作用没有落地时才重试。",
        "b": "工具超时后立即重试，然后查询业务状态并删除可能的重复结果。",
        "sig_a": {"operator": "postcondition_query", "timing": "before_retry", "decision": "retry_only_if_absent"},
        "sig_b": {"operator": "postcondition_query", "timing": "after_retry", "decision": "compensate_duplicate"},
    },
    {
        "id": "same_dependency_invalidation",
        "label": True,
        "a": "事实版本变化时沿派生依赖图撤销所有下游结论，只重算受影响节点。",
        "b": "为缓存结果保存读取谱系；源记录更新后做传递失效并局部重建物化结果。",
        "sig_a": {"operator": "transitive_dependency_invalidation", "trigger": "source_version_change", "scope": "descendants"},
        "sig_b": {"operator": "transitive_dependency_invalidation", "trigger": "source_version_change", "scope": "descendants"},
    },
    {
        "id": "diff_local_vs_cascade",
        "label": False,
        "a": "事实版本变化时沿派生依赖图撤销所有下游结论，只重算受影响节点。",
        "b": "事实版本变化时只删除直接缓存项，已有下游摘要继续保留直到自然过期。",
        "sig_a": {"operator": "transitive_dependency_invalidation", "trigger": "source_version_change", "scope": "descendants"},
        "sig_b": {"operator": "direct_cache_eviction", "trigger": "source_version_change", "scope": "direct_only"},
    },
    {
        "id": "same_lineage_collapse",
        "label": True,
        "a": "在共识前把引用同一原始证据的报告合并成一个独立根，再按根投票。",
        "b": "构造信息传播图并折叠共同祖先，避免转述链在聚合时被重复计票。",
        "sig_a": {"operator": "lineage_root_collapse", "timing": "before_aggregation", "unit": "independent_root"},
        "sig_b": {"operator": "lineage_root_collapse", "timing": "before_aggregation", "unit": "independent_root"},
    },
    {
        "id": "diff_source_counting",
        "label": False,
        "a": "在共识前把引用同一原始证据的报告合并成一个独立根，再按根投票。",
        "b": "保留每份报告并按发布者身份投票，只要发布者名称不同就视作独立来源。",
        "sig_a": {"operator": "lineage_root_collapse", "timing": "before_aggregation", "unit": "independent_root"},
        "sig_b": {"operator": "publisher_count", "timing": "during_aggregation", "unit": "surface_source"},
    },
    {
        "id": "same_active_constraint",
        "label": True,
        "a": "在每个高风险动作边界运行最小正反探针，确认相关约束仍能改变决策才允许执行。",
        "b": "把规则编译为动作前的成对干预测试；若开启与关闭规则不改变选择则阻断调用。",
        "sig_a": {"operator": "paired_constraint_intervention", "timing": "pre_action", "gate": "effect_required"},
        "sig_b": {"operator": "paired_constraint_intervention", "timing": "pre_action", "gate": "effect_required"},
    },
    {
        "id": "diff_prompt_restatement",
        "label": False,
        "a": "在每个高风险动作边界运行最小正反探针，确认相关约束仍能改变决策才允许执行。",
        "b": "在每个高风险动作前把相关约束重新附加到提示末尾，然后直接执行模型给出的动作。",
        "sig_a": {"operator": "paired_constraint_intervention", "timing": "pre_action", "gate": "effect_required"},
        "sig_b": {"operator": "prompt_restatement", "timing": "pre_action", "gate": "none"},
    },
    {
        "id": "same_trusted_render",
        "label": True,
        "a": "模型只能传递不透明结果句柄，可信运行时在目的地工具边界把句柄渲染成精确参数。",
        "b": "中间数据保持类型化引用；值的字节级展开由外壳在已授权接收端完成。",
        "sig_a": {"operator": "trusted_handle_render", "renderer": "runtime", "timing": "destination_boundary"},
        "sig_b": {"operator": "trusted_handle_render", "renderer": "runtime", "timing": "destination_boundary"},
    },
    {
        "id": "diff_model_render",
        "label": False,
        "a": "模型只能传递不透明结果句柄，可信运行时在目的地工具边界把句柄渲染成精确参数。",
        "b": "模型收到句柄对应的原始值后自行复制到下一个工具参数，运行时只检查 JSON 类型。",
        "sig_a": {"operator": "trusted_handle_render", "renderer": "runtime", "timing": "destination_boundary"},
        "sig_b": {"operator": "model_value_copy", "renderer": "model", "timing": "planning"},
    },
    {
        "id": "same_paired_fork",
        "label": True,
        "a": "从同一实时状态分叉，让两个策略共享前缀和控制条件，比较其条件成功差。",
        "b": "保存环境快照并对候选路由执行成对反事实重放，以同一起点估计处理效应。",
        "sig_a": {"operator": "paired_state_fork", "start": "shared_live_state", "estimand": "conditional_effect"},
        "sig_b": {"operator": "paired_state_fork", "start": "shared_live_state", "estimand": "conditional_effect"},
    },
    {
        "id": "diff_independent_rollout",
        "label": False,
        "a": "从同一实时状态分叉，让两个策略共享前缀和控制条件，比较其条件成功差。",
        "b": "分别从任务初始状态独立运行两个策略，再比较各自平均成功率。",
        "sig_a": {"operator": "paired_state_fork", "start": "shared_live_state", "estimand": "conditional_effect"},
        "sig_b": {"operator": "independent_rollout", "start": "separate_initial_state", "estimand": "marginal_difference"},
    },
    {
        "id": "same_exhaustive_coverage",
        "label": True,
        "a": "只有自动耗尽所有分页并取得完备性见证后，才允许输出‘没有记录’。",
        "b": "将否定回答绑定到查询覆盖证书；继续拉取游标直至数据源证明结果集封闭。",
        "sig_a": {"operator": "exhaustive_query_with_completeness_witness", "claim": "negative", "stop": "source_closed"},
        "sig_b": {"operator": "exhaustive_query_with_completeness_witness", "claim": "negative", "stop": "source_closed"},
    },
    {
        "id": "diff_first_page_negative",
        "label": False,
        "a": "只有自动耗尽所有分页并取得完备性见证后，才允许输出‘没有记录’。",
        "b": "读取第一页；若没有目标条目就输出‘没有记录’，同时注明可能还有后续页。",
        "sig_a": {"operator": "exhaustive_query_with_completeness_witness", "claim": "negative", "stop": "source_closed"},
        "sig_b": {"operator": "first_page_search", "claim": "hedged_negative", "stop": "page_end"},
    },
    {
        "id": "same_transactional_belief",
        "label": True,
        "a": "新记忆先进入快照隔离的暂存区，经证据、权限和有效性校验后才成为可行动信念。",
        "b": "把共享笔记写入候选事务；通过来源与授权检查的版本在提交点原子发布给下游。",
        "sig_a": {"operator": "staged_belief_commit", "visibility": "after_validation", "isolation": "snapshot"},
        "sig_b": {"operator": "staged_belief_commit", "visibility": "after_validation", "isolation": "snapshot"},
    },
    {
        "id": "diff_immediate_memory",
        "label": False,
        "a": "新记忆先进入快照隔离的暂存区，经证据、权限和有效性校验后才成为可行动信念。",
        "b": "新记忆立即写入共享存储供其他智能体读取，后台任务稍后补做证据和权限检查。",
        "sig_a": {"operator": "staged_belief_commit", "visibility": "after_validation", "isolation": "snapshot"},
        "sig_b": {"operator": "immediate_memory_publish", "visibility": "before_validation", "isolation": "none"},
    },
    {
        "id": "same_column_generation",
        "label": True,
        "a": "从小型受限主问题开始，用对偶价求最违反约束的配置列，迭代直到定价无改进。",
        "b": "不枚举指数级联合状态；交替求松弛线性规划和二进制定价子问题来补充活跃模式。",
        "sig_a": {"operator": "delayed_column_generation", "master": "restricted_lp", "oracle": "pricing"},
        "sig_b": {"operator": "delayed_column_generation", "master": "restricted_lp", "oracle": "pricing"},
    },
    {
        "id": "diff_random_configuration",
        "label": False,
        "a": "从小型受限主问题开始，用对偶价求最违反约束的配置列，迭代直到定价无改进。",
        "b": "从联合状态空间随机采样配置，固定样本后一次性求线性规划，不运行定价子问题。",
        "sig_a": {"operator": "delayed_column_generation", "master": "restricted_lp", "oracle": "pricing"},
        "sig_b": {"operator": "random_column_sampling", "master": "sampled_lp", "oracle": "none"},
    },
    {
        "id": "same_structural_delta",
        "label": True,
        "a": "将方法压成基线、信息源、算子、时机和决策边，再忽略模块名称比较规范图。",
        "b": "对候选计算去命名的变更签名，按其读取、变换与控制流的同构关系查询失败记忆。",
        "sig_a": {"operator": "name_quotiented_delta_graph", "fields": "information_operation_timing_decision", "match": "isomorphism"},
        "sig_b": {"operator": "name_quotiented_delta_graph", "fields": "information_operation_timing_decision", "match": "isomorphism"},
    },
    {
        "id": "diff_label_only_signature",
        "label": False,
        "a": "将方法压成基线、信息源、算子、时机和决策边，再忽略模块名称比较规范图。",
        "b": "抽取方法名称、应用领域和模块列表做关键词匹配，不记录信息流、执行时机或决策边。",
        "sig_a": {"operator": "name_quotiented_delta_graph", "fields": "information_operation_timing_decision", "match": "isomorphism"},
        "sig_b": {"operator": "keyword_module_match", "fields": "name_domain_modules", "match": "lexical_similarity"},
    },
]


def prompt_for(pair: dict, condition: str) -> list[dict]:
    if condition == "prose":
        payload = f"候选甲：{pair['a']}\n候选乙：{pair['b']}"
    elif condition == "delta_card":
        payload = (
            f"候选甲原文：{pair['a']}\n候选甲计算卡：{json.dumps(pair['sig_a'], ensure_ascii=False, sort_keys=True)}\n"
            f"候选乙原文：{pair['b']}\n候选乙计算卡：{json.dumps(pair['sig_b'], ensure_ascii=False, sort_keys=True)}"
        )
    elif condition == "self_normalize":
        payload = (
            "先分别把两个候选规范化为四个字段：读取的信息、核心算子、执行时机、决策规则。"
            "同义算子必须映射到同一抽象操作，不能逐字比较；不要把原文没有说明的差异臆造出来。"
            "规范化后再判断核心计算是否相同。\n"
            f"候选甲：{pair['a']}\n候选乙：{pair['b']}"
        )
    else:
        raise ValueError(f"unknown condition: {condition}")
    return [
        {
            "role": "system",
            "content": (
                "你是严格的方法审计器。判断两个候选是否改变了同一个核心计算。"
                "不要被领域、模块名或措辞迷惑；信息源、算子、执行时机或决策规则任一实质不同就判为不同。"
                "只输出 JSON：{\"same\":true} 或 {\"same\":false}。"
            ),
        },
        {"role": "user", "content": payload},
    ]


def parse_same(text: str) -> bool | None:
    matches = re.findall(r'\{\s*"same"\s*:\s*(true|false)\s*\}', text, flags=re.IGNORECASE)
    if not matches:
        return None
    return matches[-1].lower() == "true"


def call_ollama(model: str, messages: list[dict], seed: int, timeout: int) -> dict:
    request_body = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "format": {
            "type": "object",
            "properties": {"same": {"type": "boolean"}},
            "required": ["same"],
        },
        "options": {"temperature": 0.2, "seed": seed, "num_predict": 256},
    }
    encoded = json.dumps(request_body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=encoded,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    text = body.get("message", {}).get("content", "")
    return {
        "response": text,
        "parsed_same": parse_same(text),
        "latency_seconds": time.time() - started,
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "response_model": body.get("model"),
        "prompt_sha256": hashlib.sha256(json.dumps(messages, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest(),
    }


def summarize(rows: list[dict]) -> dict:
    summary: dict[str, dict] = {}
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["model"], row["condition"])].append(row)
    for (model, condition), group in sorted(grouped.items()):
        valid = [row for row in group if row["parsed_same"] is not None]
        correct = [row for row in valid if row["parsed_same"] == row["label"]]
        same_group = [row for row in valid if row["label"]]
        diff_group = [row for row in valid if not row["label"]]
        key = f"{model}|{condition}"
        summary[key] = {
            "calls": len(group),
            "valid": len(valid),
            "accuracy": len(correct) / len(valid) if valid else None,
            "same_recall": sum(row["parsed_same"] is True for row in same_group) / len(same_group) if same_group else None,
            "different_recall": sum(row["parsed_same"] is False for row in diff_group) / len(diff_group) if diff_group else None,
            "tokens": sum((row.get("prompt_eval_count") or 0) + (row.get("eval_count") or 0) for row in group),
        }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["qwen2.5:7b", "qwen3:8b"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[1701, 1702, 1703])
    parser.add_argument("--conditions", nargs="+", default=["prose", "delta_card"])
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows: list[dict] = []
    for model in args.models:
        for condition in args.conditions:
            for pair in PAIRS:
                for seed in args.seeds:
                    messages = prompt_for(pair, condition)
                    record = {
                        "model": model,
                        "condition": condition,
                        "pair_id": pair["id"],
                        "label": pair["label"],
                        "seed": seed,
                    }
                    try:
                        record.update(call_ollama(model, messages, seed, args.timeout))
                        record["error"] = None
                    except Exception as exc:  # preserve external runtime failure
                        record.update({"response": "", "parsed_same": None, "error": repr(exc)})
                    rows.append(record)
                    print(json.dumps({k: record.get(k) for k in ["model", "condition", "pair_id", "seed", "parsed_same", "label", "error"]}, ensure_ascii=False), flush=True)

    result = {
        "schema_version": 1,
        "pair_count": len(PAIRS),
        "models": args.models,
        "seeds": args.seeds,
        "summary": summarize(rows),
        "rows": rows,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
