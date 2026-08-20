import ast
import json
import math
import re
import time
import urllib.request
from pathlib import Path


MODEL = "qwen2.5:7b"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
ROOT = Path(__file__).parent
SOURCE = ROOT / "scicoqa_synthetic_first_rows.json"
OUT = ROOT / "execution_delta_witness_qwen2_5_7b.json"


def chat(system, prompt):
    payload = {
        "model": MODEL,
        "stream": False,
        "keep_alive": "30m",
        "options": {"temperature": 0, "num_predict": 900},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    started = time.time()
    with urllib.request.urlopen(req, timeout=240) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body["message"]["content"], time.time() - started, body.get("eval_count", 0)


def parse_json(text):
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I | re.S)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        if start < 0:
            raise
        for end in range(len(cleaned), start, -1):
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                continue
        raise


def normalize_label(value):
    text = str(value or "").strip().upper()
    if text in {"MATCH", "ALIGNED", "一致", "匹配"}:
        return "MATCH"
    if text in {"MISMATCH", "NOT_MATCH", "MISALIGNED", "不一致", "不匹配", "冲突"}:
        return "MISMATCH"
    return "INVALID"


ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.FloorDiv: lambda a, b: a // b,
    ast.Mod: lambda a, b: a % b,
    ast.Pow: lambda a, b: a**b,
}
ALLOWED_CMPS = {
    ast.Eq: lambda a, b: a == b,
    ast.NotEq: lambda a, b: a != b,
    ast.Lt: lambda a, b: a < b,
    ast.LtE: lambda a, b: a <= b,
    ast.Gt: lambda a, b: a > b,
    ast.GtE: lambda a, b: a >= b,
}
ALLOWED_FUNCS = {"abs": abs, "min": min, "max": max}


def safe_eval(expr, variables):
    if not isinstance(expr, str) or len(expr) > 300:
        raise ValueError("bad expression length")
    tree = ast.parse(expr, mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, bool)):
            return node.value
        if isinstance(node, ast.Name) and re.fullmatch(r"x[0-7]", node.id):
            return variables[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_BINOPS:
            return ALLOWED_BINOPS[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -visit(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +visit(node.operand)
            if isinstance(node.op, ast.Not):
                return not visit(node.operand)
        if isinstance(node, ast.BoolOp):
            values = [bool(visit(v)) for v in node.values]
            if isinstance(node.op, ast.And):
                return all(values)
            if isinstance(node.op, ast.Or):
                return any(values)
        if isinstance(node, ast.Compare):
            left = visit(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = visit(comparator)
                if type(op) not in ALLOWED_CMPS or not ALLOWED_CMPS[type(op)](left, right):
                    return False
                left = right
            return True
        if isinstance(node, ast.IfExp):
            return visit(node.body) if visit(node.test) else visit(node.orelse)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ALLOWED_FUNCS:
            return ALLOWED_FUNCS[node.func.id](*(visit(a) for a in node.args))
        raise ValueError(f"disallowed AST node: {type(node).__name__}")

    value = visit(tree)
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite value")
    return value


def values_equal(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-9)
    return a == b


def task_text(task):
    sections = "\n".join(f"- {s}" for s in task["paper_sections"])
    return f"""论文相关段落：
{sections}

最近基线代码：
```python
{task['baseline_code']}
```

待核验代码：
```python
{task['candidate_code']}
```
"""


def direct_prompt(task):
    return task_text(task) + """
判断待核验代码是否保持论文段落所述、且由最近基线实现的关键计算关系。
只返回 JSON：{"label":"MATCH或MISMATCH","reason":"一句话"}
"""


def structured_prompt(task):
    return task_text(task) + """
先分别写出论文规则、基线行为和待核验代码行为，再判断是否一致。
只返回 JSON：
{"paper_rule":"...","baseline_behavior":"...","candidate_behavior":"...","label":"MATCH或MISMATCH","reason":"..."}
"""


def witness_prompt(task):
    return task_text(task) + """
把与论文声明直接相关的基线计算和待核验计算，各自抽象成一个可执行标量表达式，并给出一组最小输入。
表达式只能使用变量 x0 到 x7、数值/布尔常量、+ - * / // % **、比较、and/or/not、Python 条件表达式，以及 abs/min/max；不得调用其他函数、索引、属性、列表或任意代码。
若原代码涉及张量、归一化、损失、采样或网络，可把声明相关的输入/中间量抽象为 x0...，但两个表达式必须使用同一变量语义。
只返回 JSON：
{"paper_rule":"...","variable_meanings":{"x0":"..."},"variables":{"x0":0.2},"baseline_expr":"...","candidate_expr":"...","predicted_label":"MATCH或MISMATCH","binding_reason":"说明表达式如何绑定到两段代码"}
"""


def load_tasks():
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    tasks = []
    for wrapped in payload["rows"]:
        row = wrapped["row"]
        baseline = "\n\n".join(row["changed_code_snippets"]["original_code"])
        changed = "\n\n".join(row["changed_code_snippets"]["changed_code"])
        common = {
            "source_index": wrapped["row_idx"],
            "source_id": row["discrepancy_id"],
            "paper_sections": row["relevant_paper_sections_gpt"],
            "baseline_code": baseline,
            "discrepancy_type": row["discrepancy_type"],
            "source_file": ",".join(row["changed_code_files"]["file_name"]),
        }
        tasks.append(
            {
                **common,
                "task_id": f"{row['discrepancy_id']}-changed",
                "variant": "changed",
                "candidate_code": changed,
                "gold": "MISMATCH",
            }
        )
        tasks.append(
            {
                **common,
                "task_id": f"{row['discrepancy_id']}-benign",
                "variant": "benign_comment",
                "candidate_code": "# 仅添加注释的语义等价改写\n" + baseline,
                "gold": "MATCH",
            }
        )
    return tasks


def evaluate_witness(parsed):
    variables = parsed.get("variables", {})
    if not isinstance(variables, dict) or not variables or len(variables) > 8:
        raise ValueError("variables must be a non-empty object")
    normalized = {}
    for key, value in variables.items():
        if not re.fullmatch(r"x[0-7]", str(key)) or not isinstance(value, (int, float, bool)):
            raise ValueError("invalid variable")
        normalized[str(key)] = value
    baseline_value = safe_eval(parsed.get("baseline_expr"), normalized)
    candidate_value = safe_eval(parsed.get("candidate_expr"), normalized)
    label = "MATCH" if values_equal(baseline_value, candidate_value) else "MISMATCH"
    return {
        "variables": normalized,
        "baseline_value": baseline_value,
        "candidate_value": candidate_value,
        "verified_label": label,
    }


def summarize(records, method):
    subset = [r for r in records if r["method"] == method]
    valid = [r for r in subset if r["prediction"] != "INVALID"]
    changed = [r for r in subset if r["gold"] == "MISMATCH"]
    benign = [r for r in subset if r["gold"] == "MATCH"]
    return {
        "total": len(subset),
        "valid": len(valid),
        "accuracy_strict": sum(r["prediction"] == r["gold"] for r in subset) / len(subset),
        "changed_recall": sum(r["prediction"] == "MISMATCH" for r in changed) / len(changed),
        "benign_specificity": sum(r["prediction"] == "MATCH" for r in benign) / len(benign),
        "mean_seconds": sum(r["seconds"] for r in subset) / len(subset),
        "tokens": sum(r["eval_count"] for r in subset),
    }


def main():
    tasks = load_tasks()
    methods = [
        ("direct", "你是严格的论文—代码一致性核验器。只依据给定论文段落和代码。", direct_prompt),
        ("structured", "你是严格的论文—代码一致性核验器。先分解规则与实现，再判断。", structured_prompt),
        ("execution_witness", "你把论文方法声明绑定为受限、可执行的标量差分见证。不得输出或运行任意代码。", witness_prompt),
    ]
    records = []
    started = time.time()
    for method, system, make_prompt in methods:
        for index, task in enumerate(tasks, 1):
            raw = ""
            parsed = None
            error = None
            witness = None
            seconds = 0.0
            eval_count = 0
            prediction = "INVALID"
            try:
                raw, seconds, eval_count = chat(system, make_prompt(task))
                parsed = parse_json(raw)
                if method == "execution_witness":
                    witness = evaluate_witness(parsed)
                    prediction = witness["verified_label"]
                else:
                    prediction = normalize_label(parsed.get("label"))
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
            records.append(
                {
                    "method": method,
                    "task_id": task["task_id"],
                    "source_id": task["source_id"],
                    "variant": task["variant"],
                    "gold": task["gold"],
                    "prediction": prediction,
                    "correct": prediction == task["gold"],
                    "seconds": seconds,
                    "eval_count": eval_count,
                    "parsed": parsed,
                    "witness": witness,
                    "raw": raw,
                    "error": error,
                }
            )
            print(f"{method} {index:02d}/{len(tasks)} {task['task_id']} {prediction} gold={task['gold']} error={error}", flush=True)
    result = {
        "model": MODEL,
        "source": "UKPLab/scicoqa synthetic first rows via Hugging Face datasets server",
        "task_count": len(tasks),
        "source_pair_count": len(tasks) // 2,
        "safety": "Only a whitelisted Python AST evaluator executed model-produced scalar expressions; repository and arbitrary generated code were not executed.",
        "elapsed_seconds": time.time() - started,
        "metrics": {method: summarize(records, method) for method, _, _ in methods},
        "records": records,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["metrics"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
