from flask import Flask

import models

from resources.recipes import recipes
from resources.users import users

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.register_blueprint(recipes, url_prefix='/api/v1/recipes')
app.register_blueprint(users, url_prefix='/api/v1/users')

@app.route('/')
def hello_world():
    return "Hello world!"

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
