import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, options):
        costs = []
        for i, opt in enumerate(options):
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
    
    # Transport costs
    out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_costs = []
    for h in data["hotels"]:
        hotel_costs.append(h["price"] * math.ceil(people / h["max_occupancy"]) * nights)
    hotel_cost = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = avg_cost * people
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for mk in meal_keys:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[mk], costs))
    
    total_cost = out_cost + back_cost + hotel_cost + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meals must be pairwise distinct
    meal_vars = [choices[mk] for mk in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # Requirement: no flights for transportation
    # transport_out cannot be a flight
    out_no_flight = []
    for i, opt in enumerate(data["transport_out"]):
        if opt["kind"] != "flight":
            out_no_flight.append(choices["transport_out"] == i)
    s.add(z3.Or(out_no_flight))
    
    # transport_back cannot be a flight
    back_no_flight = []
    for i, opt in enumerate(data["transport_back"]):
        if opt["kind"] != "flight":
            back_no_flight.append(choices["transport_back"] == i)
    s.add(z3.Or(back_no_flight))
    
    # Requirement: accommodations that allow children under 10
    # We interpret "allow children under 10" as house_rules not containing "No children"
    # and also not containing "Adults only" etc. We'll check for "No children" or "no children"
    hotel_allows_children = []
    for i, h in enumerate(data["hotels"]):
        rules_lower = h["house_rules"].lower()
        if "no children" not in rules_lower and "adults only" not in rules_lower:
            hotel_allows_children.append(choices["hotel"] == i)
    s.add(z3.Or(hotel_allows_children))
    
    # Requirement: prefer having entire rooms to ourselves
    # We interpret as preferring "Entire home/apt" room_type
    hotel_entire = []
    for i, h in enumerate(data["hotels"]):
        if h["room_type"] == "Entire home/apt":
            hotel_entire.append(choices["hotel"] == i)
    s.add(z3.Or(hotel_entire))
