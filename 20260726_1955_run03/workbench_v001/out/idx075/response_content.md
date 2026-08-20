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
        # We'll build a conditional expression using z3.If
        # Since pick returns a z3 expression, we need to handle the kind-dependent cost
        # We'll iterate over indices and build a sum of conditions
        cost_expr = z3.IntVal(0)
        for i, opt in enumerate(options):
            kind = opt["kind"]
            price = opt["price"]
            if kind == "flight":
                per_person = price * people
            elif kind == "taxi":
                per_person = price * math.ceil(people / 4)
            elif kind == "self-driving":
                per_person = price * math.ceil(people / 5)
            else:
                per_person = 0
            cost_expr = z3.If(choice_var == i, z3.IntVal(per_person), cost_expr)
        return cost_expr
    
    # Transport costs
    transport_out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    transport_back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_cost = z3.IntVal(0)
    for i, hotel in enumerate(data["hotels"]):
        price = hotel["price"]
        max_occ = hotel["max_occupancy"]
        factor = math.ceil(people / max_occ)
        hotel_cost = z3.If(choices["hotel"] == i, z3.IntVal(price * factor * nights), hotel_cost)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_slots = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                  "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                  "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for slot in meal_slots:
        cost_expr = z3.IntVal(0)
        for i, rest in enumerate(data["restaurants"]):
            cost_expr = z3.If(choices[slot] == i, z3.IntVal(rest["avg_cost"] * people), cost_expr)
        meal_costs.append(cost_expr)
    
    total_cost = transport_out_cost + transport_back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= int(budget))
    
    # All 9 restaurants must be pairwise distinct
    for i in range(len(meal_slots)):
        for j in range(i+1, len(meal_slots)):
            s.add(choices[meal_slots[i]] != choices[meal_slots[j]])
    
    # All 3 attractions must be pairwise distinct
    attr_slots = ["attr_1", "attr_2", "attr_3"]
    for i in range(3):
        for j in range(i+1, 3):
            s.add(choices[attr_slots[i]] != choices[attr_slots[j]])
    
    # Accommodation must allow visitors per house rules
    # We need to find hotels where house_rules does not contain "No visitors" or similar
    # The query says "allow visitors", so we exclude hotels with "No visitors" in house_rules
    allowed_hotel_indices = [i for i, h in enumerate(data["hotels"]) if "No visitors" not in h.get("house_rules", "")]
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
```