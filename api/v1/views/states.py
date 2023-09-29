#!/usr/bin/python3
"""
Handles RESTful API actions for State objects.
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
    states = [state.to_dict() for state in storage.all(State).values()]
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
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()))


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
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
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
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


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
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return (jsonify(state.to_dict()), 200)
