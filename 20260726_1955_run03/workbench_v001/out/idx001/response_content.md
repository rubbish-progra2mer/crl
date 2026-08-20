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
        # We'll build a list of possible costs per index
        costs = []
        for opt in options:
            if opt["kind"] == "flight":
                cost = opt["price"] * people
            elif opt["kind"] == "taxi":
                cost = opt["price"] * math.ceil(people / 4)
            elif opt["kind"] == "self-driving":
                cost = opt["price"] * math.ceil(people / 5)
            else:
                cost = 0  # should not happen
            costs.append(cost)
        return pick(choice_var, costs)
    
    # Transport costs
    transport_out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    transport_back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        cost = h["price"] * math.ceil(people / h["max_occupancy"]) * nights
        hotel_costs.append(cost)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
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
    
    # Total cost constraint
    total_cost = transport_out_cost + transport_back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meal choices must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attraction choices must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Additional constraints from the query: 
    # The query mentions "one person", so people=1, but we already used that.
    # No other explicit requirements are stated beyond budget and distinctness.
    # However, we must ensure that the chosen options are valid indices.
    # The harness already bounds variables, so no extra constraints needed.
    
    # Note: The query does not specify any other constraints like cuisine preferences,
    # hotel rules, etc. So we only enforce the generic rules above.
    
    # (Optional) If there were any query-specific constraints, they would go here.
    # For completeness, we add nothing else.