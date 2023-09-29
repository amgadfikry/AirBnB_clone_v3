""" module to route to status """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """ function that return status of api in json"""
    return jsonify({"status": "OK"})
