import json
import re
import time
import urllib.request
from collections import defaultdict
from pathlib import Path


MODEL = "qwen2.5:7b"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
OUT = Path(__file__).with_name("scope_cell_synthesis_qwen2_5_7b.json")
UNKNOWN = "未报告"
ANY = "任意"


TASKS = [
    {
        "id": "crop_xor",
        "dimensions": {"土壤": ["黏土", "沙土"], "降雨": ["低", "高"]},
        "studies": [
            ["S1", "在黏土且降雨低的地块，处理剂使产量上升。"],
            ["S2", "在沙土且降雨低的地块，处理剂使产量下降。"],
            ["S3", "在黏土且降雨高的地块，处理剂使产量下降。"],
            ["S4", "在沙土且降雨高的地块，处理剂使产量上升。"],
        ],
        "atoms": [
            ["S1", {"土壤": "黏土", "降雨": "低"}, "上升"],
            ["S2", {"土壤": "沙土", "降雨": "低"}, "下降"],
            ["S3", {"土壤": "黏土", "降雨": "高"}, "下降"],
            ["S4", {"土壤": "沙土", "降雨": "高"}, "上升"],
        ],
    },
    {
        "id": "latency_by_load",
        "dimensions": {"部署": ["边缘", "云端"], "负载": ["突发", "稳定"]},
        "studies": [
            ["S1", "边缘部署在突发负载下使尾延迟上升。"],
            ["S2", "云端部署在突发负载下也使尾延迟上升。"],
            ["S3", "边缘部署在稳定负载下使尾延迟下降。"],
            ["S4", "云端部署在稳定负载下也使尾延迟下降。"],
        ],
        "atoms": [
            ["S1", {"部署": "边缘", "负载": "突发"}, "上升"],
            ["S2", {"部署": "云端", "负载": "突发"}, "上升"],
            ["S3", {"部署": "边缘", "负载": "稳定"}, "下降"],
            ["S4", {"部署": "云端", "负载": "稳定"}, "下降"],
        ],
    },
    {
        "id": "battery_by_chemistry",
        "dimensions": {"化学体系": ["磷酸铁锂", "三元锂"], "温度": ["低温", "常温"]},
        "studies": [
            ["S1", "磷酸铁锂电芯在低温下循环寿命上升。"],
            ["S2", "磷酸铁锂电芯在常温下循环寿命上升。"],
            ["S3", "三元锂电芯在低温下循环寿命下降。"],
            ["S4", "三元锂电芯在常温下循环寿命下降。"],
        ],
        "atoms": [
            ["S1", {"化学体系": "磷酸铁锂", "温度": "低温"}, "上升"],
            ["S2", {"化学体系": "磷酸铁锂", "温度": "常温"}, "上升"],
            ["S3", {"化学体系": "三元锂", "温度": "低温"}, "下降"],
            ["S4", {"化学体系": "三元锂", "温度": "常温"}, "下降"],
        ],
    },
    {
        "id": "education_unresolved",
        "dimensions": {"学习方式": ["小组", "独立"], "基础": ["初学", "进阶"]},
        "studies": [
            ["S1", "小组学习对初学者使测验成绩上升。"],
            ["S2", "另一项相同设置的研究报告：小组学习对初学者使测验成绩下降。"],
            ["S3", "小组学习对进阶者使测验成绩上升。"],
            ["S4", "独立学习对初学者使测验成绩不变。"],
            ["S5", "独立学习对进阶者使测验成绩不变。"],
        ],
        "atoms": [
            ["S1", {"学习方式": "小组", "基础": "初学"}, "上升"],
            ["S2", {"学习方式": "小组", "基础": "初学"}, "下降"],
            ["S3", {"学习方式": "小组", "基础": "进阶"}, "上升"],
            ["S4", {"学习方式": "独立", "基础": "初学"}, "不变"],
            ["S5", {"学习方式": "独立", "基础": "进阶"}, "不变"],
        ],
    },
    {
        "id": "ecology_sparse",
        "dimensions": {"生境": ["城市", "乡村"], "季节": ["旱季", "雨季"]},
        "studies": [
            ["S1", "在城市旱季，干预使物种丰富度上升。"],
            ["S2", "在乡村旱季，干预使物种丰富度上升。"],
            ["S3", "在城市雨季，干预使物种丰富度下降。"],
            ["S4", "在乡村雨季，干预使物种丰富度上升。"],
        ],
        "atoms": [
            ["S1", {"生境": "城市", "季节": "旱季"}, "上升"],
            ["S2", {"生境": "乡村", "季节": "旱季"}, "上升"],
            ["S3", {"生境": "城市", "季节": "雨季"}, "下降"],
            ["S4", {"生境": "乡村", "季节": "雨季"}, "上升"],
        ],
    },
    {
        "id": "manufacturing_xor",
        "dimensions": {"材料": ["甲", "乙"], "湿度": ["低", "高"]},
        "studies": [
            ["S1", "材料甲在低湿度时缺陷率上升。"],
            ["S2", "材料乙在低湿度时缺陷率下降。"],
            ["S3", "材料甲在高湿度时缺陷率下降。"],
            ["S4", "材料乙在高湿度时缺陷率上升。"],
        ],
        "atoms": [
            ["S1", {"材料": "甲", "湿度": "低"}, "上升"],
            ["S2", {"材料": "乙", "湿度": "低"}, "下降"],
            ["S3", {"材料": "甲", "湿度": "高"}, "下降"],
            ["S4", {"材料": "乙", "湿度": "高"}, "上升"],
        ],
    },
    {
        "id": "traffic_partial_merge",
        "dimensions": {"路网": ["网格", "环形"], "需求": ["低", "高"]},
        "studies": [
            ["S1", "网格路网在低需求下平均行程时间不变。"],
            ["S2", "环形路网在低需求下平均行程时间不变。"],
            ["S3", "网格路网在高需求下平均行程时间上升。"],
            ["S4", "环形路网在高需求下平均行程时间下降。"],
        ],
        "atoms": [
            ["S1", {"路网": "网格", "需求": "低"}, "不变"],
            ["S2", {"路网": "环形", "需求": "低"}, "不变"],
            ["S3", {"路网": "网格", "需求": "高"}, "上升"],
            ["S4", {"路网": "环形", "需求": "高"}, "下降"],
        ],
    },
    {
        "id": "network_unknown_not_any",
        "dimensions": {"协议": ["甲协议", "乙协议"], "丢包率": ["低", "高"]},
        "studies": [
            ["S1", "甲协议在低丢包率下使吞吐量上升。"],
            ["S2", "甲协议在高丢包率下使吞吐量下降。"],
            ["S3", "乙协议在低丢包率下使吞吐量不变。"],
            ["S4", "乙协议在高丢包率下使吞吐量不变。"],
            ["S5", "一项未报告丢包率的甲协议实验发现吞吐量上升。"],
        ],
        "atoms": [
            ["S1", {"协议": "甲协议", "丢包率": "低"}, "上升"],
            ["S2", {"协议": "甲协议", "丢包率": "高"}, "下降"],
            ["S3", {"协议": "乙协议", "丢包率": "低"}, "不变"],
            ["S4", {"协议": "乙协议", "丢包率": "高"}, "不变"],
            ["S5", {"协议": "甲协议", "丢包率": UNKNOWN}, "上升"],
        ],
    },
    {
        "id": "solver_by_resolution",
        "dimensions": {"求解器": ["显式", "隐式"], "分辨率": ["粗", "细"]},
        "studies": [
            ["S1", "显式求解器在粗分辨率下使误差上升。"],
            ["S2", "隐式求解器在粗分辨率下也使误差上升。"],
            ["S3", "显式求解器在细分辨率下使误差下降。"],
            ["S4", "隐式求解器在细分辨率下也使误差下降。"],
        ],
        "atoms": [
            ["S1", {"求解器": "显式", "分辨率": "粗"}, "上升"],
            ["S2", {"求解器": "隐式", "分辨率": "粗"}, "上升"],
            ["S3", {"求解器": "显式", "分辨率": "细"}, "下降"],
            ["S4", {"求解器": "隐式", "分辨率": "细"}, "下降"],
        ],
    },
    {
        "id": "retrieval_unresolved",
        "dimensions": {"语料": ["干净", "噪声"], "查询": ["短", "长"]},
        "studies": [
            ["S1", "干净语料配合短查询时召回率上升。"],
            ["S2", "干净语料配合长查询时召回率上升。"],
            ["S3", "噪声语料配合短查询时召回率下降。"],
            ["S4", "噪声语料配合长查询时召回率上升。"],
            ["S5", "另一项噪声语料配合长查询的实验报告召回率下降。"],
        ],
        "atoms": [
            ["S1", {"语料": "干净", "查询": "短"}, "上升"],
            ["S2", {"语料": "干净", "查询": "长"}, "上升"],
            ["S3", {"语料": "噪声", "查询": "短"}, "下降"],
            ["S4", {"语料": "噪声", "查询": "长"}, "上升"],
            ["S5", {"语料": "噪声", "查询": "长"}, "下降"],
        ],
    },
]


def chat(prompt):
    payload = {
        "model": MODEL,
        "stream": False,
        "options": {"temperature": 0, "num_predict": 1800},
        "messages": [
            {"role": "system", "content": "你是严谨的研究证据抽取与综合器。只依据输入，不补充常识。"},
            {"role": "user", "content": prompt},
        ],
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    start = time.time()
    with urllib.request.urlopen(req, timeout=240) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body["message"]["content"], time.time() - start, body.get("eval_count", 0)


def parse_json(text):
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I | re.S)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        starts = [i for i in (cleaned.find("{"), cleaned.find("[")) if i >= 0]
        if not starts:
            raise
        start = min(starts)
        for end in range(len(cleaned), start, -1):
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                continue
        raise


def atom_dict(source, conditions, direction):
    return {"source_id": source, "conditions": conditions, "direction": direction}


def normalize_atoms(raw, task):
    items = raw.get("atoms", raw) if isinstance(raw, dict) else raw
    allowed_direction = {"上升", "下降", "不变"}
    output = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        source = str(item.get("source_id", "")).upper().strip()
        direction = str(item.get("direction", "")).strip()
        conditions = item.get("conditions", {})
        if not source or direction not in allowed_direction or not isinstance(conditions, dict):
            continue
        normalized = {}
        for dim, allowed in task["dimensions"].items():
            value = str(conditions.get(dim, UNKNOWN)).strip()
            normalized[dim] = value if value in allowed or value == UNKNOWN else value
        output.append(atom_dict(source, normalized, direction))
    return output


def can_merge(a, b, dimensions):
    if a["status"] != "支持" or b["status"] != "支持" or a["direction"] != b["direction"]:
        return None
    differing = []
    merged = {}
    for dim, levels in dimensions.items():
        va, vb = a["conditions"][dim], b["conditions"][dim]
        if va == vb:
            merged[dim] = va
        else:
            if UNKNOWN in (va, vb) or ANY in (va, vb):
                return None
            if set((va, vb)) != set(levels):
                return None
            differing.append(dim)
            merged[dim] = ANY
    return merged if len(differing) == 1 else None


def partition(atoms, dimensions):
    grouped = defaultdict(list)
    dim_names = list(dimensions)
    for atom in atoms:
        key = tuple(atom["conditions"].get(dim, UNKNOWN) for dim in dim_names)
        grouped[key].append(atom)
    cells = []
    for key, members in grouped.items():
        directions = sorted({m["direction"] for m in members})
        cells.append(
            {
                "conditions": dict(zip(dim_names, key)),
                "direction": directions[0] if len(directions) == 1 else "混合",
                "status": "支持" if len(directions) == 1 else "未解决",
                "source_ids": sorted({m["source_id"] for m in members}),
            }
        )
    changed = True
    while changed:
        changed = False
        for i in range(len(cells)):
            for j in range(i + 1, len(cells)):
                merged_conditions = can_merge(cells[i], cells[j], dimensions)
                if merged_conditions is None:
                    continue
                merged_cell = {
                    "conditions": merged_conditions,
                    "direction": cells[i]["direction"],
                    "status": "支持",
                    "source_ids": sorted(set(cells[i]["source_ids"] + cells[j]["source_ids"])),
                }
                cells = [c for k, c in enumerate(cells) if k not in (i, j)] + [merged_cell]
                changed = True
                break
            if changed:
                break
    cells.sort(key=lambda c: json.dumps(c["conditions"], ensure_ascii=False, sort_keys=True))
    return {"cells": cells, "global_claim": "无"}


def extraction_prompt(task):
    dimensions = json.dumps(task["dimensions"], ensure_ascii=False)
    studies = "\n".join(f"{sid}: {text}" for sid, text in task["studies"])
    return f"""从研究摘要中逐条抽取证据原子。
范围维度与唯一允许值：{dimensions}
若某维度没有报告，必须填“{UNKNOWN}”，不得把它解释成所有值。
方向只能是“上升”“下降”“不变”。保留每个来源，不能合并相反结果。

{studies}

只返回 JSON：
{{"atoms":[{{"source_id":"S1","conditions":{{"维度名":"允许值"}},"direction":"上升"}}]}}
每条研究恰好对应一个原子，每个 conditions 必须包含全部维度。"""


def synthesis_prompt(task, evidence_text, from_atoms):
    dimensions = json.dumps(task["dimensions"], ensure_ascii=False)
    source_label = "已抽取的证据原子" if from_atoms else "原始研究摘要"
    return f"""请综合下列多项研究，但必须保留结论适用范围。
范围维度与允许值：{dimensions}
规则：
1. 相同范围内方向相反，status 填“未解决”、direction 填“混合”，不得编造解释。
2. 两个“支持”单元仅在一个维度分别覆盖该维度的全部允许值、其他维度完全相同且方向相同时，才可把该维度合并为“{ANY}”。
3. “{UNKNOWN}”表示未知，绝不能当成“{ANY}”。
4. 若不同范围的方向不一致，global_claim 必须为“无”；不要输出无条件总体效应。
5. source_ids 必须列出支持该单元的全部来源。

{source_label}：
{evidence_text}

只返回 JSON：
{{"cells":[{{"conditions":{{"每个维度":"允许值/任意/未报告"}},"direction":"上升/下降/不变/混合","status":"支持/未解决","source_ids":["S1"]}}],"global_claim":"无/上升/下降/不变"}}"""


def normalize_output(raw, task):
    if not isinstance(raw, dict):
        return {"cells": [], "global_claim": "解析失败"}
    cells = []
    for cell in raw.get("cells", []) if isinstance(raw.get("cells", []), list) else []:
        if not isinstance(cell, dict) or not isinstance(cell.get("conditions"), dict):
            continue
        conditions = {dim: str(cell["conditions"].get(dim, UNKNOWN)).strip() for dim in task["dimensions"]}
        cells.append(
            {
                "conditions": conditions,
                "direction": str(cell.get("direction", "")).strip(),
                "status": str(cell.get("status", "")).strip(),
                "source_ids": sorted({str(x).upper().strip() for x in cell.get("source_ids", [])}),
            }
        )
    return {"cells": cells, "global_claim": str(raw.get("global_claim", "")).strip()}


def cell_key(cell, with_sources=False):
    core = (
        tuple(sorted(cell["conditions"].items())),
        cell["direction"],
        cell["status"],
    )
    return core + (tuple(sorted(cell.get("source_ids", []))),) if with_sources else core


def score(output, gold):
    predicted = {cell_key(c) for c in output["cells"]}
    expected = {cell_key(c) for c in gold["cells"]}
    predicted_sources = {cell_key(c, True) for c in output["cells"]}
    expected_sources = {cell_key(c, True) for c in gold["cells"]}
    overlap = len(predicted & expected)
    precision = overlap / len(predicted) if predicted else 0.0
    recall = overlap / len(expected) if expected else 1.0
    global_safe = output.get("global_claim") == gold.get("global_claim")
    exact_cells = predicted == expected
    exact_sources = predicted_sources == expected_sources
    return {
        "cell_precision": precision,
        "cell_recall": recall,
        "exact_cells": exact_cells,
        "exact_sources": exact_sources,
        "global_safe": global_safe,
        "full_success": exact_cells and exact_sources and global_safe,
    }


def safe_parse(text):
    try:
        return parse_json(text), None
    except Exception as exc:
        return {}, f"{type(exc).__name__}: {exc}"


def summarize(records):
    strategies = ["direct", "strong_two_stage", "auto_partition", "oracle_partition"]
    summary = {}
    for strategy in strategies:
        scores = [r["strategies"][strategy]["score"] for r in records]
        summary[strategy] = {
            "tasks": len(scores),
            "full_success": sum(s["full_success"] for s in scores),
            "exact_cells": sum(s["exact_cells"] for s in scores),
            "exact_sources": sum(s["exact_sources"] for s in scores),
            "global_safe": sum(s["global_safe"] for s in scores),
            "mean_cell_precision": sum(s["cell_precision"] for s in scores) / len(scores),
            "mean_cell_recall": sum(s["cell_recall"] for s in scores) / len(scores),
        }
    return summary


def main():
    records = []
    totals = {"seconds": 0.0, "output_tokens": 0}
    for task in TASKS:
        gold_atoms = [atom_dict(*item) for item in task["atoms"]]
        gold = partition(gold_atoms, task["dimensions"])

        extract_text, extract_seconds, extract_tokens = chat(extraction_prompt(task))
        extract_raw, extract_error = safe_parse(extract_text)
        auto_atoms = normalize_atoms(extract_raw, task)
        auto_partition = partition(auto_atoms, task["dimensions"])

        studies_text = "\n".join(f"{sid}: {text}" for sid, text in task["studies"])
        direct_text, direct_seconds, direct_tokens = chat(synthesis_prompt(task, studies_text, False))
        direct_raw, direct_error = safe_parse(direct_text)
        direct = normalize_output(direct_raw, task)

        atoms_text = json.dumps({"atoms": auto_atoms}, ensure_ascii=False, indent=2)
        strong_text, strong_seconds, strong_tokens = chat(synthesis_prompt(task, atoms_text, True))
        strong_raw, strong_error = safe_parse(strong_text)
        strong = normalize_output(strong_raw, task)

        totals["seconds"] += extract_seconds + direct_seconds + strong_seconds
        totals["output_tokens"] += extract_tokens + direct_tokens + strong_tokens
        records.append(
            {
                "task_id": task["id"],
                "dimensions": task["dimensions"],
                "studies": task["studies"],
                "gold_atoms": gold_atoms,
                "gold_partition": gold,
                "extraction": {
                    "raw_text": extract_text,
                    "parse_error": extract_error,
                    "atoms": auto_atoms,
                    "seconds": extract_seconds,
                    "output_tokens": extract_tokens,
                },
                "strategies": {
                    "direct": {
                        "raw_text": direct_text,
                        "parse_error": direct_error,
                        "output": direct,
                        "score": score(direct, gold),
                        "seconds": direct_seconds,
                        "output_tokens": direct_tokens,
                    },
                    "strong_two_stage": {
                        "raw_text": strong_text,
                        "parse_error": strong_error,
                        "output": strong,
                        "score": score(strong, gold),
                        "seconds": strong_seconds,
                        "output_tokens": strong_tokens,
                    },
                    "auto_partition": {
                        "output": auto_partition,
                        "score": score(auto_partition, gold),
                    },
                    "oracle_partition": {
                        "output": gold,
                        "score": score(gold, gold),
                    },
                },
            }
        )
        print(json.dumps({"completed": task["id"], "count": len(records)}, ensure_ascii=False), flush=True)

    result = {
        "model": MODEL,
        "task_count": len(TASKS),
        "design": "10 个本地多文档、多变量、非临床决策合成任务；直接综合与强两阶段基线使用同一模型，自动范围分割复用同一抽取结果。",
        "summary": summarize(records),
        "totals": totals,
        "records": records,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
