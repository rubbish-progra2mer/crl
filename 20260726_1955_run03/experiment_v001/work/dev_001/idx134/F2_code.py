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
    cost_out = transport_cost(choices["transport_out"], data["transport_out"])
    cost_back = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost
    hotel_choices = data["hotels"]
    hotel_costs = []
    for h in hotel_choices:
        price = h["price"]
        max_occ = h["max_occupancy"]
        cost = price * math.ceil(people / max_occ) * nights
        hotel_costs.append(cost)
    cost_hotel = pick(choices["hotel"], hotel_costs)
    
    # Meal costs (9 meals)
    meal_keys = [
        "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
        "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
        "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"
    ]
    meal_costs = []
    for mk in meal_keys:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[mk], costs))
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # Constraint: no self-driving for both transport directions
    # For each direction, disallow self-driving options
    for direction in ["transport_out", "transport_back"]:
        allowed = []
        for i, opt in enumerate(data[direction]):
            if opt["kind"] != "self-driving":
                allowed.append(i)
        s.add(z3.Or([choices[direction] == i for i in allowed]))
    
    # Hotel must allow smoking: house_rules must NOT contain "No smoking"
    hotel_allowed = []
    for i, h in enumerate(data["hotels"]):
        if "No smoking" not in h["house_rules"]:
            hotel_allowed.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in hotel_allowed]))
    
    # Required cuisines: American, Italian, Mediterranean, Mexican
    required_cuisines = ["American", "Italian", "Mediterranean", "Mexican"]
    # For each cuisine, at least one of the 9 chosen restaurants must have it
    for cuisine in required_cuisines:
        cuisine_conditions = []
        for mk in meal_keys:
            # For each restaurant index, check if cuisine is in its cuisines string
            for i, r in enumerate(data["restaurants"]):
                if cuisine in r["cuisines"]:
                    cuisine_conditions.append(choices[mk] == i)
        s.add(z3.Or(cuisine_conditions))
    
    # Pairwise distinct restaurants (9 meals)
    meal_vars = [choices[mk] for mk in meal_keys]
    for i in range(len(meal_vars)):
        for j in range(i+1, len(meal_vars)):
            s.add(meal_vars[i] != meal_vars[j])
    
    # Pairwise distinct attractions (3 attractions)
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    for i in range(3):
        for j in range(i+1, 3):
            s.add(attr_vars[i] != attr_vars[j])