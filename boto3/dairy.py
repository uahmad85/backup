#!/usr/bin/env python

from collections import OrderedDict
import datetime
import sys

from peewee import *

db = SqliteDatabase("dairy.db")


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and the table if not exists"""
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit")
        for key, val in menu.items():
            print("{}) {}".format(key, val.__doc__))
        choice = raw_input("Action: ").lower().strip()

        if choice in menu:
            menu[choice]()


def add_entry():
    """Add an entry"""
    print("Enter your entry. Press ctrl+d when finished")
    data = sys.stdin.read().strip()

    if data:
        if raw_input("Save entry?, [yn] ").lower() != 'n':
            Entry.create(content=data)
            print("Save successfully")


def view_entry(search_query=None):
    """View previous entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M%p")
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('n) next entry')
        print('q) return to main manu')


def search_entry():
    """Search entry"""
    view_entry(raw_input("Search query: "))


def delete_entry(entry):
    """Delete an Entry"""

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entry),
    ('s', search_entry)
])

if __name__ == "__main__":
    initialize()
    menu_loop()
