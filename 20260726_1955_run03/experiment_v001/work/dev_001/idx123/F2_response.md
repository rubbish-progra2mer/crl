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
        # We'll build a conditional expression using pick
        # For each option, compute the cost based on kind
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
    transport_out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    transport_back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        price = h["price"]
        max_occ = h["max_occupancy"]
        hotel_costs.append(price * math.ceil(people / max_occ) * nights)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_slots = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                  "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                  "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for slot in meal_slots:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[slot], costs))
    
    total_cost = transport_out_cost + transport_back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 restaurants must be pairwise distinct
    restaurant_vars = [choices[slot] for slot in meal_slots]
    s.add(z3.Distinct(restaurant_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Requirement: private rooms that accommodate children under 10
    # "private rooms" means room_type == "Private room"
    # "accommodate children under 10" means house_rules must NOT contain "No children under 10"
    # Actually the query says "accommodate children under the age of 10" meaning they allow children under 10,
    # so the hotel must NOT have a rule "No children under 10"
    # Also "private rooms" -> room_type == "Private room"
    hotel_idx = choices["hotel"]
    allowed_hotel_indices = []
    for i, h in enumerate(data["hotels"]):
        if h["room_type"] == "Private room" and "No children under 10" not in h["house_rules"]:
            allowed_hotel_indices.append(i)
    s.add(z3.Or([hotel_idx == i for i in allowed_hotel_indices]))
    
    # Requirement: no self-driving (applies to both directions)
    # So transport_out and transport_back must not be self-driving
    for direction in ["transport_out", "transport_back"]:
        choice_var = choices[direction]
        options = data[direction]
        allowed = [i for i, opt in enumerate(options) if opt["kind"] != "self-driving"]
        s.add(z3.Or([choice_var == i for i in allowed]))
```