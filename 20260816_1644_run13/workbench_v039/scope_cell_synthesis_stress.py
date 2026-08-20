import json
from pathlib import Path

import scope_cell_synthesis_pilot as pilot
import scope_cell_semantic_rescore as semantic


OUT = Path(__file__).with_name("scope_cell_synthesis_stress_qwen2_5_7b.json")


TASKS = [
    {
        "id": "coating_three_dimensional_merge",
        "dimensions": {"基材": ["铝", "钢"], "温度": ["低温", "高温"], "工艺": ["喷涂", "浸涂"]},
        "studies": [
            ["A1", "铝基材在低温喷涂时，附着强度比对照低 8%，即附着强度下降。"],
            ["A2", "钢基材采用低温喷涂，测得附着强度下降；样品厚度为 2 毫米。"],
            ["A3", "对铝片实施低温浸涂后，附着强度有所下降。"],
            ["A4", "钢片的低温浸涂实验重复三次，结论仍是附着强度下降。"],
            ["A5", "铝基材在高温喷涂条件下，附着强度上升。"],
            ["A6", "尽管早期试验讨论过腐蚀，当前钢基材高温喷涂结果显示附着强度上升。"],
            ["A7", "高温浸涂的铝片，其附着强度提高，幅度为 6%。"],
            ["A8", "钢片经高温浸涂后并未下降，而是出现附着强度上升。"],
        ],
        "atoms": [
            ["A1", {"基材": "铝", "温度": "低温", "工艺": "喷涂"}, "下降"],
            ["A2", {"基材": "钢", "温度": "低温", "工艺": "喷涂"}, "下降"],
            ["A3", {"基材": "铝", "温度": "低温", "工艺": "浸涂"}, "下降"],
            ["A4", {"基材": "钢", "温度": "低温", "工艺": "浸涂"}, "下降"],
            ["A5", {"基材": "铝", "温度": "高温", "工艺": "喷涂"}, "上升"],
            ["A6", {"基材": "钢", "温度": "高温", "工艺": "喷涂"}, "上升"],
            ["A7", {"基材": "铝", "温度": "高温", "工艺": "浸涂"}, "上升"],
            ["A8", {"基材": "钢", "温度": "高温", "工艺": "浸涂"}, "上升"],
        ],
    },
    {
        "id": "compiler_three_way_interaction",
        "dimensions": {"语言": ["甲语言", "乙语言"], "优化": ["开启", "关闭"], "程序": ["递归", "迭代"]},
        "studies": [
            ["B1", "甲语言、开启优化、递归程序的峰值内存上升。"],
            ["B2", "甲语言在开启优化后运行迭代程序，峰值内存下降。"],
            ["B3", "关闭优化的甲语言递归程序没有保持原值，峰值内存下降。"],
            ["B4", "甲语言、关闭优化、迭代实现的峰值内存上升。"],
            ["B5", "乙语言的递归程序在开启优化时峰值内存下降。"],
            ["B6", "乙语言、优化开启、迭代程序使峰值内存上升。"],
            ["B7", "对乙语言关闭优化并使用递归实现，峰值内存上升。"],
            ["B8", "乙语言的迭代实现关闭优化后，峰值内存下降。"],
        ],
        "atoms": [
            ["B1", {"语言": "甲语言", "优化": "开启", "程序": "递归"}, "上升"],
            ["B2", {"语言": "甲语言", "优化": "开启", "程序": "迭代"}, "下降"],
            ["B3", {"语言": "甲语言", "优化": "关闭", "程序": "递归"}, "下降"],
            ["B4", {"语言": "甲语言", "优化": "关闭", "程序": "迭代"}, "上升"],
            ["B5", {"语言": "乙语言", "优化": "开启", "程序": "递归"}, "下降"],
            ["B6", {"语言": "乙语言", "优化": "开启", "程序": "迭代"}, "上升"],
            ["B7", {"语言": "乙语言", "优化": "关闭", "程序": "递归"}, "上升"],
            ["B8", {"语言": "乙语言", "优化": "关闭", "程序": "迭代"}, "下降"],
        ],
    },
    {
        "id": "irrigation_partial_invariance",
        "dimensions": {"土质": ["壤土", "砂土"], "季节": ["春季", "秋季"], "剂量": ["低剂量", "高剂量"]},
        "studies": [
            ["C1", "壤土春季使用低剂量方案，耗水量下降。"],
            ["C2", "在壤土的春季，高剂量方案同样降低耗水量。"],
            ["C3", "壤土秋季低剂量使耗水量上升。"],
            ["C4", "壤土秋季高剂量也使耗水量上升。"],
            ["C5", "砂土春季低剂量的耗水量上升。"],
            ["C6", "砂土春季高剂量方案下，耗水量仍然上升。"],
            ["C7", "砂土秋季低剂量使耗水量下降。"],
            ["C8", "砂土秋季高剂量实验观测到耗水量下降。"],
        ],
        "atoms": [
            ["C1", {"土质": "壤土", "季节": "春季", "剂量": "低剂量"}, "下降"],
            ["C2", {"土质": "壤土", "季节": "春季", "剂量": "高剂量"}, "下降"],
            ["C3", {"土质": "壤土", "季节": "秋季", "剂量": "低剂量"}, "上升"],
            ["C4", {"土质": "壤土", "季节": "秋季", "剂量": "高剂量"}, "上升"],
            ["C5", {"土质": "砂土", "季节": "春季", "剂量": "低剂量"}, "上升"],
            ["C6", {"土质": "砂土", "季节": "春季", "剂量": "高剂量"}, "上升"],
            ["C7", {"土质": "砂土", "季节": "秋季", "剂量": "低剂量"}, "下降"],
            ["C8", {"土质": "砂土", "季节": "秋季", "剂量": "高剂量"}, "下降"],
        ],
    },
    {
        "id": "robot_unresolved_with_distractors",
        "dimensions": {"场地": ["室内", "室外"], "光照": ["弱光", "强光"], "控制器": ["甲控制器", "乙控制器"]},
        "studies": [
            ["D1", "室内弱光下，甲控制器使定位误差下降。旧版机器人重量为 12 千克。"],
            ["D2", "相同的室内弱光和甲控制器设置，却报告定位误差上升；摘要没有给出可解释差异。"],
            ["D3", "室内弱光下使用乙控制器，定位误差不变。"],
            ["D4", "室外弱光实验采用甲控制器，定位误差上升。"],
            ["D5", "室外弱光实验改用乙控制器后，定位误差仍上升。"],
            ["D6", "室外强光下，甲控制器和乙控制器分别测试，两个实验均发现定位误差下降。"],
        ],
        "atoms": [
            ["D1", {"场地": "室内", "光照": "弱光", "控制器": "甲控制器"}, "下降"],
            ["D2", {"场地": "室内", "光照": "弱光", "控制器": "甲控制器"}, "上升"],
            ["D3", {"场地": "室内", "光照": "弱光", "控制器": "乙控制器"}, "不变"],
            ["D4", {"场地": "室外", "光照": "弱光", "控制器": "甲控制器"}, "上升"],
            ["D5", {"场地": "室外", "光照": "弱光", "控制器": "乙控制器"}, "上升"],
            ["D6", {"场地": "室外", "光照": "强光", "控制器": "甲控制器"}, "下降"],
            ["D6", {"场地": "室外", "光照": "强光", "控制器": "乙控制器"}, "下降"],
        ],
    },
    {
        "id": "storage_unknown_dimension",
        "dimensions": {"介质": ["固态盘", "机械盘"], "队列": ["短队列", "长队列"], "缓存": ["开启", "关闭"]},
        "studies": [
            ["E1", "固态盘、短队列且开启缓存时，写入延迟下降。"],
            ["E2", "固态盘在短队列、关闭缓存时，写入延迟上升。"],
            ["E3", "机械盘使用长队列并开启缓存，写入延迟下降。"],
            ["E4", "机械盘、长队列、关闭缓存的实验显示写入延迟上升。"],
            ["E5", "固态盘长队列实验发现写入延迟下降，但摘要没有报告缓存是否开启。"],
        ],
        "atoms": [
            ["E1", {"介质": "固态盘", "队列": "短队列", "缓存": "开启"}, "下降"],
            ["E2", {"介质": "固态盘", "队列": "短队列", "缓存": "关闭"}, "上升"],
            ["E3", {"介质": "机械盘", "队列": "长队列", "缓存": "开启"}, "下降"],
            ["E4", {"介质": "机械盘", "队列": "长队列", "缓存": "关闭"}, "上升"],
            ["E5", {"介质": "固态盘", "队列": "长队列", "缓存": pilot.UNKNOWN}, "下降"],
        ],
    },
    {
        "id": "sensor_negation_and_background",
        "dimensions": {"传感器": ["甲型", "乙型"], "天气": ["晴天", "雨天"], "校准": ["单点", "多点"]},
        "studies": [
            ["F1", "背景工作认为甲型传感器不稳定；但本研究在晴天单点校准后，测量偏差并未上升，而是下降。"],
            ["F2", "甲型、晴天、多点校准没有带来改善，测量偏差保持不变。"],
            ["F3", "在雨天对甲型做单点校准，测量偏差提高。"],
            ["F4", "甲型雨天多点校准使偏差降低，尽管电池电压下降了 0.2 伏。"],
            ["F5", "乙型晴天单点校准，测量偏差下降。"],
            ["F6", "乙型晴天多点校准后偏差没有显著变化。"],
            ["F7", "乙型雨天单点校准的偏差不降反升。"],
            ["F8", "乙型雨天多点校准把测量偏差降了下来。"],
        ],
        "atoms": [
            ["F1", {"传感器": "甲型", "天气": "晴天", "校准": "单点"}, "下降"],
            ["F2", {"传感器": "甲型", "天气": "晴天", "校准": "多点"}, "不变"],
            ["F3", {"传感器": "甲型", "天气": "雨天", "校准": "单点"}, "上升"],
            ["F4", {"传感器": "甲型", "天气": "雨天", "校准": "多点"}, "下降"],
            ["F5", {"传感器": "乙型", "天气": "晴天", "校准": "单点"}, "下降"],
            ["F6", {"传感器": "乙型", "天气": "晴天", "校准": "多点"}, "不变"],
            ["F7", {"传感器": "乙型", "天气": "雨天", "校准": "单点"}, "上升"],
            ["F8", {"传感器": "乙型", "天气": "雨天", "校准": "多点"}, "下降"],
        ],
    },
]


def stress_extraction_prompt(task):
    dimensions = json.dumps(task["dimensions"], ensure_ascii=False)
    studies = "\n".join(f"{sid}: {text}" for sid, text in task["studies"])
    return f"""从研究摘要中逐条抽取证据原子。
范围维度与唯一允许值：{dimensions}
若某维度没有报告，必须填“{pilot.UNKNOWN}”，不得把它解释成所有值。
方向只能是“上升”“下降”“不变”。保留每个来源，不能合并相反结果。
一篇摘要若明确报告多个不同范围的实验结果，应为同一 source_id 输出多个原子。
背景工作、其他指标和样本描述不是当前结果，不得抽成证据原子。

{studies}

只返回 JSON：
{{"atoms":[{{"source_id":"A1","conditions":{{"维度名":"允许值"}},"direction":"上升"}}]}}
每个 conditions 必须包含全部维度。"""


def run():
    records = []
    totals = {"seconds": 0.0, "output_tokens": 0}
    for task in TASKS:
        gold_atoms = [pilot.atom_dict(*item) for item in task["atoms"]]
        gold = pilot.partition(gold_atoms, task["dimensions"])

        extract_text, extract_seconds, extract_tokens = pilot.chat(stress_extraction_prompt(task))
        extract_raw, extract_error = pilot.safe_parse(extract_text)
        auto_atoms = pilot.normalize_atoms(extract_raw, task)
        auto_output = pilot.partition(auto_atoms, task["dimensions"])

        studies_text = "\n".join(f"{sid}: {text}" for sid, text in task["studies"])
        direct_text, direct_seconds, direct_tokens = pilot.chat(pilot.synthesis_prompt(task, studies_text, False))
        direct_raw, direct_error = pilot.safe_parse(direct_text)
        direct_output = pilot.normalize_output(direct_raw, task)

        atoms_text = json.dumps({"atoms": auto_atoms}, ensure_ascii=False, indent=2)
        strong_text, strong_seconds, strong_tokens = pilot.chat(pilot.synthesis_prompt(task, atoms_text, True))
        strong_raw, strong_error = pilot.safe_parse(strong_text)
        strong_output = pilot.normalize_output(strong_raw, task)

        totals["seconds"] += extract_seconds + direct_seconds + strong_seconds
        totals["output_tokens"] += extract_tokens + direct_tokens + strong_tokens
        outputs = {
            "direct": direct_output,
            "strong_two_stage": strong_output,
            "auto_partition": auto_output,
            "oracle_partition": gold,
        }
        scores = {
            name: semantic.score(output, gold, gold_atoms, task["dimensions"])
            for name, output in outputs.items()
        }
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
                    "direct": {"raw_text": direct_text, "parse_error": direct_error, "output": direct_output, "score": scores["direct"]},
                    "strong_two_stage": {"raw_text": strong_text, "parse_error": strong_error, "output": strong_output, "score": scores["strong_two_stage"]},
                    "auto_partition": {"output": auto_output, "score": scores["auto_partition"]},
                    "oracle_partition": {"output": gold, "score": scores["oracle_partition"]},
                },
            }
        )
        print(json.dumps({"completed": task["id"], "count": len(records)}, ensure_ascii=False), flush=True)

    summary = {}
    for name in ["direct", "strong_two_stage", "auto_partition", "oracle_partition"]:
        scores = [record["strategies"][name]["score"] for record in records]
        summary[name] = {
            "tasks": len(scores),
            "semantic_full_success": sum(score["semantic_full_success"] for score in scores),
            "exact_semantics": sum(score["exact_semantics"] for score in scores),
            "global_safe": sum(score["global_safe"] for score in scores),
            "mean_semantic_precision": sum(score["semantic_precision"] for score in scores) / len(scores),
            "mean_semantic_recall": sum(score["semantic_recall"] for score in scores) / len(scores),
            "mean_evidence_coverage": sum(score["evidence_coverage"] for score in scores) / len(scores),
            "mean_compactness_ratio": sum(score["compactness_ratio"] for score in scores) / len(scores),
        }
    result = {
        "model": pilot.MODEL,
        "task_count": len(TASKS),
        "design": "6 个本地三维或干扰压力任务；包含自然改写、否定、背景数值、同域冲突、一条摘要双原子和未报告变量。",
        "summary": summary,
        "totals": totals,
        "records": records,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    run()
