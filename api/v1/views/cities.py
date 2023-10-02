#!/usr/bin/python3
""" module that make api for cities table """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def all_cities(state_id):
    """ function that manage route of all cities """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        li = []
        for o in obj.cities:
            li.append(o.to_dict())
        return jsonify(li), 200
    else:
        header = request.get_json()
        if header is None or type(header) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif "name" not in header:
            return jsonify({"error": "Missing name"}), 400
        else:
            header['state_id'] = state_id
            new = City(**header)
            new.save()
            return jsonify(new.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT', 'DELETE', 'GET'], strict_slashes=False)
def id_cities(city_id):
    """ function that manange route for city by id """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(obj.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        header = request.get_json()
        if header is None or type(header) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in header.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict()), 200
