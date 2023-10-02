#!/usr/bin/python3
""" module to route api if state objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
def all_state():
    """ function route to json all state """
    if request.method == 'GET':
        states = storage.all(State)
        li = []
        for v in states.values():
            li.append(v.to_dict())
        return jsonify(li), 200
    else:
        header = request.get_json()
        if header is None or type(header) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif "name" not in header:
            return jsonify({"error": "Missing name"}), 400
        else:
            new = State(**header)
            new.save()
            return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def id_states(state_id):
    """ get state obj by state id """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    elif request.method == 'GET':
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
