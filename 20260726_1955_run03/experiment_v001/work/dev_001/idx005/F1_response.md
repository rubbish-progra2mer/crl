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
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    restaurant_options = data["restaurants"]
    meal_costs = []
    for key in meal_keys:
        costs = [r["avg_cost"] * people for r in restaurant_options]
        meal_costs.append(pick(choices[key], costs))
    
    total_cost = out_cost + back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # Pairwise distinct restaurants (9 meals)
    meal_vars = [choices[key] for key in meal_keys]
    for i in range(len(meal_vars)):
        for j in range(i+1, len(meal_vars)):
            s.add(meal_vars[i] != meal_vars[j])
    
    # Pairwise distinct attractions (3 attractions)
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    for i in range(3):
        for j in range(i+1, 3):
            s.add(attr_vars[i] != attr_vars[j])
    
    # Additional constraints from query: solo traveller -> people == 1
    # Already given, but we can enforce if needed (data["people"] should be 1)
    # No other explicit requirements in query besides budget and distinctness.
    # However, we must ensure that the plan is feasible: e.g., hotel max_occupancy >= people
    # But that is implicitly handled by cost formula (ceil division) but we should ensure
    # that the chosen hotel can accommodate the traveller.
    # Add constraint that hotel max_occupancy >= people
    hotel_max_occ = [h["max_occupancy"] for h in hotel_options]
    s.add(pick(choices["hotel"], [1 if m >= people else 0 for m in hotel_max_occ]) == 1)
    
    # Also ensure that transport options exist (already in domain)
    # No other constraints from query.
```