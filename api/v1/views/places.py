#!/usr/bin/python3
"""
Handles RESTful API actions for Place objects.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City.

    Args:
        city_id: The ID of the City to retrieve places for.

    Returns:
        JSON representation of all Place objects in the City.
        404 error if the city_id is not linked to any City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return (jsonify(places))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object by its ID.

    Args:
        place_id: The ID of the Place object to retrieve.

    Returns:
        JSON representation of the Place object.
        404 error if the place_id is not linked to any Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return (jsonify(place.to_dict()))


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object by its ID.

    Args:
        place_id: The ID of the Place object to delete.

    Returns:
        An empty dictionary with the status code 200.
        404 error if the place_id is not linked to any Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return (jsonify({}))


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place.

    Args:
        city_id: The ID of the City in which to create the Place.

    Returns:
        JSON representation of the new Place with the status code 201.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
        404 error if the city_id is not linked to any City object.
        400 error with the message "Missing user_id" or "Missing name"
            if the dictionary doesn't contain the respective keys.
        404 error if the user_id is not linked to any User object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object by its ID.

    Args:
        place_id: The ID of the Place object to update.

    Returns:
        JSON representation of the updated Place object with status code 200.
        404 error if the place_id is not linked to any Place object.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return (jsonify(place.to_dict()), 200)
