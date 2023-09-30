#!/usr/bin/python3
"""
Handles RESTful API actions for Review objects.

This module provides endpoints to perform CRUD operations on Review objects
in the API.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>

Routes:
- GET /places/<place_id>/reviews: Retrieve all Review objects of a Place.
- GET /reviews/<review_id>: Retrieve a specific Review object by ID.
- DELETE /reviews/<review_id>: Delete a specific Review object by ID.
- POST /places/<place_id>/reviews: Create a new Review object for a Place.
- PUT /reviews/<review_id>: Update a specific Review object by ID.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.

    Args:
        place_id: The ID of the Place to retrieve reviews for.

    Returns:
        JSON representation of all Review objects in the Place.
        404 error if the place_id is not linked to any Place object.
    """
    # Retrieve the Place object using its ID
    place = storage.get(Place, place_id)

    # Check if the Place object exists
    if place is None:
        # Raise a 404 error response.
        abort(404)

    # Create a list of dictionaries representing linked Review objects
    reviews = [review.to_dict() for review in place.reviews]

    # Return the JSON response for all reviews in the place
    return (jsonify(reviews))


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object by its ID.

    Args:
        review_id: The ID of the Review object to retrieve.

    Returns:
        JSON representation of the Review object.
        404 error if the review_id is not linked to any Review object.
    """
    # Retrieve the Review object using its ID
    review = storage.get(Review, review_id)

    # Check if the Review object exists
    if review is None:
        # Raise a 404 error response.
        abort(404)

    # Return the JSON response for the review
    return (jsonify(review.to_dict()))


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by its ID.

    Args:
        review_id: The ID of the Review object to delete.

    Returns:
        An empty dictionary with the status code 200.
        404 error if the review_id is not linked to any Review object.
    """
    # Retrieve the Review object using its ID
    review = storage.get(Review, review_id)

    # Check if the Review object exists
    if review is None:
        # Raise a 404 error response.
        abort(404)

    # Delete the Review object and save the changes
    storage.delete(review)
    storage.save()

    # Return an empty dictionary as a JSON response with status code 200.
    return (jsonify({}))


@app_views.route(
    '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review.

    Args:
        place_id: The ID of the Place in which to create the Review.

    Returns:
        JSON representation of the new Review with the status code 201.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
        404 error if the place_id is not linked to any Place object.
        400 error with the message "Missing user_id" or "Missing text"
            if the dictionary doesn't contain the respective keys.
        404 error if the user_id is not linked to any User object.
    """
    # Retrieve the Place object using its ID
    place = storage.get(Place, place_id)

    # Check if the Place object exists
    if place is None:
        # Raise a 404 error response.
        abort(404)

    # Get the request data as JSON
    data = request.get_json()

    # Define error messages as variables
    error_not_json = {"error": "Not a JSON"}
    error_missing_user_id = {"error": "Missing user_id"}
    error_missing_text = {"error": "Missing text"}

    # Check if the request data is valid JSON
    if data is None:
        # Return a JSON response with a 400 error and the "Not a JSON" message.
        return (jsonify(error_not_json), 400)

    if 'user_id' not in data:
        # Return a JSON response with a 400 error
        # and the "Missing user_id" message.
        return (jsonify(error_missing_user_id), 400)

    if 'text' not in data:
        # Return a JSON response with a 400 error
        # and the "Missing text" message.
        return (jsonify(error_missing_text), 400)

    # Retrieve the User object using 'user_id'
    user_id = data['user_id']
    user = storage.get(User, user_id)

    # Check if the User object exists
    if user is None:
        # Raise a 404 error response.
        abort(404)

    # Add 'place_id' to the data
    data['place_id'] = place_id

    # Create a new Review object and save it
    new_review = Review(**data)
    new_review.save()

    # Return a JSON representation of the new Review with status code 201
    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object by its ID.

    Args:
        review_id: The ID of the Review object to update.

    Returns:
        JSON representation of the updated Review object with status code 200.
        404 error if the review_id is not linked to any Review object.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
    """
    # Retrieve the Review object using its ID
    review = storage.get(Review, review_id)

    # Check if the Review object exists
    if review is None:
        # Raise a 404 error response.
        abort(404)
    
    # Get the request data as JSON
    data = request.get_json()

    # Check if the request data is valid JSON
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    # Update the Review object with the request data
    for key, value in data.items():
        # Define keys to ignore in the update
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        if key not in ignore_keys:
            setattr(review, key, value)

    # Save the changes to the Review object
    review.save()

     # Return a JSON representation of the updated Review with status code 200
    return (jsonify(review.to_dict()), 200)
