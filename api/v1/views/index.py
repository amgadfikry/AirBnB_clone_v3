#!/usr/bin/python3
"""
API Index Routes.

This module defines routes for the API index, which includes the status of the
API and statistics about the data stored in the application's storage engine.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>

Routes:
    - /status: Returns the status of the API.
    - /stats: Retrieves the number of each object type in the storage.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """
    Get API Status.

    Returns:
        A JSON response with the status of the API.

    Example:
        {
            "status": "OK"
        }
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def api_stats():
    """
    Get API Statistics.

    Retrieves the number of each object type in the storage and returns it in
    a JSON response.

    Returns:
        A JSON response with statistics on the number of each object type.

    Example:
        {
            "amenities": 10,
            "cities": 25,
            "places": 50,
            "reviews": 30,
            "states": 15,
            "users": 100
        }
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return (jsonify(stats))
