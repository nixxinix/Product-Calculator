import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from routes.compute import process_ingredients

# Mock for convert_unit — returns value unchanged for testing simplicity
def mock_convert_unit(value, from_unit, to_unit):
    return value

class TestProcessIngredients(unittest.TestCase):

    def setUp(self):
        # Monkey-patch convert_unit in compute module
        import routes.compute
        routes.compute.convert_unit = mock_convert_unit

    # Test normal case where all inputs are valid and computable
    def test_basic_computation(self):
        print("\n========== TEST: Basic Computation ==========")
        ingredients = [
            {"name": "Flour", "available_qty": 100, "available_unit": "kg", "required_per_unit": 1, "required_unit": "kg", "cost_per_unit": 0.5},
            {"name": "Sugar", "available_qty": 50, "available_unit": "kg", "required_per_unit": 0.5, "required_unit": "kg", "cost_per_unit": 0.8}
        ]

        result = process_ingredients("Cake", 10.0, 20.0, ingredients)

        print(">> Input: Cake, 10.0 cost, 20.0 price")
        print(">> Ingredients:", ingredients)
        print(">> Result:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        print("=============================================\n")

        self.assertEqual(result["max_units"], 100)
        self.assertAlmostEqual(result["raw_total"], 90)
        self.assertAlmostEqual(result["total_cost"], 110)
        self.assertAlmostEqual(result["cost_per_unit"], 1.1)
        self.assertAlmostEqual(result["revenue"], 1000)
        self.assertAlmostEqual(result["profit"], 890)
        self.assertEqual(result["break_even_units"], 3)

    # Test when one ingredient has 0 required amount (should be ignored in limiting factor)
    def test_zero_required_amount(self):
        print("\n====== TEST: Zero Required Amount ======")
        ingredients = [
            {"name": "Water", "available_qty": 1000, "available_unit": "L", "required_per_unit": 0, "required_unit": "L", "cost_per_unit": 0.0},
            {"name": "Flour", "available_qty": 100, "available_unit": "kg", "required_per_unit": 2, "required_unit": "kg", "cost_per_unit": 0.5}
        ]

        result = process_ingredients("Bread", 5, 10, ingredients)

        print(">> Input: Bread, 5 cost, 10 price")
        print(">> Ingredients:", ingredients)
        print(">> Result:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        print("=========================================\n")

        self.assertEqual(result["max_units"], 50)

    # Test when there is no available quantity for a required ingredient (production not possible)
    def test_zero_max_units(self):
        print("\n====== TEST: Zero Max Units ======")
        ingredients = [
            {"name": "Salt", "available_qty": 0, "available_unit": "g", "required_per_unit": 1, "required_unit": "g", "cost_per_unit": 0.1}
        ]

        result = process_ingredients("Snack", 2, 5, ingredients)

        print(">> Input: Snack, 2 cost, 5 price")
        print(">> Ingredients:", ingredients)
        print(">> Result:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        print("====================================\n")

        self.assertEqual(result["max_units"], 0)
        self.assertEqual(result["cost_per_unit"], 0)
        self.assertEqual(result["profit"], -5)

    # Test where break-even calculation leads to division by zero or negative margin
    def test_negative_margin_break_even(self):
        print("\n====== TEST: Negative Margin Break-Even ======")
        ingredients = [
            {"name": "IngredientA", "available_qty": 10, "available_unit": "kg", "required_per_unit": 1, "required_unit": "kg", "cost_per_unit": 10}
        ]

        result = process_ingredients("ExpensiveProduct", 5, 10, ingredients)

        print(">> Input: ExpensiveProduct, 5 cost, 10 price")
        print(">> Ingredients:", ingredients)
        print(">> Result:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        print("================================================\n")

        self.assertEqual(result["break_even_units"], float('inf'))

if __name__ == "__main__":
    unittest.main()
