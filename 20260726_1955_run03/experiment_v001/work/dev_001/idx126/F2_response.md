```python
import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options is a list of dicts with "kind" and "price"
        # We'll build a list of possible costs per index
        costs = []
        for opt in options:
            kind = opt["kind"]
            price = opt["price"]
            if kind == "flight":
                cost = price * people
            elif kind == "self-driving":
                cost = price * math.ceil(people / 5)
            elif kind == "taxi":
                cost = price * math.ceil(people / 4)
            else:
                cost = 0  # should not happen
            costs.append(cost)
        return pick(choice_var, costs)
    
    # Transport costs
    cost_out = transport_cost(choices["transport_out"], data["transport_out"])
    cost_back = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        hotel_costs.append(h["price"] * math.ceil(people / h["max_occupancy"]) * nights)
    cost_hotel = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for mk in meal_keys:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[mk], costs))
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # Constraint: no flights for transportation (both directions)
    # For each transport option list, find indices where kind != "flight"
    out_no_flight = [i for i, opt in enumerate(data["transport_out"]) if opt["kind"] != "flight"]
    back_no_flight = [i for i, opt in enumerate(data["transport_back"]) if opt["kind"] != "flight"]
    s.add(z3.Or([choices["transport_out"] == i for i in out_no_flight]))
    s.add(z3.Or([choices["transport_back"] == i for i in back_no_flight]))
    
    # Hotel: must allow children under 10 (i.e., house_rules must NOT contain "No children under 10")
    # Also prefer entire rooms to ourselves -> room_type must be "Entire home/apt"
    allowed_hotel_indices = []
    for i, h in enumerate(data["hotels"]):
        rules = h["house_rules"].lower()
        if "no children under 10" in rules or "no children" in rules:
            continue
        if h["room_type"] != "Entire home/apt":
            continue
        allowed_hotel_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
    
    # All 9 restaurants must be pairwise distinct
    meal_vars = [choices[mk] for mk in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    s.add(z3.Distinct(choices["attr_1"], choices["attr_2"], choices["attr_3"]))
```