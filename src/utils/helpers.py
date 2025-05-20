import json

# Define unit groups for compatibility checks
MASS_UNITS = {"kg", "g", "mg"}
VOLUME_UNITS = {"l", "ml"}
COUNT_UNITS = {"pcs"}

# Conversion factors within groups (base units: grams for mass, liters for volume)
UNIT_CONVERSION = {
    "kg": {"kg": 1, "g": 1000, "mg": 1_000_000},
    "g": {"kg": 0.001, "g": 1, "mg": 1000},
    "mg": {"kg": 1e-6, "g": 0.001, "mg": 1},
    "l": {"l": 1, "ml": 1000},
    "ml": {"l": 0.001, "ml": 1},
    "pcs": {"pcs": 1}
}

SAVED_INGREDIENTS_FILE = "saved_ingredients.json"

def convert_unit(value, from_unit, to_unit):
    """
    Convert value from from_unit to to_unit.
    Raises ValueError if units are incompatible or unknown.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Check unit compatibility
    if from_unit in MASS_UNITS and to_unit in MASS_UNITS:
        factor = UNIT_CONVERSION[from_unit][to_unit]
    elif from_unit in VOLUME_UNITS and to_unit in VOLUME_UNITS:
        factor = UNIT_CONVERSION[from_unit][to_unit]
    elif from_unit in COUNT_UNITS and to_unit in COUNT_UNITS:
        factor = 1  # No conversion needed
    else:
        raise ValueError(f"Cannot convert from '{from_unit}' to '{to_unit}' - incompatible units")
    
    return value * factor

def is_valid_number(value):
    """
    Check if value is a number >= 0.
    Returns True/False.
    """
    try:
        return float(value) >= 0
    except (ValueError, TypeError):
        return False

def load_saved_ingredients():
    """
    Load saved ingredients from JSON file.
    Returns list of saved ingredients or empty list if file not found.
    """
    try:
        with open(SAVED_INGREDIENTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_ingredients_list(name, ingredients):
    """
    Save a named ingredient list to JSON file.
    Appends to existing saved lists.
    """
    saved = load_saved_ingredients()
    saved.append({'name': name, 'ingredients': ingredients})
    try:
        with open(SAVED_INGREDIENTS_FILE, 'w') as f:
            json.dump(saved, f, indent=4)
    except IOError as e:
        print(f"Error saving ingredients list: {e}")

def get_ingredients_by_name(name):
    """
    Retrieve saved ingredient list by name.
    Returns ingredients list or None if not found.
    """
    for item in load_saved_ingredients():
        if item['name'] == name:
            return item['ingredients']
    return None

def remove_ingredients_list(name):
    """
    Remove a saved ingredient list by name.
    """
    lists = [i for i in load_saved_ingredients() if i['name'] != name]
    try:
        with open(SAVED_INGREDIENTS_FILE, 'w') as f:
            json.dump(lists, f, indent=4)
    except IOError as e:
        print(f"Error removing ingredients list: {e}")
