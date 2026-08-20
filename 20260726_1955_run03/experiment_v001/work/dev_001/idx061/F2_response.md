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
    cost_out = transport_cost(choices["transport_out"], data["transport_out"])
    cost_back = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        hotel_costs.append(h["price"] * math.ceil(people / h["max_occupancy"]) * nights)
    cost_hotel = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_slots = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                  "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                  "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for slot in meal_slots:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[slot], costs))
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meals must be pairwise distinct restaurants
    meal_vars = [choices[slot] for slot in meal_slots]
    s.add(z3.Distinct(meal_vars))
    
    # 3 attractions must be pairwise distinct
    s.add(z3.Distinct([choices["attr_1"], choices["attr_2"], choices["attr_3"]]))
    
    # Requirement: non-shared rooms -> room_type must not be "Shared room"
    # So hotel must have room_type in {"Entire home/apt", "Private room"}
    allowed_hotel_indices = [i for i, h in enumerate(data["hotels"]) if h["room_type"] != "Shared room"]
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
```