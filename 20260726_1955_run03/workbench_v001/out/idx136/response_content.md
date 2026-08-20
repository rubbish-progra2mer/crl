```python
import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options: list of dicts with "kind" and "price"
        # We'll build a z3 expression using pick
        costs = []
        for opt in options:
            kind = opt["kind"]
            price = opt["price"]
            if kind == "flight":
                cost = price * people
            elif kind == "taxi":
                cost = price * math.ceil(people / 4)
            elif kind == "self-driving":
                cost = price * math.ceil(people / 5)
            else:
                cost = price * people  # fallback
            costs.append(cost)
        return pick(choice_var, costs)
    
    # Transport costs
    out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        price = h["price"]
        max_occ = h["max_occupancy"]
        cost = price * math.ceil(people / max_occ) * nights
        hotel_costs.append(cost)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_keys = [
        "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
        "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
        "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"
    ]
    meal_costs = []
    for key in meal_keys:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[key], costs))
    
    # Total cost constraint
    total_cost = out_cost + back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # 9 meals pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # 3 attractions pairwise distinct
    s.add(z3.Distinct([choices["attr_1"], choices["attr_2"], choices["attr_3"]]))
    
    # Query requirements:
    # "accommodations that allow children under 10" -> house_rules must not contain "No children"
    # "private rooms" -> room_type == "Private room"
    # "not planning on self-driving" -> no self-driving transport options
    hotel_idx = choices["hotel"]
    allowed_hotel_indices = []
    for i, h in enumerate(data["hotels"]):
        rules = h["house_rules"].lower()
        if "no children" in rules or "no child" in rules:
            continue
        if h["room_type"] != "Private room":
            continue
        allowed_hotel_indices.append(i)
    s.add(z3.Or([hotel_idx == i for i in allowed_hotel_indices]))
    
    # No self-driving for transport
    for direction in ["transport_out", "transport_back"]:
        choice_var = choices[direction]
        options = data[direction]
        allowed = [i for i, opt in enumerate(options) if opt["kind"] != "self-driving"]
        s.add(z3.Or([choice_var == i for i in allowed]))