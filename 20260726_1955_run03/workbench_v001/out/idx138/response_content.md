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
        costs = []
        for opt in options:
            kind = opt["kind"]
            price = opt["price"]
            if kind == "flight":
                cost = price * people
            elif kind == "self-driving":
                cost = price * math.ceil(people / 5)
            elif kind == "taxi":
                cost = price * math.ceil(people / 4)
            else:
                cost = 0  # should not happen
            costs.append(cost)
        return pick(choice_var, costs)
    
    # Transport costs
    cost_out = transport_cost(choices["transport_out"], data["transport_out"])
    cost_back = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        price = h["price"]
        max_occ = h["max_occupancy"]
        hotel_costs.append(price * math.ceil(people / max_occ) * nights)
    cost_hotel = pick(choices["hotel"], hotel_costs)
    
    # Meal costs (9 meals)
    meal_keys = [
        "meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
        "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
        "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"
    ]
    restaurant_options = data["restaurants"]
    meal_costs = []
    for key in meal_keys:
        costs = [r["avg_cost"] * people for r in restaurant_options]
        meal_costs.append(pick(choices[key], costs))
    
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # Constraint: no flights
    def no_flight(choice_var, options):
        allowed = [i for i, opt in enumerate(options) if opt["kind"] != "flight"]
        s.add(z3.Or([choice_var == i for i in allowed]))
    
    no_flight(choices["transport_out"], data["transport_out"])
    no_flight(choices["transport_back"], data["transport_back"])
    
    # Constraint: hotel allows pets and entire home/apt
    hotel_allowed = []
    for i, h in enumerate(data["hotels"]):
        rules = h["house_rules"].lower()
        if "pets" in rules or "pet" in rules:
            # Check if it explicitly says no pets? We assume "allows pets" means not prohibited.
            # But the query says "allow pets", so we require that pets are allowed.
            # Since house_rules may say "No pets", we check for "no pets" or "no pet".
            if "no pets" not in rules and "no pet" not in rules:
                if h["room_type"] == "Entire home/apt":
                    hotel_allowed.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in hotel_allowed]))
    
    # Pairwise distinct restaurants (9 meals)
    meal_vars = [choices[key] for key in meal_keys]
    for i in range(len(meal_vars)):
        for j in range(i+1, len(meal_vars)):
            s.add(meal_vars[i] != meal_vars[j])
    
    # Pairwise distinct attractions (3)
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    for i in range(3):
        for j in range(i+1, 3):
            s.add(attr_vars[i] != attr_vars[j])