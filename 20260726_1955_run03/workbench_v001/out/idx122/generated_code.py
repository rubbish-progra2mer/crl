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
                cost = opt["price"] * people
            elif opt["kind"] == "taxi":
                cost = opt["price"] * math.ceil(people / 4)
            elif opt["kind"] == "self-driving":
                cost = opt["price"] * math.ceil(people / 5)
            else:
                cost = 0
            costs.append(cost)
        return pick(choice_var, costs)
    
    # Transport costs
    out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_costs = []
    for h in data["hotels"]:
        hotel_costs.append(h["price"] * math.ceil(people / h["max_occupancy"]) * nights)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = avg_cost * people
    meal_slots = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                  "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                  "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for slot in meal_slots:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[slot], costs))
    
    # Total cost constraint
    total_cost = out_cost + back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meals must be pairwise distinct
    meal_vars = [choices[slot] for slot in meal_slots]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Accommodation: smoking allowed and room not shared
    allowed_hotel_indices = []
    for i, h in enumerate(data["hotels"]):
        if "smoking" in h["house_rules"].lower() and h["room_type"] != "Shared room":
            allowed_hotel_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
    
    # No self-driving for transport
    for transport_key in ["transport_out", "transport_back"]:
        allowed_indices = []
        for i, opt in enumerate(data[transport_key]):
            if opt["kind"] != "self-driving":
                allowed_indices.append(i)
        s.add(z3.Or([choices[transport_key] == i for i in allowed_indices]))
