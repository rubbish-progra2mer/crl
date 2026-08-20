```python
import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Transport costs
    transport_out_options = data["transport_out"]
    transport_back_options = data["transport_back"]
    
    # Compute cost for each transport option
    def transport_cost(option):
        if option["kind"] == "flight":
            return option["price"] * people
        elif option["kind"] == "taxi":
            return option["price"] * math.ceil(people / 4)
        elif option["kind"] == "self-driving":
            return option["price"] * math.ceil(people / 5)
        else:
            return 0
    
    out_costs = [transport_cost(opt) for opt in transport_out_options]
    back_costs = [transport_cost(opt) for opt in transport_back_options]
    
    total_transport = pick(choices["transport_out"], out_costs) + pick(choices["transport_back"], back_costs)
    
    # Hotel cost
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        max_occ = h["max_occupancy"]
        hotel_costs.append(h["price"] * math.ceil(people / max_occ) * nights)
    total_hotel = pick(choices["hotel"], hotel_costs)
    
    # Meal costs
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    restaurant_options = data["restaurants"]
    meal_costs = [r["avg_cost"] * people for r in restaurant_options]
    total_meals = sum(pick(choices[mk], meal_costs) for mk in meal_keys)
    
    # Total cost constraint
    total_cost = total_transport + total_hotel + total_meals
    s.add(total_cost <= budget)
    
    # Pairwise distinct restaurants
    meal_vars = [choices[mk] for mk in meal_keys]
    for i in range(len(meal_vars)):
        for j in range(i+1, len(meal_vars)):
            s.add(meal_vars[i] != meal_vars[j])
    
    # Pairwise distinct attractions
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    for i in range(3):
        for j in range(i+1, 3):
            s.add(attr_vars[i] != attr_vars[j])
    
    # Accommodation requirement: ideally entire rooms -> prefer entire home/apt or private room
    # Enforce that hotel room_type is not "Shared room"
    hotel_indices = []
    for i, h in enumerate(hotel_options):
        if h["room_type"] != "Shared room":
            hotel_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in hotel_indices]))
```