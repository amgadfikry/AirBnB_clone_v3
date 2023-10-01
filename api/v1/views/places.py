#!/usr/bin/python3
"""
API Routes for Place Objects.

This module defines routes for performing RESTful API actions on Place objects.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>

Routes:
    - /cities/<city_id>/places: Retrieves list of all Place objects of a City.
    - /places/<place_id>: Retrieves a Place object by its ID.
    - /places_search: Retrieves Place objects based on search criteria.
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City.

    Args:
        city_id: The ID of the City to retrieve places for.

    Returns:
        JSON representation of all Place objects in the City.
        404 error if the city_id is not linked to any City object.
    """
    # Attempt to retrieve a City object from the storage engine by its ID.
    city = storage.get(City, city_id)

    # Check if the 'city' variable is None, indicating that no City object
    # with the provided ID was found.
    if city is None:
        # Raise a 404 error response.
        abort(404)

    # Create a list of dictionaries representing Place objects within the City.
    places = [place.to_dict() for place in city.places]

    # Return the 'places' list as a JSON response.
    return (jsonify(places))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object by its ID.

    Args:
        place_id: The ID of the Place object to retrieve.

    Returns:
        JSON representation of the Place object.
        404 error if the place_id is not linked to any Place object.
    """
    # Attempt to retrieve a Place object from the storage engine by its ID.
    place = storage.get(Place, place_id)

    # Check if the 'place' variable is None, indicating that no Place object
    # with the provided ID was found.
    if place is None:
        # Raise a 404 error response.
        abort(404)

    # Convert the retrieved 'place' object to a dictionary.
    place_dict = place.to_dict()

    # Return the 'place_dict' as a JSON response.
    return (jsonify(place_dict))


@app_views.route(
    '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object by its ID.

    Args:
        place_id: The ID of the Place object to delete.

    Returns:
        An empty dictionary with the status code 200.
        404 error if the place_id is not linked to any Place object.
    """
    # Attempt to retrieve a Place object from the storage engine by its ID.
    place = storage.get(Place, place_id)

    # Check if the 'place' variable is None, indicating that no Place object
    # with the provided ID was found.
    if place is None:
        # Raise a 404 error response.
        abort(404)

    # Delete the 'place' object from the storage engine.
    storage.delete(place)

    # Save the changes in the storage engine.
    storage.save()

    # Return an empty dictionary as a JSON response with status code 200.
    return (jsonify({}))


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place.

    Args:
        city_id: The ID of the City in which to create the Place.

    Returns:
        JSON representation of the new Place with the status code 201.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
        404 error if the city_id is not linked to any City object.
        400 error with the message "Missing user_id" or "Missing name"
            if the dictionary doesn't contain the respective keys.
        404 error if the user_id is not linked to any User object.
    """
    # Attempt to retrieve a City object from the storage engine by its ID.
    city = storage.get(City, city_id)

    # Check if the 'city' variable is None, indicating that no City object
    # with the provided ID was found.
    if city is None:
        # Raise a 404 error response.
        abort(404)

    # Attempt to retrieve JSON data from the request body.
    data = request.get_json()

    # Define error messages as variables
    error_not_json = {"error": "Not a JSON"}
    error_missing_user_id = {"error": "Missing user_id"}
    error_missing_name = {"error": "Missing name"}

    # Check if the 'data' variable is None, indicating that the request body
    # is not valid JSON.
    if data is None:
        # Return a JSON response with a 400 error and the "Not a JSON" message.
        return (jsonify(error_not_json), 400)

    # Check if the 'data' dictionary contains the key 'user_id'.
    if 'user_id' not in data:
        # Return a JSON response with a 400 error
        # and the "Missing user_id" message.
        return (jsonify(error_missing_user_id), 400)

    # Check if the 'data' dictionary contains the key 'name'.
    if 'name' not in data:
        # Return a JSON response with a 400 error
        # and the "Missing name" message.
        return (jsonify(error_missing_name), 400)

    # Add 'user_id' to the 'data' dictionary.
    user_id = data['user_id']

    # Attempt to retrieve a User object from the storage engine by its ID
    user = storage.get(User, user_id)

    # Check if the 'user' variable is None, indicating that no User object
    # with the provided ID was found.
    if user is None:
        # Raise a 404 error response.
        abort(404)

    # Add 'city_id' to the 'data' dictionary.
    data['city_id'] = city_id

    # Create a new Place object using the provided JSON data.
    new_place = Place(**data)

    # Save the new Place object to the storage engine.
    new_place.save()

    # Convert the newly created 'place' object to a dictionary.
    place_dict = new_place.to_dict()

    # Return a JSON representation of the new Place with status code 201.
    return (jsonify(place_dict), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object by its ID.

    Args:
        place_id: The ID of the Place object to update.

    Returns:
        JSON representation of the updated Place object with status code 200.
        404 error if the place_id is not linked to any Place object.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
    """
    # Attempt to retrieve a Place object from the storage engine by its ID.
    place = storage.get(Place, place_id)

    # Check if the 'place' variable is None, indicating that no Place object
    # with the provided ID was found.
    if place is None:
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

    # Iterate through the 'data' dictionary and update the Place object's
    # attributes accordingly.
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    # Save the updated Place object to the storage engine.
    place.save()

    # Convert the updated 'place' object to a dictionary.
    place_dict = place.to_dict()

    # Return a JSON representation of the updated City with status code 200.
    return (jsonify(place_dict), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves Place objects based on search criteria from JSON request body.

    Returns:
        JSON representation of the filtered Place objects.
        400 error with the message "Not a JSON"
            if the request body is not valid JSON.
    """
    # Attempt to retrieve JSON data from the request body.
    data = request.get_json()

    # Define error message as variable
    error_not_json = {"error": "Not a JSON"}

    # Check if the 'data' variable is None, indicating that the request body
    # is not valid JSON.
    if data is None:
        # Return a JSON response with a 400 error and the "Not a JSON" message.
        return (jsonify(error_not_json), 400)

    # Get search criteria from the JSON data
    if data and len(data):
        # Extract states, cities, and amenities from the JSON data
        states = data.get("states", [])
        cities = data.get("cities", [])
        amenities = data.get("amenities", [])

    # Retrieve all places if no search criteria are specified
    if (
        not data or not len(data) or (
            not states and not cities and not amenities)):
        # If no search criteria provided, fetch all places and return as JSON
        places = storage.all(Place).values()

        # Create a list of dictionaries,
        # where each dictionary is a representation of a place
        # by calling the to_dict() method on each place in places
        place_dicts = [place.to_dict() for place in places]

        # Return the JSON response for all places
        return jsonify(place_dicts)

    # Initialize an empty list to store filtered places
    filtered_places = []

    # Helper function to add places from a specific city to the result
    def add_city_places(city_id):
        """
        Add places associated with a given city to the filtered_places list.

        Args:
            city_id (int): The ID of the city whose places are to be added.
        """
        # Retrieve the city object from the data storage using its ID
        city = storage.get(City, city_id)

        # If the city object was found in the data storage
        if city:
            # Add all places associated with the given city
            # to the filtered_places list
            filtered_places.extend(city.places)

    # Handle states and cities inclusion
    for state_id in states:
        # Retrieve the State object from the data storage using its ID
        state = storage.get(State, state_id)

        # If the State object was found in the data storage,
        if state:
            # iterate through the cities within the selected state
            for city in state.cities:
                # Add places from each city within the selected states
                add_city_places(city.id)

    for city_id in cities:
        # Add places from each individual city selected
        add_city_places(city_id)

    # Filter places based on amenities
    if amenities:
        # Check if any amenities were selected for filtering
        if not filtered_places:
            # If no places have been filtered yet, consider all places
            filtered_places = storage.all(Place).values()

        # Create a list of Amenity objects corresponding to
        # the selected amenity IDs
        amenities_obj = [
            # Retrieve Amenity object for each amenity_id
            storage.get(Amenity, amenity_id)
            # Iterate through the selected amenity IDs
            for amenity_id in amenities
        ]

        # Filter places to only include those with all selected amenities
        filtered_places = [
            place  # Keep the place if it meets the following conditions
            for place in filtered_places  # Iterate through filtered places
            if all([
                # Check if each amenity is in the place's amenities
                amenity in place.amenities
                for amenity in amenities_obj  # Iterate through amenities_obj
            ])
        ]

    # Create the final list of places without 'amenities' in the response
    places = [
        # Iterate through the filtered places & prepare each place's dictionary
        {
            key: value  # Keep key-value pairs
            # Convert the place object to a dictionary representation
            for key, value in place.to_dict()
            if key != "amenities" # Exclude 'amenities' key
        }
        for place in filtered_places  # Iterate through filtered places
    ]

    # Return the filtered places as JSON response
    return (jsonify(places))
