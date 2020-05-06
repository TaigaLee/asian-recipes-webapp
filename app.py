import os
from flask import Flask, g
from flask_login import LoginManager
from flask_cors import CORS

import models

from resources.recipes import recipes
from resources.users import users

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = "THIS IS MY TOP SECRET SESSION KEY. oirhjowi3ehqypv40o"

login_manager = LoginManager()

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  try:
    return models.User.get_by_id(user_id)
  except models.DoesNotExist:
    return None


@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(
    data={
    "error": "Not logged in"
    },
    message = "You must be logged in!",
    status = 401
  ), 401

CORS(recipes, origins=['https://miso-happy-react.herokuapp.com'], supports_credentials=True)
CORS(users, origins=['https://miso-happy-react.herokuapp.com'], supports_credentials=True)
CORS(recipes, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(recipes, url_prefix='/api/v1/recipes')
app.register_blueprint(users, url_prefix='/api/v1/users')

@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()


@app.after_request
def after_request(response):
  print("you should see this after each request")
  g.db.close()
  return response

if 'ON_HEROKU' in os.environ:
  print('non heroku!')
  models.initialize()

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)
