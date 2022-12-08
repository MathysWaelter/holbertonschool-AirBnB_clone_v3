#!/usr/bin/python3
"""
users Object method
"""
from api.v1.views import app_views, storage
from flask import jsonify, request, abort, Flask
import json
from models.user import User
from api.v1.app import handler_error

app = Flask(__name__)


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_list():
    """
    list all user
    """
    if request.method == "GET":
        all_user = []
        storagest = storage.all("User")
        for user in storagest.values():
            all_user.append(user.to_dict())
        return jsonify(all_user), 200


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def user_select(user_id):
    """
    select user by id
    """
    if request.method == "GET":
        storagest = storage.all("User")
        storageamen = storagest.get('User' + "." + user_id)
        if storageamen is None:
            abort(404)
        else:
            return jsonify(storageamen.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def user_delete(user_id):
    """
    delete user by id
    """
    if request.method == "DELETE":
        for user in storage.all("user").values():
            if user is None:
                abort(404)
            if user.id == user_id:
                storage.delete(user)
                storage.save()
                return {}
        return handler_error(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    create user by id
    """
    new_user = request.get_json(silent=True)
    if not new_user:
        return abort(400, {"Not a JSON"})
    if "name" not in new_user.keys():
        return abort(400, {"Missing name"})
    new_obj = User(name=new_user['name'])
    storage.new(new_obj)
    storage.save()
    return new_obj.to_dict(), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def user_update(user_id):
    """
    update user by id
    """
    new = request.get_json(silent=True)
    if not new:
        return abort(400, {"Not a JSON"})
    old = storage.get(User, user_id)
    if not old:
        return handler_error(404)
    for key, value in new.items():
        if key not in ['id', 'created_at']:
            setattr(old, key, value)
    storage.save()
    return jsonify(old.to_dict())
