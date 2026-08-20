import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options: list of dicts with "kind" and "price"
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
                cost = 0  # should not happen
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
    
    total_cost = out_cost + back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meals must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Requirement: accommodations must be entire rooms (room_type == "Entire home/apt")
    hotel_idx = choices["hotel"]
    entire_home_indices = [i for i, h in enumerate(hotel_options) if h["room_type"] == "Entire home/apt"]
    s.add(z3.Or([hotel_idx == i for i in entire_home_indices]))
    
    # Requirement: visitor-friendly (house_rules should not contain "No parties" or "No smoking"? 
    # The query says "visitor-friendly", which we interpret as no restrictive rules like "No parties" or "No smoking".
    # We'll filter hotels that do NOT have "No parties" or "No smoking" in house_rules.
    visitor_friendly_indices = []
    for i, h in enumerate(hotel_options):
        rules = h["house_rules"].lower()
        if "no parties" not in rules and "no smoking" not in rules:
            visitor_friendly_indices.append(i)
    s.add(z3.Or([hotel_idx == i for i in visitor_friendly_indices]))
    
    # Requirement: prefer not to drive ourselves -> no self-driving transport
    # For transport_out
    out_no_self_drive = [i for i, opt in enumerate(data["transport_out"]) if opt["kind"] != "self-driving"]
    s.add(z3.Or([choices["transport_out"] == i for i in out_no_self_drive]))
    # For transport_back
    back_no_self_drive = [i for i, opt in enumerate(data["transport_back"]) if opt["kind"] != "self-driving"]
    s.add(z3.Or([choices["transport_back"] == i for i in back_no_self_drive]))