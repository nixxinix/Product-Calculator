from flask import Flask
from routes import register_blueprints

# Create the Flask application instance
app = Flask(__name__)

# Set a secret key for securely signing the session cookie and other security needs
app.secret_key = "your_secret_key"

# Register all blueprints (grouped routes) to the Flask app
register_blueprints(app)

# Run the app only if this script is executed directly (not imported)
if __name__ == "__main__":
    # Enable debug mode for automatic reloads and better error messages during development
    app.run(debug=True)
