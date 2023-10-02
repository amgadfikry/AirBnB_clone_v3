#!/usr/bin/python3
""" module to route api if users objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users", methods=['GET', 'POST'], strict_slashes=False)
def all_users():
    """ function route to json all users """
    if request.method == 'GET':
        users = storage.all(User)
        li = []
        for v in users.values():
            li.append(v.to_dict())
        return jsonify(li), 200
    else:
        header = request.get_json()
        if header is None or type(header) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif "email" not in header:
            return jsonify({"error": "Missing email"}), 400
        elif "password" not in header:
            return jsonify({"error": "Missing password"}), 400
        else:
            new = User(**header)
            new.save()
            return jsonify(new.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def id_users(user_id):
    """ get state obj by user id """
    obj = storage.get(User, user_id)
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
            if k not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(obj, k, v)
            obj.save()
        return jsonify(obj.to_dict()), 200
