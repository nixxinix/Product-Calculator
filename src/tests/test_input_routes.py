import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class InputRoutesTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client before each test runs.
        This creates a test client instance from the Flask app
        and enables testing mode to propagate exceptions and give better error messages.
        """
        self.app = app
        self.app.testing = True  # Enables testing mode
        self.client = self.app.test_client()  # Test client simulates HTTP requests
        print("\nSetup test client")

    def test_get_index(self):
        """
        Test the GET request to the root URL '/'.
        Verify that the response status code is 200 (OK)
        and that the expected text is present in the page content.
        """
        print("Running test_get_index...")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        print("Status code 200 OK confirmed")

        expected_text = "Product Cost and Profit Calculator"
        self.assertIn(expected_text, response.data.decode('utf-8'))
        print(f"Verified presence of expected text: '{expected_text}'")

    def test_post_adequate_resources(self):
        """
        TEST CASE: Adequate resources
        Test submitting valid form data with adequate ingredient quantities.
        Expect a successful response and that the result page contains 'Profit'.
        """
        print("Running test_post_adequate_resources (Adequate resources)...")
        data = {
            "product_name": "Test Product",
            "selling_price": "15.0",
            "fixed_cost": "3",
            "name": ["Flour", "Sugar"],
            "available_qty": ["100", "50"],      # Adequate quantities
            "cost_per_unit": ["0.5", "0.8"],
            "required_per_unit": ["1", "0.5"],
            "available_unit": ["kg", "kg"],
            "required_unit": ["kg", "kg"]
        }
        response = self.client.post("/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Profit", response.data.decode('utf-8'))
        print("Adequate resources test passed with 'Profit' in response")

    def test_post_scarce_resources(self):
        """
        TEST CASE: Scarce resources
        Test submitting form data with ingredient quantities very close to required amounts.
        The app should process it without crashing and still show 'Profit' or results.
        """
        print("Running test_post_scarce_resources (Scarce resources)...")
        data = {
            "product_name": "Scarce Product",
            "selling_price": "12.0",
            "fixed_cost": "4",
            "name": ["Flour", "Sugar"],
            "available_qty": ["1", "0.5"],       # Very low quantities (scarce)
            "cost_per_unit": ["0.5", "0.8"],
            "required_per_unit": ["1", "0.5"],   # Required amounts just met
            "available_unit": ["kg", "kg"],
            "required_unit": ["kg", "kg"]
        }
        response = self.client.post("/", data=data)
        self.assertEqual(response.status_code, 200)
        # Check for profit or result presence (depends on your app implementation)
        self.assertIn("Profit", response.data.decode('utf-8'))
        print("Scarce resources test passed with 'Profit' in response")

    def test_post_zero_or_negative_inputs(self):
        """
        TEST CASE: Zero or negative inputs
        Test submitting invalid data such as negative selling price or zero quantities.
        Expect the app to return validation error messages.
        """
        print("Running test_post_zero_or_negative_inputs (Zero/Negative inputs)...")
        data = {
            "product_name": "Invalid Product",
            "selling_price": "-10",               # Negative selling price (invalid)
            "fixed_cost": "2",
            "name": ["Flour"],
            "available_qty": ["0"],               # Zero available quantity (invalid)
            "cost_per_unit": ["0.5"],
            "required_per_unit": ["1"],
            "available_unit": ["kg"],
            "required_unit": ["kg"]
        }
        response = self.client.post("/", data=data)
        self.assertEqual(response.status_code, 200)

        # List of expected validation error messages returned by your app
        error_msgs = [
            "Selling price must be a positive number.",
            "Available quantity must be greater than zero."
        ]
        page_content = response.data.decode('utf-8')
        # Check that all expected error messages appear in the response
        for msg in error_msgs:
            self.assertIn(msg, page_content)
            print(f"Verified error message presence: '{msg}'")

if __name__ == "__main__":
    # Run the tests if this script is executed directly
    unittest.main()
