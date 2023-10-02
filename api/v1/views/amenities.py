#!/usr/bin/python3
""" module to route for amenities objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
def all_amenity():
    """ function route to json all amenities """
    if request.method == 'GET':
        data = storage.all(Amenity)
        li = []
        for v in data.values():
            li.append(v.to_dict())
        return jsonify(li), 200
    else:
        header = request.get_json()
        if header is None or type(header) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif "name" not in header:
            return jsonify({"error": "Missing name"}), 400
        else:
            new = Amenity(**header)
            new.save()
            return jsonify(new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def id_amenity(amenity_id):
    """ get state obj by amenitiy id """
    obj = storage.get(Amenity, amenity_id)
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
