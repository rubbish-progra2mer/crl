import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options: list of dicts with "kind" and "price"
        # We'll build a z3 expression using pick
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
    cost_out = transport_cost(choices["transport_out"], data["transport_out"])
    cost_back = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        price = h["price"]
        max_occ = h["max_occupancy"]
        hotel_costs.append(price * math.ceil(people / max_occ) * nights)
    cost_hotel = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for mk in meal_keys:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[mk], costs))
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # 9 meals pairwise distinct
    meal_vars = [choices[mk] for mk in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # 3 attractions pairwise distinct
    s.add(z3.Distinct([choices["attr_1"], choices["attr_2"], choices["attr_3"]]))
    
    # No flight bookings for transportation
    # For each transport option, restrict to indices where kind != "flight"
    for direction in ["transport_out", "transport_back"]:
        allowed = [i for i, opt in enumerate(data[direction]) if opt["kind"] != "flight"]
        s.add(z3.Or([choices[direction] == i for i in allowed]))
    
    # Accommodations where pets are allowed
    # We assume "house_rules" contains info; we'll check if "pets" is mentioned (case-insensitive)
    hotel_allowed = []
    for i, h in enumerate(data["hotels"]):
        rules = h.get("house_rules", "").lower()
        if "pets" in rules or "pet" in rules:
            hotel_allowed.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in hotel_allowed]))
    
    # Cuisine requirements: Mediterranean, French, Mexican, Indian
    # Each meal must be from a restaurant that offers at least one of these cuisines
    # We'll build a list of allowed restaurant indices for each cuisine requirement
    # Actually we need all 9 meals to collectively cover these cuisines? The query says:
    # "we're particularly interested in Mediterranean, French, Mexican, and Indian food."
    # This likely means each of these cuisines must appear at least once among the 9 meals.
    # We'll enforce that for each cuisine, at least one meal is from a restaurant that includes it.
    required_cuisines = ["mediterranean", "french", "mexican", "indian"]
    for cuisine in required_cuisines:
        # Find indices of restaurants that have this cuisine in their cuisines string
        allowed_rest = [i for i, r in enumerate(data["restaurants"]) 
                        if cuisine in r["cuisines"].lower()]
        # At least one meal must be from these indices
        s.add(z3.Or([z3.Or([choices[mk] == i for i in allowed_rest]) for mk in meal_keys]))
