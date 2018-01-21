#!/usr/bin/env python

import json

from argon2 import PasswordHasher
from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (Resource, Api, reqparse, inputs, fields,
                           marshal, marshal_with, url_for, abort)

import models
HASHER = PasswordHasher()

user_fields = {
    'username': fields.String,
}


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
                'username',
                required=True,
                help='No username not provied',
                location=['form', 'json']
        )
        self.reqparse.add_argument(
                'email',
                required=True,
                help='No email address provided',
                location=['form', 'json'],
        )
        self.reqparse.add_argument(
                'password',
                required=True,
                help='No password provided',
                location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super(UserList, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        if args.get('password') == args.get('verify_password'):
            args['password'] = HASHER.hash(args.get('password'))
            user = models.User.create(**args)
            return marshal(user, user_fields), 201
        return make_response(
            json.dumps({
                "error": "password and password verification do not match"
            }), 400)

users_api = Blueprint('resources.user', __name__)
api = Api(users_api)
api.add_resource(
        UserList,
        "/users",
        endpoint='users'
)