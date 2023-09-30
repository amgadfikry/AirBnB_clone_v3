#!/usr/bin/python3
"""
API Routes for City Objects.

This module defines routes for performing RESTful API actions on City objects.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>
    
Routes:
    - /states/<state_id>/cities: Retrieves list of all City objects of a State.
    - /cities/<city_id>: Retrieves a City object by its ID.
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
    # Attempt to retrieve a State object from the storage engine by its ID.
    state = storage.get(State, state_id)

    # Check if the 'state' variable is None, indicating that no State object
    # with the provided ID was found.
    if state is None:
        # Raise a 404 error response.
        abort(404)

    # Create a list of dictionaries representing City objects within the State.
    cities = [city.to_dict() for city in state.cities]

    # Return the 'cities' list as a JSON response.
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
    # Attempt to retrieve a City object from the storage engine by its ID.
    city = storage.get(City, city_id)

    # Check if the 'city' variable is None, indicating that no City object
    # with the provided ID was found.
    if city is None:
        # Raise a 404 error response.
        abort(404)

    # Convert the retrieved 'city' object to a dictionary.
    city_dict = city.to_dict()

    # Return the 'city_dict' as a JSON response.
    return (jsonify(city_dict))


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
    # Attempt to retrieve a City object from the storage engine by its ID.
    city = storage.get(City, city_id)

    # Check if the 'city' variable is None, indicating that no City object
    # with the provided ID was found.
    if city is None:
        # Raise a 404 error response.
        abort(404)

    # Delete the 'city' object from the storage engine.
    storage.delete(city)

    # Save the changes in the storage engine.
    storage.save()

    # Return an empty dictionary as a JSON response with status code 200.
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
    # Attempt to retrieve a State object from the storage engine by its ID.
    state = storage.get(State, state_id)

    # Check if the 'state' variable is None, indicating that no State object
    # with the provided ID was found.
    if state is None:
        # Raise a 404 error response.
        abort(404)

    # Attempt to retrieve JSON data from the request body.
    data = request.get_json()

    # Define error messages as variables
    error_not_json = {"error": "Not a JSON"}
    error_missing_name = {"error": "Missing name"}

    # Check if the 'data' variable is None, indicating that the request body
    # is not valid JSON.
    if data is None:
        # Return a JSON response with a 400 error and the "Not a JSON" message.
        return (jsonify(error_not_json), 400)

    # Check if the 'data' dictionary contains the key 'name'.
    if 'name' not in data:
        # Return a JSON response with a 400 error
        # and the "Missing name" message.
        return (jsonify(error_missing_name), 400)

    # Add 'state_id' to the 'data' dictionary.
    data['state_id'] = state_id

    # Create a new City object using the provided JSON data.
    new_city = City(**data)

    # Save the new City object to the storage engine.
    new_city.save()

    # Convert the newly created 'city' object to a dictionary.
    city_dict = new_city.to_dict()

    # Return a JSON representation of the new City with status code 201.
    return (jsonify(city_dict), 201)


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
    # Attempt to retrieve the City object by its ID from storage.
    city = storage.get(City, city_id)

    # Check if the retrieved city is None, indicating that no City object
    # with the given ID was found.
    if city is None:
        # Raise a 404 error response.
        abort(404)

    # Attempt to retrieve JSON data from the request body.
    data = request.get_json()

    # Define error message as variable
    error_not_json = {"error": "Not a JSON"}

    # Check if the 'data' variable is None, indicating that the request body
    # is not valid JSON.
    if data is None:
        # Return a JSON response with a 400 error and the "Not a JSON" message.
        return (jsonify(error_not_json), 400)

    # Iterate through the 'data' dictionary and update the City object's
    # attributes accordingly.
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    # Save the updated City object to the storage engine.
    city.save()

    # Convert the updated 'city' object to a dictionary.
    city_dict = city.to_dict()

    # Return a JSON representation of the updated City with status code 200.
    return (jsonify(city_dict), 200)
