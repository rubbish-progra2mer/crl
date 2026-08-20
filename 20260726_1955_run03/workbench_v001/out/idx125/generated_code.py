import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options is list of dicts with "kind" and "price"
        # We'll build a list of possible costs per index
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
    cost_out = transport_cost(choices["transport_out"], data["transport_out"])
    cost_back = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_costs = []
    for h in data["hotels"]:
        price = h["price"]
        max_occ = h["max_occupancy"]
        cost = price * math.ceil(people / max_occ) * nights
        hotel_costs.append(cost)
    cost_hotel = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for key in meal_keys:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[key], costs))
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # 9 meals pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # 3 attractions pairwise distinct
    s.add(z3.Distinct(choices["attr_1"], choices["attr_2"], choices["attr_3"]))
    
    # Requirement: accommodations that allow smoking
    # house_rules string contains "No smoking" -> not allowed; we need smoking allowed.
    # So we need hotel where "No smoking" is NOT in house_rules.
    smoking_allowed_indices = []
    for i, h in enumerate(data["hotels"]):
        if "No smoking" not in h["house_rules"]:
            smoking_allowed_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in smoking_allowed_indices]))
    
    # Requirement: ideally entire rooms (room_type == "Entire home/apt")
    entire_room_indices = []
    for i, h in enumerate(data["hotels"]):
        if h["room_type"] == "Entire home/apt":
            entire_room_indices.append(i)
    # We'll enforce that the chosen hotel is among those with entire room
    s.add(z3.Or([choices["hotel"] == i for i in entire_room_indices]))
    
    # Requirement: not self-driving during this trip
    # So transport_out and transport_back must not be self-driving
    not_self_driving_out = []
    for i, opt in enumerate(data["transport_out"]):
        if opt["kind"] != "self-driving":
            not_self_driving_out.append(i)
    s.add(z3.Or([choices["transport_out"] == i for i in not_self_driving_out]))
    
    not_self_driving_back = []
    for i, opt in enumerate(data["transport_back"]):
        if opt["kind"] != "self-driving":
            not_self_driving_back.append(i)
    s.add(z3.Or([choices["transport_back"] == i for i in not_self_driving_back]))
    
    # Cuisine: open to any suggestions, so no constraint needed.
    
    # Note: pick function is assumed available in the namespace.
    # We'll define it locally just in case, but the harness provides it.
    # Actually the harness says it's available, so we don't define it.
    # But to be safe, we can define a local version if not present.
    # However, the problem says it's available, so we rely on that.
    # We'll just use it as is. If not defined, we could define it here.
    # But to avoid NameError, we'll define it locally.
    # Actually the instruction says "A global helper pick(choice_var, values) is available"
    # So we assume it exists. We'll not redefine to avoid confusion.
    pass