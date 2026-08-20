import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # Build list of costs per option index
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
    hotel_costs = []
    for h in data["hotels"]:
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
    
    # All 9 meals must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # 3 attractions must be pairwise distinct
    s.add(z3.Distinct([choices["attr_1"], choices["attr_2"], choices["attr_3"]]))
    
    # Hotel: room_type not shared (i.e., "Entire home/apt" or "Private room")
    allowed_hotel_indices = [i for i, h in enumerate(data["hotels"]) if h["room_type"] != "Shared room"]
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
    
    # No self-driving: transport_out and transport_back must not be "self-driving"
    allowed_transport_indices = []
    for opt_list_name in ["transport_out", "transport_back"]:
        allowed = [i for i, opt in enumerate(data[opt_list_name]) if opt["kind"] != "self-driving"]
        allowed_transport_indices.append(allowed)
    s.add(z3.Or([choices["transport_out"] == i for i in allowed_transport_indices[0]]))
    s.add(z3.Or([choices["transport_back"] == i for i in allowed_transport_indices[1]]))
    
    # Cuisines: each meal must be from a restaurant that offers at least one of Mexican, Chinese, Mediterranean, American
    # Build list of allowed restaurant indices (those whose cuisines contain any of the desired cuisines)
    desired_cuisines = {"mexican", "chinese", "mediterranean", "american"}
    allowed_restaurant_indices = []
    for i, r in enumerate(data["restaurants"]):
        cuisines = [c.strip().lower() for c in r["cuisines"].split(",")]
        if any(c in desired_cuisines for c in cuisines):
            allowed_restaurant_indices.append(i)
    # Each meal must be from allowed restaurants
    for key in meal_keys:
        s.add(z3.Or([choices[key] == i for i in allowed_restaurant_indices]))