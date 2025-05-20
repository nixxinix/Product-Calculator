from flask import Blueprint, jsonify, request
from utils.helpers import (
    load_saved_ingredients,
    save_ingredients_list,
    get_ingredients_by_name,
    remove_ingredients_list
)

# Create a Blueprint named 'output_routes' to group API endpoints for ingredient data management
bp = Blueprint('output_routes', __name__)

@bp.route('/save_ingredients', methods=['POST'])
def save_ingredients():
    """
    Endpoint to save a named list of ingredients.
    Expects JSON payload with 'name' and 'ingredients' keys.

    If both are provided, saves the list and returns success message.
    Otherwise, returns a 400 error for invalid data.
    """
    data = request.get_json()  # Parse JSON payload from request
    name = data.get('name')
    ingredients = data.get('ingredients')

    # Validate presence of required data
    if name and ingredients:
        save_ingredients_list(name, ingredients)  # Save ingredients list persistently
        return jsonify({'message': 'Ingredients saved successfully!'})

    # Return error response if data is invalid or missing
    return jsonify({'error': 'Invalid data'}), 400


@bp.route('/get_saved_ingredients')
def get_saved():
    """
    Endpoint to retrieve all saved ingredient lists.
    Returns a JSON array of saved ingredient list names or data.
    """
    return jsonify(load_saved_ingredients())


@bp.route('/load_ingredients/<name>')
def load(name):
    """
    Endpoint to load a specific saved ingredient list by name.
    Returns the ingredient list as JSON if found,
    or a 404 error if no list exists with the given name.
    """
    ingredients = get_ingredients_by_name(name)
    if ingredients:
        return jsonify(ingredients)

    return jsonify({'error': 'List not found'}), 404


@bp.route('/remove_ingredients/<name>', methods=['DELETE'])
def remove(name):
    """
    Endpoint to delete a saved ingredient list by name.
    Returns a success message regardless of whether the list existed.
    """
    remove_ingredients_list(name)
    return jsonify({'message': 'List removed successfully!'})
