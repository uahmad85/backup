#!/usr/bin/env python

import json
from flask import jsonify, Blueprint, g, make_response

from flask_restful import (Resource, url_for, Api, reqparse, inputs,
                           fields, marshal, marshal_with, abort)

from auth import auth
import models

review_fields = {
    'id': fields.Integer,
    'for_course': fields.String,
    'rating': fields.Integer,
    'comment': fields.String(default=''),
    'created_at': fields.DateTime
}


def review_or_404(review_id):
    try:
        review = models.Review.get(models.Review.id==review_id)
    except models.Review.DoesNotExist:
        abort(404)
    else:
        return review


def add_course(review):
    review.for_course = url_for('resources.courses.course', id=review.course.id)
    return review


class ReviewList(Resource):
    def get(self):
        return {'reviews': [
            marshal(add_course(review), review_fields)
            for review in models.Review.select()
            ]}


class Review(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
                'course',
                required=True,
                type=inputs.positive,
                help='No course name provided',
                location=['form', 'json']
    )
        self.reqparse.add_argument(
                'rating',
                required=True,
                help='No rating provided',
                location=['form', 'json'],
                type=inputs.int_range(1, 5)
        )
        self.reqparse.add_argument(
                'comment',
                required=False,
                nullable=True,
                location=['form', 'json'],
                default=''
        )

    def get(self, id):
        return {'reviews': [
            marshal(add_course(review), review_fields)
            for review in models.Review.select()
            ]}

    @marshal_with(review_fields)
    @auth.login_required
    def post(self, id):
        args = self.reqparse.parse_args()
        review = models.Review.create(created_by=g.user, **args)
        return (add_course(review), 201, {
            'Location': url_for('resources.reviews.review', id=review.id)
        })

    @marshal_with(review_fields)
    @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            review = models.Review.select().where(
                    models.Review.created_by == g.user,
                    models.Review.id == id
            ).get()
        except models.Review.DoesNotExist:
            return make_response(
                    json.dumps({"error": "that review does not exist sucker"}), 403)
        query = review.update(**args)
        query.execute()
        return (add_course(models.Review.get(models.Review.id == id)), 200,
                {'Location': url_for("resources.reviews.review", id=id)})

    @auth.login_required
    def delete(self, id):
        try:
            review = models.Review.select().where(
                    models.Review.created_by == g.user,
                    models.Review.id == id
            ).get()
        except models.Review.DoesNotExist:
            return make_response(
                json.dumps({"error": "that review does not exist sucker"}), 403)
        query = review.delete()
        query.execute()
        return '', 204, {'Location': url_for("resources.reviews.review")}

reviews_api = Blueprint('resources.reviews', __name__)
api = Api(reviews_api)
api.add_resource(
    ReviewList,
    "/reviews",
    endpoint='reviews'
)
api.add_resource(
    Review,
    '/reviews/<int:id>',
    endpoint='review'
)