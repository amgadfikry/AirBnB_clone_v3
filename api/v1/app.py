#!/usr/bin/python3
""" module to all routes of v1 """
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv


app = Flask('__name__')


@app.teardown_appcontext
def close(self):
    """close storage function after close it"""
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
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'

    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True)
