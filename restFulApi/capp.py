#!/usr/bin/env python
import json
from flask import jsonify, Blueprint, Flask, make_response

from flask_restful import (Resource, Api, reqparse, inputs, fields,
                           marshal, marshal_with, url_for, abort)

import models
from resources.config import *

count_fields = {
    "count": fields.Integer,
}

course_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "url": fields.String,
    "reviews": fields.List(fields.String)
}

app = Flask(__name__)


@app.route('/')
def helloworld():
    return "Hello World!!!"


@marshal_with(count_fields)
@app.route('/api/v1/<action>/<item>', methods=['GET'])
def api_action(action, item):
    actions = ['count', 'ids', 'tags']
    if action in actions:
        if action == 'count':
            response = models.Course.select().where(models.Course.title.contains(item)).count()
            return make_response(json.dumps({
                'count': response
            }))
        elif action == 'ids':
            response = models.Course.select().where(models.Course.url != '').count()
            return make_response(json.dumps({
                'count': response
            }))
    else:
        return make_response(json.dumps({
            'error': 'Not a valid action'
        }))
            #print response


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)