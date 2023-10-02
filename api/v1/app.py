#!/usr/bin/python3
""" module to all routes of v1 """
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
from flask_cors import CORS


app = Flask('__name__')
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(self):
    """close storage function after close it"""
    storage.close()


@app.errorhandler(404)
def error_handle(err):
    """ function that handle error 404 route"""
    return jsonify({"error": "Not found"}), 404


app.register_blueprint(app_views)


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'

    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True, debug=True)
