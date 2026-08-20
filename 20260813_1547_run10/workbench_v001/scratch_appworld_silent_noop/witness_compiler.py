from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


CONTROL_FIELDS = {
    "access_token",
    "password",
    "page_index",
    "page_limit",
    "sort_by",
}
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
READ_METHODS = {"GET"}
ROLE_BY_WRITE_VERB = {
    "send": "receiver",
    "transfer": "receiver",
    "pay": "receiver",
    "add": "target",
    "create": "target",
    "update": "target",
    "delete": "target",
    "remove": "target",
}


def _singular(token: str) -> str:
    if token.endswith("ies") and len(token) > 3:
        return token[:-3] + "y"
    if token.endswith("ses") and len(token) > 3:
        return token[:-2]
    if token.endswith("s") and not token.endswith("ss") and len(token) > 2:
        return token[:-1]
    return token


def tokens(text: str) -> tuple[str, ...]:
    pieces = re.findall(r"[A-Za-z0-9]+", re.sub(r"([a-z])([A-Z])", r"\1 \2", text))
    return tuple(_singular(piece.lower()) for piece in pieces if piece)


def _token_set(text: str) -> set[str]:
    return set(tokens(text))


def _compatible_type(parameter_type: str, example: Any) -> bool:
    if example is None:
        return True
    if parameter_type == "boolean":
        return isinstance(example, bool)
    if parameter_type == "integer":
        return isinstance(example, int) and not isinstance(example, bool)
    if parameter_type == "number":
        return isinstance(example, int | float) and not isinstance(example, bool)
    if parameter_type == "string":
        return isinstance(example, str)
    return True


def _flatten_schema(schema: Any, prefix: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], Any]]:
    if isinstance(schema, Mapping):
        leaves: list[tuple[tuple[str, ...], Any]] = []
        for key, value in schema.items():
            leaves.extend(_flatten_schema(value, prefix + (str(key),)))
        return leaves
    if isinstance(schema, list):
        if not schema:
            return [(prefix, [])]
        return _flatten_schema(schema[0], prefix + ("[]",))
    return [(prefix, schema)]


def _path_tokens(path: Sequence[str]) -> set[str]:
    output: set[str] = set()
    for component in path:
        if component != "[]":
            output.update(tokens(component))
    return output


def _name_match_score(source_name: str, target_path: Sequence[str]) -> float:
    source = _token_set(source_name)
    target = _path_tokens(target_path)
    if not source or not target:
        return 0.0
    overlap = len(source & target)
    if overlap == 0:
        return 0.0
    coverage = overlap / len(source)
    precision = overlap / len(target)
    return 0.7 * coverage + 0.3 * precision


def _parameter_match_score(source_name: str, target_name: str) -> float:
    source = _token_set(source_name)
    target = _token_set(target_name)
    if not source or not target:
        return 0.0
    overlap = len(source & target)
    if overlap == 0:
        return 0.0
    return 0.6 * overlap / len(target) + 0.4 * overlap / len(source)


def _path_overlap(left: str, right: str) -> float:
    left_tokens = _token_set(left)
    right_tokens = _token_set(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def _write_role(write_doc: Mapping[str, Any]) -> str | None:
    leading_tokens = tokens(str(write_doc.get("api_name", ""))) + tokens(
        str(write_doc.get("description", ""))
    )
    for token in leading_tokens:
        if token in ROLE_BY_WRITE_VERB:
            return ROLE_BY_WRITE_VERB[token]
    return None


@dataclass(frozen=True)
class Binding:
    parameter: str
    source: str
    source_field: str
    score: float


@dataclass(frozen=True)
class Relation:
    source_field: str
    response_path: tuple[str, ...]
    operator: str
    score: float


@dataclass(frozen=True)
class WitnessPlan:
    app_name: str
    write_api: str
    read_api: str
    bindings: tuple[Binding, ...]
    relations: tuple[Relation, ...]
    score: float
    root_is_collection: bool
    provenance: str = "public_tool_docs+instantiated_write_call"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _best_binding(
    parameter: Mapping[str, Any],
    write_arguments: Mapping[str, Any],
    write_response: Mapping[str, Any],
) -> Binding | None:
    target_name = str(parameter["name"])
    candidates: list[Binding] = []
    for source, values in (("request", write_arguments), ("response", write_response)):
        for source_name, value in values.items():
            if not _compatible_type(str(parameter.get("type", "")), value):
                continue
            score = _parameter_match_score(source_name, target_name)
            if score <= 0:
                continue
            if source_name == target_name:
                score += 1.0
            if source == "request":
                score += 0.15
            candidates.append(Binding(target_name, source, source_name, round(score, 4)))
    if not candidates:
        return None
    return max(candidates, key=lambda item: (item.score, item.source == "request"))


def _relations(
    write_doc: Mapping[str, Any],
    read_doc: Mapping[str, Any],
    write_arguments: Mapping[str, Any],
) -> tuple[Relation, ...]:
    success_schema = read_doc.get("response_schemas", {}).get("success")
    leaves = _flatten_schema(success_schema)
    role = _write_role(write_doc)
    output: list[Relation] = []
    used_paths: set[tuple[str, ...]] = set()
    for source_name, source_value in write_arguments.items():
        if source_name in CONTROL_FIELDS or source_value is None:
            continue
        ranked: list[Relation] = []
        for path, schema_example in leaves:
            if not _compatible_type(
                "boolean"
                if isinstance(schema_example, bool)
                else "integer"
                if isinstance(schema_example, int)
                else "number"
                if isinstance(schema_example, float)
                else "string"
                if isinstance(schema_example, str)
                else "",
                source_value,
            ):
                continue
            score = _name_match_score(source_name, path)
            if score < 0.7:
                continue
            path_tokens = _path_tokens(path)
            if role == "receiver" and "receiver" in path_tokens:
                score += 0.2
            if role == "receiver" and "sender" in path_tokens:
                score -= 0.2
            normalized_path = path[1:] if path and path[0] == "[]" else path
            operator = "contains" if "[]" in normalized_path else "equals"
            ranked.append(
                Relation(source_name, normalized_path, operator, round(score, 4))
            )
        if ranked:
            best = max(ranked, key=lambda item: item.score)
            if best.response_path not in used_paths:
                used_paths.add(best.response_path)
                output.append(best)
    return tuple(output)


def compile_witness(
    app_docs: Mapping[str, Mapping[str, Any]],
    write_api: str,
    write_arguments: Mapping[str, Any],
    write_response: Mapping[str, Any],
) -> WitnessPlan | None:
    write_doc = app_docs[write_api]
    if str(write_doc.get("method", "")).upper() not in WRITE_METHODS:
        raise ValueError(f"{write_api} is not a state-changing operation.")
    candidates: list[WitnessPlan] = []
    for read_api, read_doc in app_docs.items():
        if str(read_doc.get("method", "")).upper() not in READ_METHODS:
            continue
        bindings: list[Binding] = []
        executable = True
        request_anchor_count = 0
        for parameter in read_doc.get("parameters", []):
            binding = _best_binding(parameter, write_arguments, write_response)
            if binding is not None:
                if binding.score >= 0.7 or bool(parameter.get("required")):
                    bindings.append(binding)
                    if binding.source == "request" and binding.source_field not in CONTROL_FIELDS:
                        request_anchor_count += 1
            elif bool(parameter.get("required")):
                executable = False
                break
        if not executable:
            continue
        relations = _relations(write_doc, read_doc, write_arguments)
        if not relations:
            continue
        root_is_collection = isinstance(
            read_doc.get("response_schemas", {}).get("success"), list
        )
        score = (
            3.0 * _path_overlap(str(write_doc.get("path", "")), str(read_doc.get("path", "")))
            + sum(relation.score for relation in relations)
            + 0.4 * len(relations)
            + 0.75 * request_anchor_count
            - 0.25 * sum(binding.source == "response" for binding in bindings)
            - (0.15 if root_is_collection else 0.0)
        )
        candidates.append(
            WitnessPlan(
                app_name=str(write_doc["app_name"]),
                write_api=write_api,
                read_api=read_api,
                bindings=tuple(bindings),
                relations=relations,
                score=round(score, 4),
                root_is_collection=root_is_collection,
            )
        )
    if not candidates:
        return None
    return max(candidates, key=lambda item: (item.score, len(item.relations)))


def resolve_bindings(
    plan: WitnessPlan,
    write_arguments: Mapping[str, Any],
    write_response: Mapping[str, Any],
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for binding in plan.bindings:
        values = write_arguments if binding.source == "request" else write_response
        output[binding.parameter] = values[binding.source_field]
    return output


def _extract_path(value: Any, path: Sequence[str]) -> list[Any]:
    values = [value]
    for component in path:
        next_values: list[Any] = []
        if component == "[]":
            for item in values:
                if isinstance(item, Sequence) and not isinstance(item, str | bytes):
                    next_values.extend(item)
            values = next_values
            continue
        for item in values:
            if isinstance(item, Mapping) and component in item:
                next_values.append(item[component])
            elif hasattr(item, component):
                next_values.append(getattr(item, component))
        values = next_values
    return values


def _item_satisfies(
    plan: WitnessPlan,
    item: Any,
    write_arguments: Mapping[str, Any],
) -> bool:
    for relation in plan.relations:
        observed = _extract_path(item, relation.response_path)
        expected = write_arguments[relation.source_field]
        if relation.operator == "equals" and not any(value == expected for value in observed):
            return False
        if relation.operator == "contains" and expected not in observed:
            return False
    return True


def evaluate_witness(
    plan: WitnessPlan,
    read_response: Any,
    write_arguments: Mapping[str, Any],
) -> bool:
    if plan.root_is_collection:
        if not isinstance(read_response, Sequence) or isinstance(read_response, str | bytes):
            return False
        return any(_item_satisfies(plan, item, write_arguments) for item in read_response)
    return _item_satisfies(plan, read_response, write_arguments)
