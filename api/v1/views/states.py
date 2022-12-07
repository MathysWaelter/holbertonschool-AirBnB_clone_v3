#!/usr/bin/python3
"""
States Object method
"""
from api.v1.views import app_views, storage
from flask import jsonify
import json
from models.state import State

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_list():
    """
    list all state
    """
    all_state = []
    all_state = storage.all("State")
    for state in all_state.values():
        all_state.append(state)
    json.dumps(state_list)
    return jsonify(state_list)
