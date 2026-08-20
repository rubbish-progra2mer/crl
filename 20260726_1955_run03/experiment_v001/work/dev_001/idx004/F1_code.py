import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # ---------- transport costs ----------
    # outbound
    out_options = data["transport_out"]
    out_price_expr = pick(choices["transport_out"], [opt["price"] for opt in out_options])
    out_kind_expr = pick(choices["transport_out"], [opt["kind"] for opt in out_options])
    # compute cost per person based on kind
    out_cost = z3.If(out_kind_expr == "flight",
                     out_price_expr * people,
                     z3.If(out_kind_expr == "taxi",
                           out_price_expr * math.ceil(people / 4),
                           out_price_expr * math.ceil(people / 5)))
    
    # back
    back_options = data["transport_back"]
    back_price_expr = pick(choices["transport_back"], [opt["price"] for opt in back_options])
    back_kind_expr = pick(choices["transport_back"], [opt["kind"] for opt in back_options])
    back_cost = z3.If(back_kind_expr == "flight",
                      back_price_expr * people,
                      z3.If(back_kind_expr == "taxi",
                            back_price_expr * math.ceil(people / 4),
                            back_price_expr * math.ceil(people / 5)))
    
    # ---------- hotel cost ----------
    hotel_options = data["hotels"]
    hotel_price_expr = pick(choices["hotel"], [h["price"] for h in hotel_options])
    hotel_max_occ_expr = pick(choices["hotel"], [h["max_occupancy"] for h in hotel_options])
    hotel_cost = hotel_price_expr * z3.ToInt(z3.Ceiling(z3.ToReal(people) / z3.ToReal(hotel_max_occ_expr))) * nights
    
    # ---------- meal costs ----------
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for mk in meal_keys:
        cost_expr = pick(choices[mk], [r["avg_cost"] for r in data["restaurants"]])
        meal_costs.append(cost_expr * people)
    total_meal_cost = sum(meal_costs)
    
    # ---------- total cost constraint ----------
    total_cost = out_cost + back_cost + hotel_cost + total_meal_cost
    s.add(total_cost <= budget)
    
    # ---------- pairwise distinct restaurants ----------
    meal_vars = [choices[mk] for mk in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # ---------- pairwise distinct attractions ----------
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))

