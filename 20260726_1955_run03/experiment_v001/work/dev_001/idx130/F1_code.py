import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options: list of dicts with "kind" and "price"
        # We'll build a conditional expression using z3.If
        # For each index, compute cost based on kind
        costs = []
        for i, opt in enumerate(options):
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
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        price = h["price"]
        max_occ = h["max_occupancy"]
        cost = price * math.ceil(people / max_occ) * nights
        hotel_costs.append(cost)
    cost_hotel = pick(choices["hotel"], hotel_costs)
    
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
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # 9 meals pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # 3 attractions pairwise distinct
    s.add(z3.Distinct([choices["attr_1"], choices["attr_2"], choices["attr_3"]]))
    
    # Requirement: hotels must allow visitors (house_rules does not contain "No visitors")
    # We'll check each hotel's house_rules string; if it contains "No visitors" (case-insensitive), exclude it.
    allowed_hotel_indices = []
    for i, h in enumerate(data["hotels"]):
        rules = h["house_rules"].lower()
        if "no visitors" not in rules:
            allowed_hotel_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
    
    # Requirement: diverse cuisines including Chinese, Indian, Mexican, Italian
    # We need at least one meal from each of these cuisines across the 9 meals.
    # Each restaurant has a "cuisines" string like "Mexican, Italian, Bakery"
    # We'll find indices of restaurants that contain each required cuisine.
    required_cuisines = ["chinese", "indian", "mexican", "italian"]
    for cuisine in required_cuisines:
        indices = []
        for i, r in enumerate(data["restaurants"]):
            cuisines = r["cuisines"].lower()
            if cuisine in cuisines:
                indices.append(i)
        # At least one meal must be from a restaurant with this cuisine
        s.add(z3.Or([z3.Or([choices[meal_key] == idx for idx in indices]) for meal_key in meal_keys]))
    
    # Requirement: prefer not to self-drive
    # Exclude self-driving options for both transport_out and transport_back
    for transport_key in ["transport_out", "transport_back"]:
        allowed_indices = []
        for i, opt in enumerate(data[transport_key]):
            if opt["kind"] != "self-driving":
                allowed_indices.append(i)
        s.add(z3.Or([choices[transport_key] == i for i in allowed_indices]))