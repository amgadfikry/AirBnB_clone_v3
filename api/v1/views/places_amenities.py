#!/usr/bin/python3
""" module that make api for amenities related to place table """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def all_place_amenities(place_id):
    """ function that manage route of all places """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    li = []
    for o in obj.amenities:
        li.append(o.to_dict())
    return jsonify(li), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def id_place_amenity(place_id, amenity_id):
    """ function that manange route for place amenities by id """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    if request.method == 'DELETE':
        if amenity_obj not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity_obj)
        place_obj.save()
        return jsonify({}), 200
    else:
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict()), 200
        else:
            place_obj.amenities.append(amenity_obj)
            place_obj.save()
            return jsonify(amenity_obj.to_dict()), 201
