#!/usr/bin/python3
""" module that make api for places table """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def all_cplaces(city_id):
    """ function that manage route of all places """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        li = []
        for o in obj.places:
            li.append(o.to_dict())
        return jsonify(li), 200
    else:
        header = request.get_json()
        if header is None or type(header) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        elif "user_id" not in header:
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get(User, header.get('user_id'))
        if user is None:
            abort(404)
        elif "name" not in header:
            return jsonify({"error": "Missing name"}), 400
        else:
            header['city_id'] = city_id
            new = Place(**header)
            new.save()
            return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT', 'DELETE', 'GET'], strict_slashes=False)
def id_places(place_id):
    """ function that manange route for place by id """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(obj.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        header = request.get_json()
        if header is None or type(header) is not dict:
            return jsonify({"error": "Not a JSON"}), 400
        for k, v in header.items():
            if k not in ['id', 'created_at',
                         'updated_at', 'city_id', 'user_id']:
                setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict()), 200


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def search_places():
    """ methods that search places by critria """
    header = request.get_json()
    if header is None or type(header) is not dict:
        return jsonify({"error": "Not a JSON"}), 400
    states = header.get('states')
    cities = header.get('cities')
    amenities = header.get('amenities')
    all = []
    if not len(header) or (not len(states) and not len(cities)):
        li = [i.to_dict() for i in storage.all(Place).values()]
        return jsonify(li)
    elif len(states) > 0 and len(cities) == 0:
        for state in states:
            obj = storage.get(State, state)
            for city in state.cities:
                li = [place for place in city.places]
                all.extend(li)
    elif len(states) == 0 and len(cities) > 0:
        for city in cities:
            obj = storage.get(City, city)
            li = [place for place in city.places]
            all.extend(li)
    elif len(states) > 0 and len(cities) > 0:
        for state in states:
            obj_s = storage.get(State, state)
            for c in obj_s.cities:
                if c.to_dict().get('id') in cities:
                    pass
                li = [place for place in c.places]
                all.extend(li)
        for city in cities:
            obj_c = storage.get(City, city)
            li = [place for place in obj_c.places]
            all.extend(li)

    if len(amenities) > 0:
        res = []
        for p in all:
            add = True
            for amen in amenities:
                obj = storage.get(Amenity, amen)
                if obj not in p.amenities:
                    add = False
                    break
            if add:
                res.append(p.to_dict())
        return jsonify(res)
    return jsonify([p.to_dict() for p in all])
