from program import (
    calendar_contract_violations,
    levenshtein_one,
    path_dependency_violations,
    reference_calls,
    schema_reference_violations,
    unit_contract_violations,
)


def test_schema_reference_nested_key_mismatch():
    row = {
        "function": [
            {
                "name": "control",
                "parameters": {
                    "properties": {
                        "body": {"properties": {"currentMode": {"type": "string"}}}
                    }
                },
            }
        ]
    }
    calls = [("control", {"body": [{"oldMode": ["COOL"]}]})]
    assert schema_reference_violations(row, calls) == 1


def test_reference_call_parser():
    calls = reference_calls([["touch(file_name='statistics.txt')"]])
    assert calls == [("touch", {"file_name": "statistics.txt"})]


def test_path_near_collision():
    calls = [
        ("touch", {"file_name": "statistics.txt"}),
        ("echo", {"file_name": "statistics.txt."}),
    ]
    assert path_dependency_violations(calls) == 1
    assert levenshtein_one("statistics.txt", "statistics.txt.")


def test_unit_contract_conflict():
    row = {
        "function": [
            {
                "name": "area",
                "parameters": {
                    "properties": {
                        "base": {"description": "base in meters"},
                        "height": {"description": "height in meters"},
                    }
                },
            }
        ]
    }
    assert unit_contract_violations(row, "25 feet and 30 meters") == 1


def test_calendar_contract_conflict():
    assert calendar_contract_violations("Thursday April 25th 2023") == 1
    assert calendar_contract_violations("Tuesday April 25th 2023") == 0
