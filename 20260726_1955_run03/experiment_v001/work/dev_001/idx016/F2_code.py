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
    out_cost = transport_cost(choices["transport_out"], data["transport_out"])
    back_cost = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_prices = [h["price"] for h in data["hotels"]]
    hotel_max_occ = [h["max_occupancy"] for h in data["hotels"]]
    hotel_cost_expr = pick(choices["hotel"], 
                           [price * math.ceil(people / occ) * nights 
                            for price, occ in zip(hotel_prices, hotel_max_occ)])
    
    # Meal costs: each meal cost = avg_cost * people
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for key in meal_keys:
        avg_costs = [r["avg_cost"] for r in data["restaurants"]]
        meal_costs.append(pick(choices[key], [c * people for c in avg_costs]))
    
    # Total cost constraint
    total_cost = out_cost + back_cost + hotel_cost_expr + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meals must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # No additional requirements from the query (budget already handled, no other constraints mentioned)
