"""Workbench v001 frozen prompt builder (free-form condition).

The prompt gives the interface contract, the runtime data schema, the platform
rules (cost formulas, structural validity), and the natural-language query.
It does NOT enumerate the benchmark's local-constraint categories: encoding
every requirement stated in the query is the formalizer's responsibility.
Candidate tables are available to the generated code at runtime via `data`;
they are not inlined in the prompt, so constraints must be encoded generally
(no index hardcoding).
"""

SYSTEM = (
    "You are an expert at formalizing natural-language planning problems as "
    "constraint satisfaction programs using the z3 Python API."
)

TEMPLATE = '''Write a Python function `add_constraints(s, choices, data)` that encodes a 3-day, single-destination travel-planning instance as z3 constraints.

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


def build_prompt(query: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": TEMPLATE.format(query=query)},
    ]
