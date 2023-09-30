#!/usr/bin/python3
"""
API Routes for State Objects.

This module defines routes for performing RESTful API actions on State objects.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>

Routes:
    - /states: Retrieves the list of all State objects.
    - /states/<state_id>: Retrieves a State object by its ID.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.

    Returns:
        JSON representation of all State objects.
    """
    # Retrieve a list of all State objects from the storage engine.
    all_states = storage.all(State)

    # Convert each State object to a dictionary using the `to_dict` method,
    # and store them in a list called 'states'.
    states = [state.to_dict() for state in all_states.values()]

    # Return the list of 'states' as a JSON response.
    return (jsonify(states))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by its ID.

    Args:
        state_id: The ID of the State object to retrieve.

    Returns:
        JSON representation of the State object.
        404 error if the state_id is not linked to any State object.
    """
    # Attempt to retrieve a State object from the storage engine by its ID.
    state = storage.get(State, state_id)

    # Check if the 'state' variable is None, indicating that no State object
    # with the provided ID was found.
    if state is None:
        # Raise a 404 error response.
        abort(404)

    # Convert the retrieved 'state' object to a dictionary
    # using the `to_dict` method.
    state_dict = state.to_dict()

    # Return the 'state_dict' as a JSON response.
    return (jsonify(state_dict))


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object by its ID.

    Args:
        state_id: The ID of the State object to delete.

    Returns:
        An empty dictionary with the status code 200.
        404 error if the state_id is not linked to any State object.
    """
    # Attempt to retrieve a State object from the storage engine by its ID.
    state = storage.get(State, state_id)

    # Check if the 'state' variable is None, indicating that no State object
    # with the provided ID was found.
    if state is None:
        # Raise a 404 error response.
        abort(404)

    # Delete the 'state' object from the storage engine.
    storage.delete(state)

    # Save the changes in the storage engine.
    storage.save()

    # Return an empty dictionary as a JSON response with status code 200.
    return (jsonify({}))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State.

    Returns:
        JSON representation of the new State with the status code 201.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
        400 error with the message "Missing name"
            if the dictionary doesn't contain the key 'name'.
    """
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

    # Create a new State object using the provided JSON data.
    new_state = State(**data)

    # Save the new State object to the storage engine.
    new_state.save()

    # Convert the newly created 'state' object to a dictionary
    # using the `to_dict` method.
    state_dict = new_state.to_dict()

    # Return a JSON representation of the new State with status code 201.
    return (jsonify(state_dict), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by its ID.

    Args:
        state_id: The ID of the State object to update.

    Returns:
        JSON representation of the updated State object with status code 200.
        404 error if the state_id is not linked to any State object.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
    """
    # Attempt to retrieve the State object by its ID from storage.
    state = storage.get(State, state_id)

    # Define error message as variable
    error_not_json = {"error": "Not a JSON"}

    # Check if the retrieved state is None, indicating that no State object
    # with the given ID was found.
    if state is None:
        # Return a JSON response with a 404 error indicating "Not found."
        abort(404)

    # Attempt to retrieve JSON data from the request body.
    data = request.get_json()

    # Check if the 'data' variable is None, indicating that the request body
    # is not valid JSON.
    if data is None:
        # Return a JSON response with a 400 error and the "Not a JSON" message.
        return (jsonify(error_not_json), 400)

    # Iterate through the 'data' dictionary and update the State object's
    # attributes accordingly.
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    # Save the updated State object to the storage engine.
    state.save()

    # Convert the updated 'state' object to a dictionary
    # using the `to_dict` method.
    state_dict = state.to_dict()

    # Return a JSON representation of the updated State with status code 200.
    return (jsonify(state_dict), 200)
