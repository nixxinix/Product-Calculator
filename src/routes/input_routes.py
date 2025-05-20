from flask import Blueprint, request, render_template, session
from utils.helpers import load_saved_ingredients, save_ingredients_list
from utils.input_validator import is_positive_number, validate_ingredients
from .compute import process_ingredients

bp = Blueprint('input_routes', __name__)
@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            product_name = request.form["product_name"].strip()
            selling_price = request.form["selling_price"]
            fixed_cost = request.form["fixed_cost"]

            errors = []

            if not product_name:
                errors.append("Product name cannot be empty.")

            # Validate selling price
            if not is_positive_number(selling_price, allow_zero=False):
                errors.append("Selling price must be a positive number.")

            # Validate fixed cost
            if not is_positive_number(fixed_cost, allow_zero=True):
                errors.append("Fixed cost must be zero or a positive number.")

            selling_price_val = None
            fixed_cost_val = None
            try:
                selling_price_val = float(selling_price)
            except:
                pass
            try:
                fixed_cost_val = float(fixed_cost)
            except:
                pass

            names = request.form.getlist("name")
            available_qtys = request.form.getlist("available_qty")
            cost_per_units = request.form.getlist("cost_per_unit")
            required_per_units = request.form.getlist("required_per_unit")
            available_units = request.form.getlist("available_unit")
            required_units = request.form.getlist("required_unit")

            ingredients = []
            for i in range(len(names)):
                ingredients.append({
                    "name": names[i].strip(),
                    "available_qty": available_qtys[i],
                    "cost_per_unit": cost_per_units[i],
                    "required_per_unit": required_per_units[i],
                    "available_unit": available_units[i].strip(),
                    "required_unit": required_units[i].strip()
                })

            # Validate ingredients
            valid, message = validate_ingredients(ingredients)
            if not valid:
                errors.append(message)

            if errors:
                # Return all errors joined, or render with errors list if preferred
                return "<br>".join(errors)

            # Convert numeric fields after all validations
            for ing in ingredients:
                ing["available_qty"] = float(ing["available_qty"])
                ing["cost_per_unit"] = float(ing["cost_per_unit"])
                ing["required_per_unit"] = float(ing["required_per_unit"])

            report_data = process_ingredients(product_name, selling_price_val, fixed_cost_val, ingredients)
            session['report_data'] = report_data

            return render_template("result.html", **report_data)

        except Exception as e:
            return f"An error occurred: {e}"

    saved_lists = load_saved_ingredients()
    return render_template("index.html", saved_lists=saved_lists)
