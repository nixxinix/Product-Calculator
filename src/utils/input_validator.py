def is_positive_number(value, allow_zero=True):
    """
    Checks if the given value is a number and is positive.
    If allow_zero is True, zero is allowed.
    """
    try:
        val = float(value)
        if allow_zero:
            return val >= 0
        return val > 0
    except (ValueError, TypeError):
        return False

def validate_ingredients(ingredients):
    for ing in ingredients:
        # Check name non-empty
        if not ing["name"]:
            return False, "Ingredient name cannot be empty."

        # Check available quantity > 0
        try:
            available_qty = float(ing["available_qty"])
            if available_qty <= 0:
                return False, "Available quantity must be greater than zero."
        except ValueError:
            return False, "Available quantity must be a number."

        # Similarly for cost_per_unit and required_per_unit
        try:
            cost_per_unit = float(ing["cost_per_unit"])
            if cost_per_unit <= 0:
                return False, "Cost per unit must be greater than zero."
        except ValueError:
            return False, "Cost per unit must be a number."

        try:
            required_per_unit = float(ing["required_per_unit"])
            if required_per_unit <= 0:
                return False, "Required quantity must be greater than zero."
        except ValueError:
            return False, "Required quantity must be a number."

        # Optional: check units are non-empty strings
        if not ing["available_unit"]:
            return False, "Available unit cannot be empty."
        if not ing["required_unit"]:
            return False, "Required unit cannot be empty."

    return True, ""
