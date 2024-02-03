#!/usr/bin/python3
'''user api'''
from flask import request, abort, jsonify, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_user():
    '''return all users'''
    users = [users.to_dict() for users in storage.all(User).values()]

    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_by_id(user_id):
    '''return user by id'''
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    user = user.to_dict()

    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_by_id(user_id):
    '''delete by id'''
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    '''create user instance'''
    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'email' not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)

    newu = User(**data)
    newu.save()
    newu = newu.to_dict()
    return jsonify(newu), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    '''update user instance'''
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in data.items():
        if key == 'id' or key == 'email':
            continue
        if key == 'created_at' or key == 'updated_at':
            continue
        setattr(user, key, value)
    storage.save()
    user = user.to_dict()

    return jsonify(user), 200