#!/usr/bin/env python

from flask import jsonify, Blueprint, make_response, json

from flask_restful import (Resource, Api, reqparse, inputs, fields,
                           marshal, marshal_with, url_for, abort)

from argon2 import PasswordHasher
from auth import auth
import models

HASHER = PasswordHasher()


class PasswordReset(Resource):
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
            required=False,
            nullable=True,
            default='',
            location=['form', 'json']
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

        super(PasswordReset, self).__init__()

    def put(self):
        args = self.reqparse.parse_args()
        try:
            user = models.User.get(models.User.username == args.get('username'))
        except models.User.DoesNotExist:
            return make_response(json.dumps({
                'error': 'User does not exist'}), 404)
        else:
            if args.get('password') != args.get('verify_password'):
                return make_response(json.dumps({
                    'error': 'Password does not match'}), 404)
            else:
                args['password'] = HASHER.hash(args.get('password'))
                del args['verify_password']
                user.update(**args).execute()
                return make_response(json.dumps({
                    'success': 'Your password has been reset successfully!'
                }))

password_api = Blueprint('passwordreset', __name__)
api = Api(password_api)
api.add_resource(
        PasswordReset,
        "/api/v1/users/password-reset",
        endpoint='password-reset'
)

