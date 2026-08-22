"""Compute EM, token F1, and cover EM from prediction JSONL files."""

from __future__ import annotations

import argparse
import re
import string
from collections import Counter

from jsonl_io import read_jsonl


def normalize(text: str) -> str:
    text = text.lower()
    text = "".join(character for character in text if character not in string.punctuation)
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())


def f1(prediction: str, answer: str) -> float:
    predicted = normalize(prediction).split()
    gold = normalize(answer).split()
    common = sum((Counter(predicted) & Counter(gold)).values())
    if not predicted or not gold:
        return float(predicted == gold)
    if common == 0:
        return 0.0
    precision = common / len(predicted)
    recall = common / len(gold)
    return 2 * precision * recall / (precision + recall)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--answers", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    predictions = {str(row["id"]): row["prediction"] for row in read_jsonl(args.predictions)}
    rows = list(read_jsonl(args.answers))
    em_values, f1_values, cem_values = [], [], []
    for row in rows:
        prediction = predictions.get(str(row["id"]), "")
        answers = row.get("answers", [row.get("answer", "")])
        em_values.append(max(float(normalize(prediction) == normalize(answer)) for answer in answers))
        f1_values.append(max(f1(prediction, answer) for answer in answers))
        cem_values.append(max(float(normalize(answer) in normalize(prediction)) for answer in answers))
    count = len(rows)
    if count == 0:
        raise ValueError("answer file is empty")
    print({"count": count, "em": sum(em_values) / count, "f1": sum(f1_values) / count, "cem": sum(cem_values) / count})


if __name__ == "__main__":
    main()
