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
        # We'll build a list of possible costs per index
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
    cost_out = transport_cost(choices["transport_out"], data["transport_out"])
    cost_back = transport_cost(choices["transport_back"], data["transport_back"])
    
    # Hotel cost: price * ceil(people / max_occupancy) * nights
    hotel_options = data["hotels"]
    hotel_costs = []
    for h in hotel_options:
        price = h["price"]
        max_occ = h["max_occupancy"]
        hotel_costs.append(price * math.ceil(people / max_occ) * nights)
    cost_hotel = pick(choices["hotel"], hotel_costs)
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_keys = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                 "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                 "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    restaurant_options = data["restaurants"]
    meal_costs = []
    for key in meal_keys:
        costs = [r["avg_cost"] * people for r in restaurant_options]
        meal_costs.append(pick(choices[key], costs))
    
    # Total cost constraint
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # 2. All 9 chosen restaurants must be pairwise distinct
    meal_vars = [choices[key] for key in meal_keys]
    s.add(z3.Distinct(meal_vars))
    
    # 3. All 3 chosen attractions must be pairwise distinct
    attr_vars = [choices["attr_1"], choices["attr_2"], choices["attr_3"]]
    s.add(z3.Distinct(attr_vars))
    
    # 4. Query requirements:
    # a) Accommodation must be visitor-friendly: hotel must NOT have "No visitors" in house_rules
    hotel_rules = [h["house_rules"] for h in hotel_options]
    allowed_hotel_indices = [i for i, rules in enumerate(hotel_rules) if "No visitors" not in rules]
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
    
    # b) Required cuisines: Indian, American, Chinese, Italian must each appear in at least one chosen restaurant
    required_cuisines = ["Indian", "American", "Chinese", "Italian"]
    for cuisine in required_cuisines:
        # For each cuisine, at least one meal must be at a restaurant that offers that cuisine
        cuisine_conditions = []
        for i, rest in enumerate(restaurant_options):
            cuisines_list = [c.strip() for c in rest["cuisines"].split(",")]
            if cuisine in cuisines_list:
                # This restaurant index i offers the cuisine
                # At least one meal variable must equal i
                condition = z3.Or([choices[key] == i for key in meal_keys])
                cuisine_conditions.append(condition)
        # At least one restaurant among all meals must offer this cuisine
        s.add(z3.Or(cuisine_conditions))
    
    # c) No self-driving: both transport_out and transport_back must not be self-driving
    # For each transport direction, restrict to indices where kind != "self-driving"
    out_indices = [i for i, opt in enumerate(data["transport_out"]) if opt["kind"] != "self-driving"]
    back_indices = [i for i, opt in enumerate(data["transport_back"]) if opt["kind"] != "self-driving"]
    s.add(z3.Or([choices["transport_out"] == i for i in out_indices]))
    s.add(z3.Or([choices["transport_back"] == i for i in back_indices]))
```