```python
import z3
import math

def add_constraints(s, choices, data):
    # Budget constraint
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Transport costs
    transport_out_options = data["transport_out"]
    transport_back_options = data["transport_back"]
    
    # Helper to compute transport cost for a single direction
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
    
    total_transport_out = transport_cost(choices["transport_out"], transport_out_options)
    total_transport_back = transport_cost(choices["transport_back"], transport_back_options)
    
    # Hotel cost
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        max_occ = h["max_occupancy"]
        price = h["price"]
        hotel_costs.append(price * math.ceil(people / max_occ) * nights)
    total_hotel = pick(choices["hotel"], hotel_costs)
    
    # Meal costs (9 meals)
    restaurant_options = data["restaurants"]
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    total_meals = 0
    for key in meal_keys:
        costs = [r["avg_cost"] * people for r in restaurant_options]
        total_meals += pick(choices[key], costs)
    
    total_cost = total_transport_out + total_transport_back + total_hotel + total_meals
    s.add(total_cost <= budget)
    
    # All 9 restaurants must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    for i in range(len(meal_vars)):
        for j in range(i+1, len(meal_vars)):
            s.add(meal_vars[i] != meal_vars[j])
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    for i in range(3):
        for j in range(i+1, 3):
            s.add(attr_vars[i] != attr_vars[j])
    
    # Requirement: Smoking allowed -> hotel must NOT have "No smoking" in house_rules
    hotel_options = data["hotels"]
    allowed_hotel_indices = []
    for i, h in enumerate(hotel_options):
        rules = h["house_rules"].lower()
        if "no smoking" not in rules:
            allowed_hotel_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
```