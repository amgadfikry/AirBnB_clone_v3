#!/usr/bin/python3
"""
Handles RESTful API actions for City objects.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State.

    Args:
        state_id: The ID of the State to retrieve cities for.

    Returns:
        JSON representation of all City objects in the State.
        404 error if the state_id is not linked to any State object.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return (jsonify(cities))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object by its ID.

    Args:
        city_id: The ID of the City object to retrieve.

    Returns:
        JSON representation of the City object.
        404 error if the city_id is not linked to any City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return (jsonify(city.to_dict()))


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by its ID.

    Args:
        city_id: The ID of the City object to delete.

    Returns:
        An empty dictionary with the status code 200.
        404 error if the city_id is not linked to any City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City.

    Args:
        state_id: The ID of the State in which to create the City.

    Returns:
        JSON representation of the new City with the status code 201.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
        404 error if the state_id is not linked to any State object.
        400 error with the message "Missing name"
            if the dictionary doesn't contain the key 'name'.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object by its ID.

    Args:
        city_id: The ID of the City object to update.

    Returns:
        JSON representation of the updated City object with status code 200.
        404 error if the city_id is not linked to any City object.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return (jsonify(city.to_dict()), 200)
