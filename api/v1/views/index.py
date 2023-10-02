#!/usr/bin/python3
""" module to route to status """
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.place import Place
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """ function that return status of api in json"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def api_state():
    """ function route to state of objects """
    obj = {'amenities': Amenity,
           'cities': City,
           'places': Place,
           'reviews': Review,
           'states': State,
           'users': User
           }
    res = {}
    for k, v in obj.items():
        res[k] = storage.count(v)
    return jsonify(res)
