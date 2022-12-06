#!/usr/bin/python3

from api.v1.views import app_view
import json



@app_view.route('/status')
def status():
    return json.dumps("\"status\": \"OK\"")
