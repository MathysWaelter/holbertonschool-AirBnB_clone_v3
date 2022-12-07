#!/usr/bin/python3
"""
for start my api
"""
from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(excepte):
    """closes the storage on teardown"""

    storage.close()


@app.errorhandler(404)
def handler_error(self):
    """returns a JSON-formatted 404 status code response"""
    format_error = {
        "error": "Not found"
    }
    status_code = 404
    return make_response(jsonify(format_error), status_code)


if __name__ == "__main__":
    hostapi = getenv('HBNB_API_HOST', default='0.0.0.0')
    portapi = getenv('HBNB_API_PORT', default=5000)
    app.run(host=hostapi, port=int(portapi), threaded=True)
