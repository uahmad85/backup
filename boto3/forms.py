#!/usr/bin/env python

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, EqualTo, Length

from models import User


def name_exists(form, field):
    if User.select().where(User.username == field.data):
        raise ValidationError("User with that name already exists.")


def email_exists(form, field):
    if User.select().where(User.email == field.data):
        raise ValidationError("User with this email already exists.")


class RegisterForm(Form):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9]+$',
                message=("Username should be one word, letters,"
                         "numbers and underscores only.")
            ),
            name_exists
        ]
    )
    email = StringField(
            "Email",
            validators=[
                DataRequired(),
                Email(),
                email_exists
            ]
    )
    password = PasswordField(
            "Password",
            validators=[
                DataRequired(),
                Length(min=2),
                EqualTo("password2", message='Passwords must match')
            ]
    )
    password2 = PasswordField(
        "Confirm Password",
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField(
            "Email",
            validators=[
                DataRequired(),
                Email(),
            ]
    )
    password = PasswordField(
            "Password",
            validators=[
                DataRequired(),
            ]
    )
