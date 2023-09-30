#!/usr/bin/python3
"""
API Routes for User Objects.

This module defines routes for performing RESTful API actions on User objects.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>

Routes:
    - /users: Retrieves the list of all User objects.
    - //users/<user_id>: Retrieves a User object by its ID.
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
    # Retrieve a list of all User objects from the storage engine.
    all_users = storage.all(User)

    # Convert each User object to a dictionary using the `to_dict` method,
    # and store them in a list called 'users'.
    users = [user.to_dict() for user in all_users.values()]

    # Return the list of 'users' as a JSON response.
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
    # Attempt to retrieve a User object from the storage engine by its ID.
    user = storage.get(User, user_id)

    # Check if the 'user' variable is None, indicating that
    # no User object with the provided ID was found.
    if user is None:
        # Raise a 404 error response.
        abort(404)

    # Convert the retrieved 'user' object to a dictionary
    # using the `to_dict` method.
    user_dict = user.to_dict()

    # Return the 'user_dict' as a JSON response.
    return (jsonify(user_dict))


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
    # Attempt to retrieve a User object from the storage engine by its ID.
    user = storage.get(User, user_id)

    # Check if the 'user' variable is None, indicating that
    # no User object with the provided ID was found.
    if user is None:
        # Raise a 404 error response.
        abort(404)

    # Delete the 'user' object from the storage engine.
    storage.delete(user)

    # Save the changes in the storage engine
    storage.save()

    # Return an empty dictionary as a JSON response with status code 200.
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
    # Attempt to retrieve JSON data from the request body.
    data = request.get_json()

    # Define error messages as variables
    error_not_json = {"error": "Not a JSON"}
    error_missing_email = {"error": "Missing email"}
    error_missing_password = {"error": "Missing password"}

    # Check if the 'data' variable is None, indicating that the request body
    # is not valid JSON.
    if data is None:
        # Return a JSON response with a 400 error and the "Not a JSON" message.
        return (jsonify(error_not_json), 400)

    # Check if the 'data' dictionary contains the key 'email'.
    if 'email' not in data:
        # Return a JSON response with a 400 error
        # and the "Missing email" message.
        return (jsonify(error_missing_email), 400)

    # Check if the 'data' dictionary contains the key 'password'.
    if 'password' not in data:
        # Return a JSON response with a 400 error
        # and the "Missing password" message.
        return (jsonify(error_missing_password), 400)

    # Create a new User object using the provided JSON data.
    new_user = User(**data)

    # Save the new User object to the storage engine.
    new_user.save()

    # Convert the newly created 'user' object to a dictionary
    # using the `to_dict` method.
    user_dict = new_user.to_dict()
    return (jsonify(user_dict), 201)


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
    # Attempt to retrieve the User object by its ID from storage.
    user = storage.get(User, user_id)

    # Define error message as variable
    error_not_json = {"error": "Not a JSON"}

    # Check if the retrieved user is None, indicating that no User object
    # with the given ID was found.
    if user is None:
        # Return a JSON response with a 404 error indicating "Not found."
        abort(404)

    # Attempt to retrieve JSON data from the request body.
    data = request.get_json()

    # Check if the 'data' variable is None, indicating that the request body
    # is not valid JSON.
    if data is None:
        # Return a JSON response with a 400 error and the "Not a JSON" message.
        return (jsonify(error_not_json), 400)

    # Iterate through the 'data' dictionary and update the User object's
    # attributes accordingly.
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at', 'password']:
            setattr(user, key, value)

    # Save the updated User object to the storage engine.
    user.save()

    # Convert the updated 'user' object to a dictionary
    # using the `to_dict` method.
    user_dict = user.to_dict()

    return (jsonify(user_dict), 200)
