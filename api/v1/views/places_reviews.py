#!/usr/bin/python3
"""
Handles RESTful API actions for Review objects.
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
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
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
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
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
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
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
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in data:
        return (jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in data:
        return (jsonify({"error": "Missing text"}), 400)
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
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
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in [
            'id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return (jsonify(review.to_dict()), 200)
