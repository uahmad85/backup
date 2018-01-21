#!/usr/bin/env python
import datetime

from peewee import *

DATABASE = SqliteDatabase('courses.db')

class Course(Model):
    title = CharField()
    url = CharField(unique=True)
    create_at = D
