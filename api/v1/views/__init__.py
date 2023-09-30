#!/usr/bin/python3
"""
Initialization of API version 1 views package.

This package contains views for the API version 1 of the AirBnB Clone project.
- It provides endpoints and routes for various functionalities
- related to managing data entities such as states, cities, amenities,
    users, places, reviews, and amenities for accommodations.

Authors:
    - Dr. Dyrane Alexander <Ogranya.Alex@gmail.com>
    - Amgad Fikry Mohamed <dr.amgad_sh92@yahoo.com>

Modules:
    - index: Index view for status endpoint
    - states: Views for managing states data
    - cities: Views for managing cities data
    - amenities: Views for managing amenities data
    - users: Views for managing user data
    - places: Views for managing places data
    - places_reviews: Views for managing place reviews data
    - places_amenities: Views for managing place amenities data

Attributes:
    - app_views: Blueprint instance for API version 1 views
    - url_prefix: Prefix for API endpoints
"""

from flask import Blueprint


# Create a Blueprint instance for API version 1 views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


# Import views from submodules
if (__name__ == 'api.v1.views'):
    from api.v1.views.index import *             # Import index view
    from api.v1.views.states import *            # Import states view
    from api.v1.views.cities import *            # Import cities view
    from api.v1.views.amenities import *         # Import amenities view
    from api.v1.views.users import *             # Import users view
    from api.v1.views.places import *            # Import places view
    from api.v1.views.places_reviews import *    # Import places_reviews view
    from api.v1.views.places_amenities import *  # Import places_amenities view
