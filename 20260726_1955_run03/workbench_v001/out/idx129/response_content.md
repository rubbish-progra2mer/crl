```python
import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        # options: list of dicts with "kind" and "price"
        # We'll build a conditional expression using pick
        # For each option, compute cost per person/group
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
    out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        price = h["price"]
        max_occ = h["max_occupancy"]
        cost = price * math.ceil(people / max_occ) * nights
        hotel_costs.append(cost)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_keys = [
        "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
        "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
        "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"
    ]
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
    
    # Requirement: accommodations that allow parties
    # house_rules string contains "No parties" or "Parties allowed"? 
    # Query says "allow parties", so we need hotels where house_rules does NOT contain "No parties"
    # We'll find indices of hotels that allow parties (i.e., "No parties" not in house_rules)
    party_allowed_indices = [i for i, h in enumerate(data["hotels"]) if "No parties" not in h["house_rules"]]
    s.add(z3.Or([choices["hotel"] == i for i in party_allowed_indices]))
    
    # Requirement: interested in tasting local Mediterranean, American, Chinese, and Indian cuisines
    # That means across the 9 meals, we must have at least one restaurant serving each of these cuisines.
    # Each restaurant has "cuisines" string like "Mexican, Italian, Bakery"
    # We need to ensure that for each required cuisine, there exists at least one meal where the chosen restaurant's cuisines contain that cuisine.
    required_cuisines = ["Mediterranean", "American", "Chinese", "Indian"]
    for cuisine in required_cuisines:
        # For each meal, check if the chosen restaurant's cuisines contain this cuisine
        cuisine_conditions = []
        for mk in meal_keys:
            # For each restaurant index, check if cuisine is in its cuisines
            restaurant_indices_with_cuisine = [i for i, r in enumerate(data["restaurants"]) if cuisine in r["cuisines"]]
            if restaurant_indices_with_cuisine:
                cuisine_conditions.append(z3.Or([choices[mk] == i for i in restaurant_indices_with_cuisine]))
        # At least one meal must have this cuisine
        s.add(z3.Or(cuisine_conditions))
    
    # Requirement: not planning on driving ourselves
    # So transport_out and transport_back must not be "self-driving"
    for transport_key in ["transport_out", "transport_back"]:
        options = data[transport_key]
        non_driving_indices = [i for i, opt in enumerate(options) if opt["kind"] != "self-driving"]
        s.add(z3.Or([choices[transport_key] == i for i in non_driving_indices]))
```