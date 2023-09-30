#!/usr/bin/python3
"""
API Routes for Amenity Objects.

This module defines routes for performing RESTful API actions on Amenity objects.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>

Routes:
    - /amenities: Retrieves the list of all Amenity objects.
    - /amenities/<amenity_id>: Retrieves an Amenity object by its ID.
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
    # Retrieve a list of all Amenity objects from the storage engine.
    all_amenities = storage.all(Amenity)

    # Convert each Amenity object to a dictionary using the `to_dict` method,
    # and store them in a list called 'amenities'.
    amenities = [amenity.to_dict() for amenity in all_amenities.values()]

    # Return the list of 'amenities' as a JSON response.
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
    # Attempt to retrieve a Amenity object from the storage engine by its ID.
    amenity = storage.get(Amenity, amenity_id)

    # Check if the 'amenity' variable is None, indicating that
    # no Amenity object with the provided ID was found.
    if amenity is None:
        # Raise a 404 error response.
        abort(404)

    # Convert the retrieved 'amenity' object to a dictionary
    # using the `to_dict` method.
    amenity_dict = amenity.to_dict()

    # Return the 'amenity_dict' as a JSON response.
    return (jsonify(amenity_dict))


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
    # Attempt to retrieve a Amenity object from the storage engine by its ID.
    amenity = storage.get(Amenity, amenity_id)

    # Check if the 'amenity' variable is None, indicating that
    # no Amenity object with the provided ID was found.
    if amenity is None:
        # Raise a 404 error response.
        abort(404)

    # Delete the 'amenity' object from the storage engine.
    storage.delete(amenity)

    # Save the changes in the storage engine
    storage.save()

    # Return an empty dictionary as a JSON response with status code 200.
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

    # Create a new Amenity object using the provided JSON data.
    new_amenity = Amenity(**data)

    # Save the new Amenity object to the storage engine.
    new_amenity.save()

    # Convert the newly created 'amenity' object to a dictionary
    # using the `to_dict` method.
    amenity_dict = new_amenity.to_dict()

    # Return a JSON representation of the new State with status code 201.
    return (jsonify(amenity_dict), 201)


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
    # Attempt to retrieve the Amenity object by its ID from storage.
    amenity = storage.get(Amenity, amenity_id)

    # Define error message as variable
    error_not_json = {"error": "Not a JSON"}

    # Check if the retrieved amenity is None, indicating that no Amenity object
    # with the given ID was found.
    if amenity is None:
        # Return a JSON response with a 404 error indicating "Not found."
        abort(404)

    # Attempt to retrieve JSON data from the request body.
    data = request.get_json()

    # Check if the 'data' variable is None, indicating that the request body
    # is not valid JSON.
    if data is None:
        # Return a JSON response with a 400 error and the "Not a JSON" message.
        return (jsonify(error_not_json), 400)

    # Iterate through the 'data' dictionary and update the Amenity object's
    # attributes accordingly.
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    # Save the updated Amenity object to the storage engine.
    amenity.save()

    # Convert the updated 'amenity' object to a dictionary
    # using the `to_dict` method.
    amenity_dict = amenity.to_dict()

    return (jsonify(amenity_dict), 200)
