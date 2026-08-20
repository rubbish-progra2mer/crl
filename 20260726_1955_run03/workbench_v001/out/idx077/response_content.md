```python
import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Transport costs
    transport_out_cost = pick(choices["transport_out"], [
        opt["price"] * (people if opt["kind"] == "flight" else 
                       math.ceil(people / 4) if opt["kind"] == "taxi" else 
                       math.ceil(people / 5))
        for opt in data["transport_out"]
    ])
    transport_back_cost = pick(choices["transport_back"], [
        opt["price"] * (people if opt["kind"] == "flight" else 
                       math.ceil(people / 4) if opt["kind"] == "taxi" else 
                       math.ceil(people / 5))
        for opt in data["transport_back"]
    ])
    
    # Hotel cost
    hotel_cost = pick(choices["hotel"], [
        opt["price"] * math.ceil(people / opt["max_occupancy"]) * nights
        for opt in data["hotels"]
    ])
    
    # Meal costs
    meal_vars = [
        "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
        "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
        "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"
    ]
    meal_costs = []
    for mv in meal_vars:
        meal_costs.append(pick(choices[mv], [
            opt["avg_cost"] * people for opt in data["restaurants"]
        ]))
    
    # Total cost constraint
    total_cost = transport_out_cost + transport_back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 restaurants must be pairwise distinct
    meal_choice_vars = [choices[mv] for mv in meal_vars]
    s.add(z3.Distinct(meal_choice_vars))
    
    # All 3 attractions must be pairwise distinct
    s.add(z3.Distinct([choices["attr_1"], choices["attr_2"], choices["attr_3"]]))
    
    # Hotel must be private room
    s.add(pick(choices["hotel"], [
        z3.BoolVal(opt["room_type"] == "Private room") for opt in data["hotels"]
    ]) == True)