#!/usr/bin/env python


from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required
import sys

import forms
import models

DEBUG = True
PORT = 8000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = "qoiweyroqiwyeroiuqyweoiryqiowuey"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("you are registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for("index"))
    return render_template('register.html', form=form)


@app.route("/login", methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You are logged in!", "success")
                return redirect(url_for('index'))
        except models.DoesNotExist:
            flash("Your email or password doesn't work", "error")
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("you have been logged out", "success")
    return redirect(url_for("index"))


@app.route('/'route)
def index():
    return 'Hey'

if __name__ == "__main__":
    models.initialize()
    try:
        models.User.create_user(
            username='uahmad',
            email='uahmad85@gmail.com',
            password='password',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT, host=HOST)

autos = ['ms-delivery', 'ms-location', 'mssessions-staging',
         'user-staging','items-server-staging' ]


def update_as_group(group_name, min, max, desired):
    autoscaling = boto3.client('autoscaling')
    autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=group_name, MinSize=min,
            MaxSize=max, DesiredCapacity=desired
    )
