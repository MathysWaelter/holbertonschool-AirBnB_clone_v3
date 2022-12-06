#!/usr/bin/python3

from flask import jsonify, Flask
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify(status='OK')