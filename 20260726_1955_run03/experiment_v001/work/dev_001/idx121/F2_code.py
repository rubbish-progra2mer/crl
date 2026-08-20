import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, transport_list):
        # We'll build a list of costs per option
        costs = []
        for opt in transport_list:
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
    meal_slots = [
        "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
        "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
        "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"
    ]
    total_meal_cost = 0
    for slot in meal_slots:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        total_meal_cost += pick(choices[slot], costs)
    
    # Total cost constraint
    total_cost = out_cost + back_cost + hotel_cost + total_meal_cost
    s.add(total_cost <= budget)
    
    # Hotel constraints: entire room and visitor-friendly
    hotel_idx = choices["hotel"]
    allowed_hotels = []
    for i, h in enumerate(data["hotels"]):
        room_type = h["room_type"]
        house_rules = h["house_rules"]
        # entire room: room_type == "Entire home/apt"
        # visitor-friendly: house_rules must NOT contain "No visitors"
        if room_type == "Entire home/apt" and "No visitors" not in house_rules:
            allowed_hotels.append(i)
    s.add(z3.Or([hotel_idx == i for i in allowed_hotels]))
    
    # Transportation: no self-driving (both directions)
    for direction in ["transport_out", "transport_back"]:
        choice_var = choices[direction]
        allowed = []
        for i, opt in enumerate(data[direction]):
            if opt["kind"] != "self-driving":
                allowed.append(i)
        s.add(z3.Or([choice_var == i for i in allowed]))
    
    # All 9 restaurants must be pairwise distinct
    meal_vars = [choices[slot] for slot in meal_slots]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))