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
    
    # Total cost constraint
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meals must be pairwise distinct
    meal_vars = [choices[mk] for mk in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Query requirements:
    # 1. Accommodations that allow smoking: house_rules must contain "smoking" (case-insensitive)
    hotel_rules = [h["house_rules"].lower() for h in hotel_options]
    allowed_hotels = [i for i, rules in enumerate(hotel_rules) if "smoking" in rules]
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotels]))
    
    # 2. Cuisines: American, Italian, Mediterranean, Mexican must all appear among the 9 chosen restaurants
    # Each restaurant has "cuisines" string like "Mexican, Italian, Bakery"
    # We need to ensure that for each required cuisine, at least one chosen restaurant has it.
    required_cuisines = ["american", "italian", "mediterranean", "mexican"]
    for cuisine in required_cuisines:
        # For each meal variable, check if the chosen restaurant has this cuisine
        cuisine_conditions = []
        for meal_var in meal_vars:
            # For each restaurant index, check if cuisine is in its cuisines list
            restaurant_cuisines = [r["cuisines"].lower() for r in data["restaurants"]]
            # Build a list of booleans: for each index, whether cuisine is present
            has_cuisine = [cuisine in cuisines_str for cuisines_str in restaurant_cuisines]
            # We need to express: meal_var == i for some i where has_cuisine[i] is True
            # Use pick to get a boolean expression? Actually we can use z3.Or with equality
            # But we need to ensure that at least one meal picks such a restaurant.
            # We'll create a condition that this meal_var picks a restaurant with the cuisine.
            condition = z3.Or([z3.And(meal_var == i, True) for i, hc in enumerate(has_cuisine) if hc])
            cuisine_conditions.append(condition)
        # At least one meal must satisfy this cuisine
        s.add(z3.Or(cuisine_conditions))
    
    # 3. No self-driving: exclude self-driving options for both transport_out and transport_back
    # For transport_out
    out_no_self = [i for i, opt in enumerate(data["transport_out"]) if opt["kind"] != "self-driving"]
    s.add(z3.Or([choices["transport_out"] == i for i in out_no_self]))
    # For transport_back
    back_no_self = [i for i, opt in enumerate(data["transport_back"]) if opt["kind"] != "self-driving"]
    s.add(z3.Or([choices["transport_back"] == i for i in back_no_self]))