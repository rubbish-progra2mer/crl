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
    
    # Hotel cost
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        price = h["price"]
        max_occ = h["max_occupancy"]
        cost = price * math.ceil(people / max_occ) * nights
        hotel_costs.append(cost)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs (9 meals)
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
    
    # All 9 restaurants must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Requirement: traveling with children under 10 -> hotel must NOT have "No children under 10" in house_rules
    # Also "No parties" etc. but specifically children under 10
    allowed_hotel_indices = []
    for i, h in enumerate(hotel_options):
        rules = h["house_rules"].lower()
        if "no children under 10" not in rules:
            allowed_hotel_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
    
    # Requirement: prefer entire rooms -> room_type must be "Entire home/apt"
    entire_room_indices = [i for i, h in enumerate(hotel_options) if h["room_type"] == "Entire home/apt"]
    s.add(z3.Or([choices["hotel"] == i for i in entire_room_indices]))
    
    # Requirement: don't need to self-drive -> no self-driving for both transport directions
    # For each direction, exclude self-driving options
    for direction in ["transport_out", "transport_back"]:
        options = data[direction]
        allowed = [i for i, opt in enumerate(options) if opt["kind"] != "self-driving"]
        s.add(z3.Or([choices[direction] == i for i in allowed]))
