from peewee import *
import datetime

DATABASE = SqliteDatabase('recipes.sqlite')

class Recipe(Model):
    name = CharField()
    poster = CharField() #temp
    origin = CharField()
    ingredients = TextField()
    instructions = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()

    DATABASE.create_tables([Recipe], safe=True)
    print("Connected to database and created tables")

    DATABASE.close() 
