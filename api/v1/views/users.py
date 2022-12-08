#!/usr/bin/python3
"""
States Object method
"""
from api.v1.views import app_views, storage
from flask import jsonify, request, abort
import json
from models.user import User
from api.v1.app import handler_error


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def state_list():
    """
    list all state
    """
    if request.method == "GET":
        all_user = []
        storagest = storage.all("User")
        for user in storagest.values():
            all_user.append(user.to_dict())
            json.dumps(all_user)
        return json.dumps(all_user, sort_keys=True, indent=4)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def state_select(user_id):
    """
    select state by id
    """
    if request.method == "GET":
        storagest = storage.all("User")
        for user in storagest.values():
            if user.id == user_id:
                user_dict = (user.to_dict())
                return json.dumps(user_dict, sort_keys=True, indent=4)
        return handler_error(404)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete(user_id):
    """
    delete state by id
    """
    if request.method == "DELETE":
        for user in storage.all("User").values():
            if user.id == user_id:
                storage.delete(user)
                storage.save()
                return {}
        return handler_error(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def state_create():
    """
    create state by id
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


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def state_update(user_id):
    """
    update state by id
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
