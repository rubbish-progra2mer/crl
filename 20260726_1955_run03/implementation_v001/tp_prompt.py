"""Implementation v001 frozen prompt templates.

F1 (free-form): identical semantics to workbench_v001/wb_prompt.py — the
category-blind condition under which the masking phenomenon was first
observed on W-bucket data.
F2 (checklist): F1 plus a single category-enumeration paragraph; the cheapest
practitioner mitigation, run as a bundle-disclosed secondary contrast.
A3 (self-check): category-checklist-aided same-model audit of the F1 code —
a deliberately favorable variant of the P052-family self-assessment.
"""

SYSTEM = (
    "You are an expert at formalizing natural-language planning problems as "
    "constraint satisfaction programs using the z3 Python API."
)

F1_TEMPLATE = '''Write a Python function `add_constraints(s, choices, data)` that encodes a 3-day, single-destination travel-planning instance as z3 constraints.

The harness already created integer decision variables (z3 Int) with correct domain bounds in the dict `choices`. The complete key list is:
- "transport_out", "transport_back": index into data["transport_out"] / data["transport_back"] (lists of options; each option has "kind" in {{"flight","self-driving","taxi"}} and "price").
- "hotel": index into data["hotels"] (each: "name", "price", "room_type" in {{"Entire home/apt","Private room","Shared room"}}, "house_rules" string like "No parties & No smoking", "max_occupancy").
- "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner", "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner", "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner": index into data["restaurants"] (each: "name", "avg_cost", "cuisines" string like "Mexican, Italian, Bakery").
- "attr_1", "attr_2", "attr_3": index into data["attractions"].

Other runtime fields: data["people"] (int), data["nights"] = 2, data["budget"] (float).

A global helper `pick(choice_var, values)` is available in your function's namespace: given a choices variable and a plain Python list of numeric values (one per option index), it returns the z3 expression selecting the value at the chosen index. Use it to build cost expressions; never index a Python list with a z3 variable directly. To constrain membership in an index set, use z3.Or([choice_var == i for i in allowed_indices]).

Platform rules that every valid plan must satisfy:
1. Total cost must not exceed the budget stated in the query. Cost formula:
   - flight option: price * people; taxi option: price * ceil(people/4); self-driving option: price * ceil(people/5);
   - hotel: price * ceil(people / max_occupancy) * nights;
   - each meal: restaurant avg_cost * people.
2. The 9 chosen restaurants must be pairwise distinct.
3. The 3 chosen attractions must be pairwise distinct.
4. Every other requirement stated in the query below must also be enforced as constraints over `choices`, using the option attributes available in `data`.

Query:
"""{query}"""

Rules for your code:
- Define exactly `def add_constraints(s, choices, data):` adding assertions to solver `s` via `s.add(...)`. Do not create new decision variables for plan slots; use `choices`. Auxiliary z3 expressions are fine.
- Use only `z3` and the Python standard library (`math` etc. as needed).
- Do not call `s.check()`, do not print, do not read files.
- Reply with ONLY one Python code block.
'''

F2_CHECKLIST_PARAGRAPH = '''
Checklist of requirement kinds that travel queries may state (encode each one that appears in this query): a total budget cap; a required house rule (e.g. the group wants to allow parties / smoking / children under 10 / visitors / pets, so the hotel must NOT list "No <rule>"); a required room type (entire room / private room / shared room / not shared room); required cuisines that must each appear in at least one chosen restaurant across the trip; a transportation-mode restriction ("no flight" or "no self-driving" applies to both directions).
'''


def build_f1(query: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": F1_TEMPLATE.format(query=query)},
    ]


def build_f2(query: str) -> list[dict]:
    content = F1_TEMPLATE.format(query=query)
    marker = "Query:\n"
    content = content.replace(marker, F2_CHECKLIST_PARAGRAPH + "\n" + marker, 1)
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": content},
    ]


A3_SYSTEM = "You are a careful code auditor for constraint-satisfaction programs."

A3_TEMPLATE = '''Below are a travel-planning request and a Python function that is supposed to encode it (plus platform rules: a budget cap computed from fixed cost formulas, pairwise-distinct restaurants, pairwise-distinct attractions) as z3 constraints.

Query:
"""{query}"""

Code:
```python
{code}
```

For each category below, answer whether the query (or the platform rules) states such a requirement for this instance, and whether the code actually enforces it. Answer with ONLY a JSON object of exactly this shape:
{{"budget": {{"stated": true, "enforced": true}}, "house_rule": {{"stated": false, "enforced": false}}, "room_type": {{"stated": false, "enforced": false}}, "cuisine": {{"stated": false, "enforced": false}}, "transportation": {{"stated": false, "enforced": false}}, "distinct_restaurants": {{"stated": true, "enforced": true}}, "distinct_attractions": {{"stated": true, "enforced": true}}}}

Meanings: "house_rule" = the group wants some rule allowed (hotel must not list "No <rule>"); "room_type" = a required room type; "cuisine" = each named cuisine must appear in at least one chosen restaurant; "transportation" = "no flight" / "no self-driving" for both directions. Set "enforced" to true only if the code as written actually guarantees the requirement for every solution.'''


def build_a3(query: str, code: str) -> list[dict]:
    return [
        {"role": "system", "content": A3_SYSTEM},
        {"role": "user", "content": A3_TEMPLATE.format(query=query, code=code)},
    ]
