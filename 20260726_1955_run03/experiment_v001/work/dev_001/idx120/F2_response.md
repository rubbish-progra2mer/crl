```python
import z3
import math

def add_constraints(s, choices, data):
    people = data["people"]
    nights = data["nights"]
    budget = data["budget"]
    
    # Helper to compute cost for a transport option
    def transport_cost(choice_var, transport_list):
        costs = []
        for opt in transport_list:
            kind = opt["kind"]
            price = opt["price"]
            if kind == "flight":
                costs.append(price * people)
            elif kind == "taxi":
                costs.append(price * math.ceil(people / 4))
            elif kind == "self-driving":
                costs.append(price * math.ceil(people / 5))
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
    
    # Meal costs: each meal cost = restaurant avg_cost * people
    meal_slots = ["meal_1_breakfast", "meal_1_lunch", "meal_1_dinner",
                  "meal_2_breakfast", "meal_2_lunch", "meal_2_dinner",
                  "meal_3_breakfast", "meal_3_lunch", "meal_3_dinner"]
    meal_costs = []
    for slot in meal_slots:
        costs = [r["avg_cost"] * people for r in data["restaurants"]]
        meal_costs.append(pick(choices[slot], costs))
    
    # Total cost constraint
    total_cost = cost_out + cost_back + cost_hotel + sum(meal_costs)
    s.add(total_cost <= budget)
    
    # All 9 meal choices must be pairwise distinct
    meal_vars = [choices[slot] for slot in meal_slots]
    s.add(z3.Distinct(meal_vars))
    
    # All 3 attraction choices must be pairwise distinct
    s.add(z3.Distinct(choices["attr_1"], choices["attr_2"], choices["attr_3"]))
    
    # Hotel must allow pets: house_rules must NOT contain "No pets" (case-insensitive)
    # We'll check each hotel's house_rules string for "No pets" (or "no pets")
    allowed_hotel_indices = []
    for i, h in enumerate(data["hotels"]):
        rules_lower = h["house_rules"].lower()
        if "no pets" not in rules_lower and "no pet" not in rules_lower:
            allowed_hotel_indices.append(i)
    s.add(z3.Or([choices["hotel"] == i for i in allowed_hotel_indices]))
    
    # Hotel must provide entire room: room_type == "Entire home/apt"
    entire_room_indices = [i for i, h in enumerate(data["hotels"]) if h["room_type"] == "Entire home/apt"]
    s.add(z3.Or([choices["hotel"] == i for i in entire_room_indices]))
    
    # Required cuisines: Indian, Chinese, Mediterranean, American must each appear in at least one chosen restaurant
    required_cuisines = ["Indian", "Chinese", "Mediterranean", "American"]
    for cuisine in required_cuisines:
        # For each meal slot, check if the chosen restaurant has this cuisine
        cuisine_conditions = []
        for slot in meal_slots:
            # For each restaurant index, check if its cuisines string contains the required cuisine
            restaurant_indices_with_cuisine = []
            for i, r in enumerate(data["restaurants"]):
                cuisines_list = [c.strip() for c in r["cuisines"].split(",")]
                if cuisine in cuisines_list:
                    restaurant_indices_with_cuisine.append(i)
            # Condition: the chosen restaurant for this slot is one of those indices
            cuisine_conditions.append(z3.Or([choices[slot] == i for i in restaurant_indices_with_cuisine]))
        # At least one meal slot must satisfy this
        s.add(z3.Or(cuisine_conditions))
    
    # Transportation mode restriction: "no flight" or "no self-driving" applies to both directions
    # The query does not mention any such restriction, so no constraint added.
    
    # Note: The query says "no flight" or "no self-driving" but none is stated, so skip.
```