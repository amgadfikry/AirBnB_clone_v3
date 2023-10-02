#!/usr/bin/python3
""" module that make api for places_reviews table """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def all_reviews(place_id):
    """ function that manage route of all reviews """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        li = []
        for o in obj.reviews:
            li.append(o.to_dict())
        return jsonify(li), 200
    else:
        header = request.get_json()
        if header is None or type(header) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif "user_id" not in header:
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get(User, header.get('user_id'))
        if user is None:
            abort(404)
        elif "text" not in header:
            return jsonify({"error": "Missing text"}), 400
        else:
            header['place_id'] = place_id
            new = Review(**header)
            new.save()
            return jsonify(new.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT', 'DELETE', 'GET'], strict_slashes=False)
def id_reviews(review_id):
    """ function that manange route for review by id """
    obj = storage.get(Review, review_id)
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
            if k not in ['id', 'created_at',
                         'updated_at', 'place_id', 'user_id']:
                setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict()), 200
