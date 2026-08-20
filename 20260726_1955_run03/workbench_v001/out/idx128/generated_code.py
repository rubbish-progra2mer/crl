import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options: list of dicts with "kind" and "price"
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
    
    # All 9 meal choices must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attraction choices must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Query constraints:
    # 1. Not self-driving: both transport options must not be "self-driving"
    for transport_key in ["transport_out", "transport_back"]:
        allowed = [i for i, opt in enumerate(data[transport_key]) if opt["kind"] != "self-driving"]
        s.add(z3.Or([choices[transport_key] == i for i in allowed]))
    
    # 2. Accommodations suitable for children under 10:
    #    - room_type must be "Entire home/apt" (most suitable for families)
    #    - house_rules must not contain "No children" or "No kids" (we'll check for "No parties" is fine, but we need to ensure no explicit child restrictions)
    #    We'll interpret "suitable for children" as: room_type is "Entire home/apt" and house_rules does not contain "No children" or "No kids".
    #    Since house_rules is a string like "No parties & No smoking", we'll check that it does not contain "No children" or "No kids".
    hotel_allowed = []
    for i, h in enumerate(data["hotels"]):
        rules = h["house_rules"].lower()
        if h["room_type"] == "Entire home/apt" and "no children" not in rules and "no kids" not in rules:
            hotel_allowed.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in hotel_allowed]))
    
    # 3. Dietary preferences: Mediterranean, Mexican, French, Indian cuisines.
    #    At least one meal per cuisine? The query says "food recommendations that cater to these preferences".
    #    We'll require that for each of the four cuisines, at least one chosen restaurant has that cuisine.
    #    Cuisines field is a comma-separated string like "Mexican, Italian, Bakery".
    cuisine_list = ["mediterranean", "mexican", "french", "indian"]
    for cuisine in cuisine_list:
        # For each meal variable, we need at least one that includes this cuisine
        # We'll create a constraint that the union of all meal choices includes at least one restaurant with this cuisine.
        # Since we have 9 meals, we can require that at least one meal index corresponds to a restaurant whose cuisines contain the target.
        # We'll use z3.Or over all meal variables.
        meal_cuisine_conditions = []
        for meal_var in meal_vars:
            # For each restaurant index, check if it has the cuisine
            restaurant_indices_with_cuisine = [i for i, r in enumerate(data["restaurants"]) if cuisine in r["cuisines"].lower()]
            if restaurant_indices_with_cuisine:
                meal_cuisine_conditions.append(z3.Or([meal_var == i for i in restaurant_indices_with_cuisine]))
        if meal_cuisine_conditions:
            s.add(z3.Or(meal_cuisine_conditions))
    
    # Note: The query says "We'll be traveling with children under 10" – we already handled accommodation.
    # Also "departing from Newark and visiting Savannah" – no specific constraint needed, just context.
    # "March 3rd to March 5th, 2022" – no constraint needed.
    # Budget already enforced.
    # No self-driving already enforced.
    # All other constraints are covered.