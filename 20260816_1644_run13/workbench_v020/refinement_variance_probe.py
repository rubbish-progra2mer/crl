"""Probe whether one-shot scores confound idea quality with implementation quality.

For each fixed optimization idea, ask local code models for independent
implementations, execute them with Heuresis' sealed BBOB driver, and retain all
raw generations and deterministic scores.  The script never edits the cloned
Heuresis repository.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TASK_DIR = ROOT / "Heuresis" / "src" / "heuresis" / "tasks" / "bbob"
LOCAL_DRIVER = ROOT / "local_bbob_driver.py"
OUT_DIR = ROOT / "refinement_variance_runs"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODELS = ("qwen2.5:7b", "qwen3:8b")
IDEAS = {
    "uniform_random": (
        "Implement a clean uniform-random-search control. Spend the complete "
        "evaluation budget and keep the best point. Do not add local search."
    ),
    "restart_pattern": (
        "Implement restarted coordinate pattern search. Use several random "
        "starts, test positive and negative coordinate moves, and adapt the "
        "step size from success or failure."
    ),
    "adaptive_gaussian": (
        "Implement a multi-start adaptive Gaussian evolution strategy around "
        "an incumbent. Adapt global step size from recent success and restart "
        "after stagnation."
    ),
    "differential_evolution": (
        "Implement differential evolution with a bounded population, mutation, "
        "binomial crossover, selection, and at least one diversity-preserving "
        "restart rule."
    ),
    "particle_swarm": (
        "Implement particle swarm optimization with personal/global bests, "
        "bounded positions, inertia scheduling, and a stagnation restart."
    ),
    "full_covariance_es": (
        "Implement a compact full-covariance evolution strategy: sample a "
        "population from a multivariate Gaussian, update the mean and covariance "
        "from elites, adapt scale, and regularize the covariance."
    ),
    "nelder_mead_restarts": (
        "Implement Nelder-Mead from scratch using only NumPy, with reflection, "
        "expansion, contraction, shrink, and multiple randomized restarts."
    ),
    "global_local_hybrid": (
        "Implement a hybrid that first spends part of the budget on broad random "
        "sampling, then launches several adaptive local searches from the best "
        "diverse points."
    ),
}


def prompt_for(idea_id: str, idea: str, replicate: int) -> str:
    return f"""You are independently implementing one fixed algorithmic idea.

Task: write the complete contents of optimizer.py for a 5-dimensional black-box
minimization benchmark. The only required entry point is:

    optimize(f, dim, bounds, budget, seed) -> dict

Calling f(x) consumes one evaluation. Stay within budget. Bounds are a pair
(low, high). You may import only Python standard-library modules, NumPy, and
BudgetExhausted from problems. The driver ignores reported scores and tracks f
calls itself. Never inspect f internals, closures, attributes, source files, or
problem generators. Do not import make_problem. Do not write files or invoke
subprocesses.

Fixed idea ({idea_id}): {idea}

This is independent implementation replicate {replicate}. Make genuine design
choices inside the fixed idea, but do not switch to another algorithm family.
Return only executable Python code, with no Markdown fence or explanation.
"""


def call_ollama(model: str, prompt: str) -> str:
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0.75,
                "top_p": 0.9,
                "num_predict": 3500,
                "seed": int(time.time_ns() % 2_147_483_647),
            },
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=900) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return str(payload.get("response", ""))


def extract_code(raw: str) -> str:
    text = raw.strip()
    fenced = re.search(r"```(?:python)?\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        text = fenced.group(1).strip()
    start_markers = [
        index for marker in ("from __future__", "import ", "from ", "def optimize")
        if (index := text.find(marker)) >= 0
    ]
    if start_markers:
        text = text[min(start_markers):]
    return text.rstrip() + "\n"


def validate_code(code: str) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return [f"syntax:{exc.msg}:line={exc.lineno}"]

    forbidden_names = {
        "eval", "exec", "open", "compile", "__import__", "getattr", "setattr",
        "globals", "locals", "vars", "breakpoint", "input",
    }
    forbidden_modules = {
        "subprocess", "socket", "requests", "urllib", "http", "pathlib", "os",
        "sys", "inspect", "importlib", "pickle", "marshal",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in forbidden_names:
            errors.append(f"forbidden_name:{node.id}")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            errors.append(f"forbidden_dunder_attribute:{node.attr}")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in forbidden_modules:
                    errors.append(f"forbidden_import:{alias.name}")
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.split(".")[0] in forbidden_modules:
                errors.append(f"forbidden_import:{module}")
            if module == "problems":
                imported = {alias.name for alias in node.names}
                if not imported.issubset({"BudgetExhausted"}):
                    errors.append(f"forbidden_problems_import:{sorted(imported)}")
    if not any(isinstance(node, ast.FunctionDef) and node.name == "optimize" for node in tree.body):
        errors.append("missing_optimize")
    return sorted(set(errors))


def parse_score(stdout: str) -> tuple[float | None, int | None]:
    score_match = re.search(r"^mean_log_gap:\s*(\S+)\s*$", stdout, flags=re.MULTILINE)
    error_match = re.search(r"^n_errors:\s*(\d+)\s*$", stdout, flags=re.MULTILINE)
    score = float(score_match.group(1)) if score_match else None
    n_errors = int(error_match.group(1)) if error_match else None
    return score, n_errors


def run_one(model: str, idea_id: str, idea: str, replicate: int, python: str) -> dict:
    safe_model = model.replace(":", "_").replace("/", "_")
    case_dir = OUT_DIR / safe_model / idea_id / f"rep_{replicate:02d}"
    case_dir.mkdir(parents=True, exist_ok=True)
    record_path = case_dir / "record.json"
    if record_path.exists():
        return json.loads(record_path.read_text(encoding="utf-8"))

    prompt = prompt_for(idea_id, idea, replicate)
    t0 = time.monotonic()
    raw = call_ollama(model, prompt)
    generation_s = time.monotonic() - t0
    code = extract_code(raw)
    validation_errors = validate_code(code)

    (case_dir / "prompt.txt").write_text(prompt, encoding="utf-8", newline="\n")
    (case_dir / "raw_response.txt").write_text(raw, encoding="utf-8", newline="\n")
    (case_dir / "optimizer.py").write_text(code, encoding="utf-8", newline="\n")
    shutil.copy2(LOCAL_DRIVER, case_dir / "driver.py")
    for name in ("problems.py", "problem_spec.json"):
        shutil.copy2(TASK_DIR / name, case_dir / name)

    stdout = ""
    stderr = ""
    return_code: int | None = None
    execution_s = 0.0
    timed_out = False
    if not validation_errors:
        t1 = time.monotonic()
        try:
            completed = subprocess.run(
                [python, "driver.py"],
                cwd=case_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=240,
                check=False,
            )
            return_code = completed.returncode
            stdout = completed.stdout
            stderr = completed.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""
        execution_s = time.monotonic() - t1
    score, n_errors = parse_score(stdout)
    (case_dir / "run.log").write_text(stdout, encoding="utf-8", newline="\n")
    (case_dir / "run.stderr.log").write_text(stderr, encoding="utf-8", newline="\n")

    record = {
        "model": model,
        "idea_id": idea_id,
        "replicate": replicate,
        "score": score,
        "n_errors": n_errors,
        "return_code": return_code,
        "timed_out": timed_out,
        "validation_errors": validation_errors,
        "generation_s": generation_s,
        "execution_s": execution_s,
        "code_sha256": hashlib.sha256(code.encode("utf-8")).hexdigest(),
        "case_dir": str(case_dir),
    }
    record_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", required=True)
    parser.add_argument("--replicates", type=int, default=3)
    parser.add_argument("--models", nargs="*", default=list(MODELS))
    parser.add_argument("--ideas", nargs="*", default=list(IDEAS))
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    total = len(args.models) * len(args.ideas) * args.replicates
    done = 0
    for model in args.models:
        for idea_id in args.ideas:
            idea = IDEAS[idea_id]
            for replicate in range(1, args.replicates + 1):
                done += 1
                print(f"[{done}/{total}] model={model} idea={idea_id} replicate={replicate}", flush=True)
                try:
                    record = run_one(model, idea_id, idea, replicate, args.python)
                except Exception as exc:  # preserve campaign progress
                    record = {
                        "model": model,
                        "idea_id": idea_id,
                        "replicate": replicate,
                        "score": None,
                        "fatal_error": f"{type(exc).__name__}: {exc}",
                    }
                records.append(record)
                print(
                    f"  score={record.get('score')} validation={record.get('validation_errors')} "
                    f"fatal={record.get('fatal_error')}",
                    flush=True,
                )

    summary_path = OUT_DIR / "records.json"
    summary_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {summary_path}", flush=True)


if __name__ == "__main__":
    main()
