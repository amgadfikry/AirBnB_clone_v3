#!/usr/bin/python3
"""
Handles RESTful API actions for the link between Place and Amenity objects.

This module provides endpoints to manage the relationship
between Place and Amenity objects
in the API.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>

Routes:
- GET /places/<place_id>/amenities: Retrieve all Amenity objects of a Place.
- DELETE /places/<place_id>/amenities/<amenity_id>:
                            Delete an Amenity linked to a Place.
- POST /places/<place_id>/amenities/<amenity_id>: Link an Amenity to a Place.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route(
    '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place.

    Args:
        place_id (str): The ID of the Place to retrieve amenities for.

    Returns:
        JSON representation of all Amenity objects linked to the Place.
        404 error if the place_id is not linked to any Place object.
    """
    # Retrieve the Place object using its ID
    place = storage.get(Place, place_id)

    # Check if the Place object exists
    if place is None:
        # Raise a 404 error response.
        abort(404)

    # Create a list of dictionaries representing linked Amenity objects
    amenities = [amenity.to_dict() for amenity in place.amenities]

    # Return the JSON response for all amenities in the place
    return (jsonify(amenities))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object linked to a Place.

    Args:
        place_id (str): The ID of the Place.
        amenity_id (str): The ID of the Amenity to delete.

    Returns:
        An empty dictionary with the status code 200.
        404 error if the place_id is not linked to any Place object,
        the amenity_id is not linked to any Amenity object,
        or the Amenity is not linked to the Place before the request.
    """
    # Retrieve the Place and Amenity objects using their IDs
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    # Check if the Place, Amenity, or their link exist
    if place is None or amenity is None or amenity not in place.amenities:
        # Raise a 404 error response.
        abort(404)

    # Remove the Amenity from the Place's amenities and save
    place.amenities.remove(amenity)

    # Save the changes in the storage engine.
    place.save()

    # Return an empty dictionary as a JSON response with status code 200.
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place.

    Args:
        place_id (str): The ID of the Place.
        amenity_id (str): The ID of the Amenity to link.

    Returns:
        JSON representation of the linked Amenity with the status code 201.
        404 error if the place_id is not linked to any Place object
        or the amenity_id is not linked to any Amenity object.
        200 status code if the Amenity is already linked to the Place.
    """
    # Retrieve the Place and Amenity objects using their IDs
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    # Check if the Place and Amenity objects exist
    if place is None or amenity is None:
        # Raise a 404 error response.
        abort(404)

    # Check if the Amenity is already linked to the Place
    if amenity in place.amenities:
        # If the Amenity is already linked,
        # convert it to a dictionary representation.
        amenity_dict = amenity.to_dict()
        # Return a JSON representation of the linked Amenity
        # with a status code of 200 (OK).
        return (jsonify(amenity_dict), 200)

    # Link the Amenity to the Place and save
    place.amenities.append(amenity)

    # Save the changes in the storage engine.
    place.save()

    # Convert the linked 'amenity' object to a dictionary representation.
    amenity_dict = amenity.to_dict()

    # Return a JSON representation of the linked Amenity
    # with a status code of 201 (Created)
    return (jsonify(amenity_dict), 201)
