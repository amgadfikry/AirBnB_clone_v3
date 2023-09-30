#!/usr/bin/python3
"""
Handles RESTful API actions for the link between Place and Amenity objects.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route(
    '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place.

    Args:
        place_id: The ID of the Place to retrieve amenities for.

    Returns:
        JSON representation of all Amenity objects linked to the Place.
        404 error if the place_id is not linked to any Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return (jsonify(amenities))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object linked to a Place.

    Args:
        place_id: The ID of the Place.
        amenity_id: The ID of the Amenity to delete.

    Returns:
        An empty dictionary with the status code 200.
        404 error if the place_id is not linked to any Place object,
        the amenity_id is not linked to any Amenity object,
        or the Amenity is not linked to the Place before the request.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None or amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    place.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place.

    Args:
        place_id: The ID of the Place.
        amenity_id: The ID of the Amenity to link.

    Returns:
        JSON representation of the linked Amenity with the status code 201.
        404 error if the place_id is not linked to any Place object
        or the amenity_id is not linked to any Amenity object.
        200 status code if the Amenity is already linked to the Place.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return (jsonify(amenity.to_dict()), 201)
