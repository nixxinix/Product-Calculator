# Import Blueprint to allow modular route handling
from flask import Blueprint

# Import individual blueprints from input_routes and output_routes
# These files should each define a `bp` Blueprint instance
from .input_routes import bp as input_bp
from .output_routes import bp as output_bp

# Function to register all route blueprints to the main Flask app
def register_blueprints(app):
    """
    Attach all blueprint route modules to the Flask app.
    
    Parameters:
    - app: The main Flask application instance.
    """
    
    # Register the input-related routes (e.g., handling form or JSON inputs)
    app.register_blueprint(input_bp)

    # Register the output-related routes (e.g., returning processed results)
    app.register_blueprint(output_bp)
