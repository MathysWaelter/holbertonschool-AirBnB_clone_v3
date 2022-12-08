#!/usr/bin/python3
"""
States Object method
"""
from api.v1.views import app_views, storage
from flask import jsonify, request, abort
import json
from models.state import State
from api.v1.app import handler_error


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_list():
    """
    list all state
    """
    if request.method == "GET":
        all_state = []
        storagest = storage.all("State")
        for state in storagest.values():
            all_state.append(state.to_dict())
            json.dumps(all_state)
        return json.dumps(all_state, sort_keys=True, indent=4)

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_select(state_id):
    """
    select state by id
    """
    if request.method == "GET":
        storagest = storage.all("State")
        for state in storagest.values():
            if state.id == state_id:
                state_dict = (state.to_dict())
                return json.dumps(state_dict, sort_keys=True, indent=4)
        return handler_error(404)

@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def state_delete(state_id):
    """
    delete state by id
    """
    if request.method == "DELETE":
        for state in storage.all("State").values():
            if state.id == state_id:
                storage.delete(state)
                storage.save()
                return {}
        return handler_error(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    create state by id
    """
    new_state = request.get_json(silent=True)
    if not new_state:
        return abort(400, {"Not a JSON"})
    if "name" not in new_state.keys():
        return abort(400, {"Missing name"})
    new_obj = State(name=new_state['name'])
    storage.new(new_obj)
    storage.save()
    return json.dumps(new_obj.to_dict(), 201, sort_keys=True, indent=4)