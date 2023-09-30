#!/usr/bin/python3
"""
API version 1 Flask application.

This module initializes and configures the Flask application for API version 1
of the AirBnB Clone project. It defines routes, error handlers, CORS settings,
and registers blueprints for different API views.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>

Attributes:
    - app: Flask application instance
    - CORS: Cross-Origin Resource Sharing for enabling CORS
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
from os import getenv


app = Flask('__name__')

# Enable CORS for all routes under /api
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(self):
    """
    Teardown app context function to close the storage.

    Args:
        self: The Flask application context.

    Returns:
        None.
    """
    storage.close()


# Register the blueprint
app.register_blueprint(app_views)


# Define a custom error handler for 404 errors
@app.errorhandler(404)
def page_not_found(error):
    """
    Custom error handler for 404 Not Found errors.

    Args:
        error: The error object (not used).

    Returns:
        A JSON response with a 404 status code.
    """
    return (jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    # Check and set the host and port based on environment variables
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'

    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = 5000

     # Run the Flask application
    app.run(host=host, port=port, threaded=True)
