import math
from utils.helpers import convert_unit

def process_ingredients(product_name, selling_price, fixed_cost, ingredients):
    """
    Calculate production capacity, costs, revenue, profit, and break-even units for a product
    based on its ingredient availability, costs, and selling price.

    Parameters:
    - product_name (str): Name of the product.
    - selling_price (float): Selling price per unit of the product.
    - fixed_cost (float): Fixed overhead costs related to production.
    - ingredients (list of dict): Each dict contains ingredient data with keys:
        - name: Ingredient name
        - available_qty: Quantity currently available
        - available_unit: Unit in which available quantity is measured
        - required_per_unit: Quantity of ingredient needed per product unit
        - required_unit: Unit for the required quantity
        - cost_per_unit: Cost per unit of ingredient (in available_unit)

    Returns:
    dict with production and cost summary including:
    - max_units: Maximum units producible given available ingredients
    - total_cost: Total cost including fixed costs
    - cost_per_unit: Cost per product unit including fixed cost allocation
    - revenue: Total revenue at max production
    - profit: Total profit at max production
    - break_even_units: Units to break even on fixed costs
    - ingredients: Detailed summary of each ingredient usage and cost
    - raw_total: Total ingredient cost before fixed costs
    - selling_price: Selling price input
    - fixed_cost: Fixed cost input
    """

    # Determine the max number of product units that can be made,
    # limited by the most constrained ingredient availability.
    # Convert required quantities to the same unit as available quantity for comparison.
    max_units = min(
        (ing["available_qty"] // convert_unit(ing["required_per_unit"], ing["required_unit"], ing["available_unit"])
         if convert_unit(ing["required_per_unit"], ing["required_unit"], ing["available_unit"]) > 0 else float('inf'))
        for ing in ingredients
    )
    max_units = int(max_units)  # Round down to whole units producible

    raw_total = 0  # Sum of ingredient costs before fixed cost
    summaries = []  # List to hold detailed info for each ingredient

    # Calculate usage and cost per ingredient based on max production units
    for ing in ingredients:
        # Convert required amount per unit to ingredient's available unit
        converted_required = convert_unit(ing["required_per_unit"], ing["required_unit"], ing["available_unit"])

        # Total quantity of ingredient used for max production
        total_used = converted_required * max_units

        # Total cost for this ingredient usage
        total_cost = ing["cost_per_unit"] * total_used

        # Remaining quantity after usage
        remaining = ing["available_qty"] - total_used

        # Accumulate ingredient cost to raw total
        raw_total += total_cost

        # Append summary info for this ingredient
        summaries.append({
            "name": ing["name"],
            "required_per_unit": ing["required_per_unit"],
            "required_unit": ing["required_unit"],
            "cost_per_unit": ing["cost_per_unit"],
            "total_used": round(total_used, 2),
            "total_cost": round(total_cost, 2),
            "remaining_qty": round(remaining, 2),
            "available_unit": ing["available_unit"]
        })

    # Add fixed cost to raw ingredient cost to get total cost of production
    total_cost_with_fixed = raw_total + fixed_cost

    # Calculate cost per product unit, avoiding division by zero
    cost_per_unit = total_cost_with_fixed / max_units if max_units else 0

    # Calculate total revenue from selling max units
    revenue = max_units * selling_price

    # Calculate profit = revenue minus total cost (ingredients + fixed)
    profit = revenue - total_cost_with_fixed

    # Calculate margin per unit (selling price minus cost per unit)
    margin = selling_price - cost_per_unit

    # Calculate break-even point in units, rounding up;
    # if margin is zero or negative, break-even is infinite
    break_even = math.ceil(fixed_cost / margin) if margin > 0 else float('inf')

    # Return all relevant computed data in a dictionary
    return {
        "product_name": product_name,
        "max_units": max_units,
        "total_cost": round(total_cost_with_fixed, 2),
        "cost_per_unit": round(cost_per_unit, 2),
        "revenue": round(revenue, 2),
        "profit": round(profit, 2),
        "break_even_units": break_even,
        "ingredients": summaries,
        "raw_total": round(raw_total, 2),
        "selling_price": selling_price,
        "fixed_cost": fixed_cost
    }
