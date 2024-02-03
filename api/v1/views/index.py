#!/usr/bin/python3
'''index for the api app'''


from api.v1.views import app_views
from flask import jsonify
from models import storage

jb = {"status": "OK"}


@app_views.route('/status')
def status():
    '''returns json to the route'''
    return jsonify(jb)


@app_views.route('/stats')
def stat():
    '''returns number of each obj by type'''
    return jsonify({"amenities": storage.count('Amenity'),
                    "cities": storage.count('City'),
                    "places": storage.count('Place'),
                    "reviews": storage.count('Review'),
                    "states": storage.count('State'),
                    "users": storage.count('User')})