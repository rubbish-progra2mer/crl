```python
import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        costs = []
        for opt in options:
            if opt["kind"] == "flight":
                costs.append(opt["price"] * people)
            elif opt["kind"] == "taxi":
                costs.append(opt["price"] * math.ceil(people / 4))
            elif opt["kind"] == "self-driving":
                costs.append(opt["price"] * math.ceil(people / 5))
            else:
                costs.append(0)  # fallback
        return pick(choice_var, costs)
    
    # Transport costs
    cost_out = transport_cost(choices["transport_out"], data["transport_out"])
    cost_back = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_prices = []
    for h in data["hotels"]:
        hotel_prices.append(h["price"] * math.ceil(people / h["max_occupancy"]) * nights)
    cost_hotel = pick(choices["hotel"], hotel_prices)
    
    # Meal costs: each meal cost = avg_cost * people
    meal_slots = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                  "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                  "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for slot in meal_slots:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[slot], costs))
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # 2. All 9 chosen restaurants must be pairwise distinct
    restaurant_vars = [choices[slot] for slot in meal_slots]
    s.add(z3.Distinct(restaurant_vars))
    
    # 3. All 3 chosen attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # 4. Query-specific constraints:
    # a) Accommodations permit smoking: hotel must NOT have "No smoking" in house_rules
    smoking_allowed_indices = []
    for i, h in enumerate(data["hotels"]):
        if "No smoking" not in h["house_rules"]:
            smoking_allowed_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in smoking_allowed_indices]))
    
    # b) Non-shared rooms: room_type must not be "Shared room"
    non_shared_indices = []
    for i, h in enumerate(data["hotels"]):
        if h["room_type"] != "Shared room":
            non_shared_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in non_shared_indices]))
    
    # c) Preferred mode of transportation is not flight-based: both directions must not be flight
    # For transport_out
    non_flight_out_indices = []
    for i, opt in enumerate(data["transport_out"]):
        if opt["kind"] != "flight":
            non_flight_out_indices.append(i)
    s.add(z3.Or([choices["transport_out"] == i for i in non_flight_out_indices]))
    
    # For transport_back
    non_flight_back_indices = []
    for i, opt in enumerate(data["transport_back"]):
        if opt["kind"] != "flight":
            non_flight_back_indices.append(i)
    s.add(z3.Or([choices["transport_back"] == i for i in non_flight_back_indices]))
```