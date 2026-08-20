```python
import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options is list of dicts with "kind" and "price"
        # We'll build a conditional sum using pick
        # For each option, compute cost per person based on kind
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
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meal choices must be pairwise distinct
    meal_vars = [choices[mk] for mk in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attraction choices must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Query requirements:
    # 1. Entire home/apt room type (entire rooms)
    hotel_indices = [i for i, h in enumerate(data["hotels"]) if h["room_type"] == "Entire home/apt"]
    s.add(z3.Or([choices["hotel"] == i for i in hotel_indices]))
    
    # 2. Pet-friendly: house_rules must contain "pet" (case-insensitive)
    pet_friendly_indices = [i for i, h in enumerate(data["hotels"]) if "pet" in h["house_rules"].lower()]
    s.add(z3.Or([choices["hotel"] == i for i in pet_friendly_indices]))
    
    # 3. Cuisines: must include French, Mexican, American, Mediterranean across the 9 meals
    # We need at least one meal from each cuisine.
    # For each cuisine, find restaurant indices that have that cuisine in their cuisines string.
    cuisine_requirements = ["French", "Mexican", "American", "Mediterranean"]
    for cuisine in cuisine_requirements:
        allowed = [i for i, r in enumerate(data["restaurants"]) if cuisine.lower() in r["cuisines"].lower()]
        # At least one meal variable must be in allowed
        s.add(z3.Or([z3.Or([choices[mk] == idx for idx in allowed]) for mk in meal_keys]))
```