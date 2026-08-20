```python
import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute transport cost
    def transport_cost(choice_var, options):
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
                cost = 0
            costs.append(cost)
        return pick(choice_var, costs)
    
    # Transport costs
    out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        max_occ = h["max_occupancy"]
        price = h["price"]
        cost = price * math.ceil(people / max_occ) * nights
        hotel_costs.append(cost)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs
    meal_keys = [
        "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
        "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
        "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"
    ]
    meal_costs = []
    for key in meal_keys:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[key], costs))
    
    total_cost = out_cost + back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meals must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    s.add(z3.Distinct(choices["attr_1"], choices["attr_2"], choices["attr_3"]))
    
    # Cuisine preference: each meal must be from a restaurant that offers American or Mediterranean cuisine
    # Build allowed indices for each meal (same set for all meals)
    allowed_restaurants = []
    for i, r in enumerate(data["restaurants"]):
        cuisines = r["cuisines"].lower()
        if "american" in cuisines or "mediterranean" in cuisines:
            allowed_restaurants.append(i)
    
    for key in meal_keys:
        s.add(z3.Or([choices[key] == i for i in allowed_restaurants]))
```