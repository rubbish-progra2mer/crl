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
    restaurant_options = data["restaurants"]
    meal_costs = []
    for key in meal_keys:
        costs = [r["avg_cost"] * people for r in restaurant_options]
        meal_costs.append(pick(choices[key], costs))
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # 9 restaurants must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # No additional requirements from the query beyond budget.
    # The query only mentions budget, no other constraints.
```