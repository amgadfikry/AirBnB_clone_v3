#!/usr/bin/python3
"""
Handles RESTful API actions for User objects.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects.

    Returns:
        JSON representation of all User objects.
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return (jsonify(users))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object by its ID.

    Args:
        user_id: The ID of the User object to retrieve.

    Returns:
        JSON representation of the User object.
        404 error if the user_id is not linked to any User object.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return (jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object by its ID.

    Args:
        user_id: The ID of the User object to delete.

    Returns:
        An empty dictionary with the status code 200.
        404 error if the user_id is not linked to any User object.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User.

    Returns:
        JSON representation of the new User with the status code 201.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
        400 error with the message "Missing email" or "Missing password"
            if the dictionary doesn't contain the respective keys.
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**data)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object by its ID.

    Args:
        user_id: The ID of the User object to update.

    Returns:
        JSON representation of the updated User object with status code 200.
        404 error if the user_id is not linked to any User object.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at', 'password']:
            setattr(user, key, value)
    user.save()
    return (jsonify(user.to_dict()), 200)
