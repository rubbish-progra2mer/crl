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
            if opt["kind"] == "flight":
                cost = opt["price"] * people
            elif opt["kind"] == "taxi":
                cost = opt["price"] * math.ceil(people / 4)
            elif opt["kind"] == "self-driving":
                cost = opt["price"] * math.ceil(people / 5)
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
        cost = h["price"] * math.ceil(people / h["max_occupancy"]) * nights
        hotel_costs.append(cost)
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
    
    # Hotel constraints: allow smoking and not shared room
    hotel_idx = choices["hotel"]
    allowed_hotel_indices = []
    for i, h in enumerate(hotel_options):
        rules = h["house_rules"].lower()
        if "no smoking" in rules:
            continue
        if h["room_type"] == "Shared room":
            continue
        allowed_hotel_indices.append(i)
    s.add(z3.Or([hotel_idx == i for i in allowed_hotel_indices]))
    
    # Cuisine preference: each meal must be from a restaurant that serves at least one of French, Mediterranean, Mexican, Chinese
    cuisine_keywords = ["french", "mediterranean", "mexican", "chinese"]
    for mk in meal_keys:
        meal_var = choices[mk]
        allowed_meal_indices = []
        for i, r in enumerate(data["restaurants"]):
            cuisines = r["cuisines"].lower()
            if any(cuisine in cuisines for cuisine in cuisine_keywords):
                allowed_meal_indices.append(i)
        s.add(z3.Or([meal_var == i for i in allowed_meal_indices]))