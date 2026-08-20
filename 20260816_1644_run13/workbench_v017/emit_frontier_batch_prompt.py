from __future__ import annotations

import argparse
import json

from mechanism_equivalence_probe import PAIRS


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=["prose", "self_normalize"], required=True)
    args = parser.parse_args()

    records = [{"id": pair["id"], "a": pair["a"], "b": pair["b"]} for pair in PAIRS]
    extra = ""
    if args.condition == "self_normalize":
        extra = (
            "判断前分别在内部规范化：读取的信息、核心算子、执行时机、决策规则。"
            "同义算子映射到同一抽象操作，不得臆造原文未说明的差异。"
        )

    prompt = (
        "你是严格的方法机制审计器。下面有 20 对候选方法描述。"
        "请判断每一对是否改变了同一个核心计算。不要按主题、领域或词面相似度判断；"
        "信息源、核心算子、执行时机或决策规则任一实质不同，就判为不同。"
        + extra
        + "不要调用工具，不要读取文件，也不要解释。只输出一个 JSON 数组，"
        '数组中每项严格为 {"id":"原始标识","same":true或false}，顺序保持不变。\n'
        + json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    )
    print(prompt)


if __name__ == "__main__":
    main()
