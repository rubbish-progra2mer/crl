import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
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
                cost = 0
            costs.append(cost)
        return pick(choice_var, costs)
    
    # Transport costs
    out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_costs = []
    for h in data["hotels"]:
        hotel_costs.append(h["price"] * math.ceil(people / h["max_occupancy"]) * nights)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for mk in meal_keys:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[mk], costs))
    
    total_cost = out_cost + back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meals must be pairwise distinct
    meal_vars = [choices[mk] for mk in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Query constraints:
    # 1. Accommodations suitable for children under 10 -> entire home/apt or private room (not shared room)
    #    Also "prefer entire rooms" -> we enforce entire home/apt only
    hotel_room_types = [h["room_type"] for h in data["hotels"]]
    allowed_hotel_indices = [i for i, rt in enumerate(hotel_room_types) if rt == "Entire home/apt"]
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
    
    # 2. "don't need to self-drive" -> no self-driving transport options
    # For transport_out
    out_kinds = [opt["kind"] for opt in data["transport_out"]]
    allowed_out = [i for i, k in enumerate(out_kinds) if k != "self-driving"]
    s.add(z3.Or([choices["transport_out"] == i for i in allowed_out]))
    
    # For transport_back
    back_kinds = [opt["kind"] for opt in data["transport_back"]]
    allowed_back = [i for i, k in enumerate(back_kinds) if k != "self-driving"]
    s.add(z3.Or([choices["transport_back"] == i for i in allowed_back]))
