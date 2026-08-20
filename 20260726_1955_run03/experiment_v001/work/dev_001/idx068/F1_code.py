import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Transport out cost
    transport_out_options = data["transport_out"]
    out_costs = []
    for opt in transport_out_options:
        kind = opt["kind"]
        price = opt["price"]
        if kind == "flight":
            out_costs.append(price * people)
        elif kind == "taxi":
            out_costs.append(price * math.ceil(people / 4))
        elif kind == "self-driving":
            out_costs.append(price * math.ceil(people / 5))
        else:
            out_costs.append(price * people)  # fallback
    total_out_cost = pick(choices["transport_out"], out_costs)
    
    # Transport back cost
    transport_back_options = data["transport_back"]
    back_costs = []
    for opt in transport_back_options:
        kind = opt["kind"]
        price = opt["price"]
        if kind == "flight":
            back_costs.append(price * people)
        elif kind == "taxi":
            back_costs.append(price * math.ceil(people / 4))
        elif kind == "self-driving":
            back_costs.append(price * math.ceil(people / 5))
        else:
            back_costs.append(price * people)
    total_back_cost = pick(choices["transport_back"], back_costs)
    
    # Hotel cost
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        max_occ = h["max_occupancy"]
        hotel_costs.append(h["price"] * math.ceil(people / max_occ) * nights)
    total_hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs (9 meals)
    meal_keys = [
        "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
        "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
        "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"
    ]
    restaurant_options = data["restaurants"]
    meal_costs = []
    for key in meal_keys:
        costs = [r["avg_cost"] * people for r in restaurant_options]
        meal_costs.append(pick(choices[key], costs))
    
    total_cost = total_out_cost + total_back_cost + total_hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # Hotel not shared room
    hotel_idx = choices["hotel"]
    allowed_hotel_indices = [i for i, h in enumerate(hotel_options) if h["room_type"] != "Shared room"]
    s.add(z3.Or([hotel_idx == i for i in allowed_hotel_indices]))
    
    # All 9 restaurants pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    for i in range(len(meal_vars)):
        for j in range(i+1, len(meal_vars)):
            s.add(meal_vars[i] != meal_vars[j])
    
    # All 3 attractions pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    for i in range(3):
        for j in range(i+1, 3):
            s.add(attr_vars[i] != attr_vars[j])
