#!/usr/bin/python3
"""
Handles RESTful API actions for Amenity objects.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects.

    Returns:
        JSON representation of all Amenity objects.
    """
    amenities = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return (jsonify(amenities))


@app_views.route(
    '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves an Amenity object by its ID.

    Args:
        amenity_id: The ID of the Amenity object to retrieve.

    Returns:
        JSON representation of the Amenity object.
        404 error if the amenity_id is not linked to any Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return (jsonify(amenity.to_dict()))


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object by its ID.

    Args:
        amenity_id: The ID of the Amenity object to delete.

    Returns:
        An empty dictionary with the status code 200.
        404 error if the amenity_id is not linked to any Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity.

    Returns:
        JSON representation of the new Amenity with the status code 201.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
        400 error with the message "Missing name"
            if the dictionary doesn't contain the key 'name'.
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**data)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route(
    '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an Amenity object by its ID.

    Args:
        amenity_id: The ID of the Amenity object to update.

    Returns:
        JSON representation of the updated Amenity object with status code 200.
        404 error if the amenity_id is not linked to any Amenity object.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
