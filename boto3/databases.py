#!/usr/bin/env python

from peewee import *

db = SqliteDatabase('students.db')


class Student(Model):
    username = CharField(max_length=255, unique=True)
    points = IntegerField(default=0)

    class Meta:
        database = db

students = [
    {"username": "klove", "points": 10004},
    {"username": "sunny", "points": 10002},
    {"username": "hunny", "points": 10005},
    {"username": "moon", "points": 1000}
]


def add_students():
    try:
        for student in students:
            Student.create(username=student['username'],
                           points=student['points'])
    except IntegrityError:
        for student in students:
            student_record = Student.get(username=student['username'])
            student_record.points = student['points']
            student_record.save()


def top_student():
    student = Student.select().order_by(Student.points.desc()).get()
    return student

if __name__ == '__main__':
    db.connect()
    db.create_tables([Student], safe=True)
    add_students()
    print("Our top student right now is: {0.username}".format(top_student()))


if not db.connect():