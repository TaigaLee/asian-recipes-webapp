import os
from peewee import *
import datetime

from flask_login import UserMixin

from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('postgres://mrhydmvthmufgn:0af25c53734478902c2165457f06bdf63ac0a1147966267f8e3888569e207b9c@ec2-34-204-22-76.compute-1.amazonaws.com:5432/daiq81k4e1kr0n'))
else:
    DATABASE = SqliteDatabase('recipes.sqlite')

class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()

    class Meta:
        database = DATABASE

class Recipe(Model):
    name = CharField()
    poster = ForeignKeyField(User, backref='recipes')
    origin = CharField()
    ingredients = TextField()
    instructions = TextField()
    image = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()

    DATABASE.create_tables([Recipe, User], safe=True)
    print("Connected to database and created tables")

    DATABASE.close()
