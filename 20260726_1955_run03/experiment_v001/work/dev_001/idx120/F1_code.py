import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options: list of dicts with "kind" and "price"
        # We'll build a conditional expression using pick
        # For each option, compute the cost based on kind
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
        hotel_costs.append(price * math.ceil(people / max_occ) * nights)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_keys = [
        "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
        "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
        "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"
    ]
    meal_costs = []
    for mk in meal_keys:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[mk], costs))
    
    # Total cost constraint
    total_cost = out_cost + back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meals must be pairwise distinct
    meal_vars = [choices[mk] for mk in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Query requirements:
    # 1. Accommodations that allow pets and provide entire rooms
    #    "allow pets" -> house_rules does not contain "No pets" (case-insensitive)
    #    "entire rooms" -> room_type == "Entire home/apt"
    allowed_hotel_indices = []
    for i, h in enumerate(data["hotels"]):
        rules_lower = h["house_rules"].lower()
        if "no pets" not in rules_lower and h["room_type"] == "Entire home/apt":
            allowed_hotel_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
    
    # 2. Meals: group enjoys Indian, Chinese, Mediterranean, American cuisines
    #    Each chosen restaurant must have at least one of these cuisines
    #    cuisines field is a string like "Mexican, Italian, Bakery"
    target_cuisines = {"indian", "chinese", "mediterranean", "american"}
    for mk in meal_keys:
        allowed_rest_indices = []
        for i, r in enumerate(data["restaurants"]):
            cuisines = [c.strip().lower() for c in r["cuisines"].split(",")]
            if any(c in target_cuisines for c in cuisines):
                allowed_rest_indices.append(i)
        s.add(z3.Or([choices[mk] == i for i in allowed_rest_indices]))
    
    # Note: No additional constraints about attractions or transport were specified in the query.
