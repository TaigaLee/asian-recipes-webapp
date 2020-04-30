from flask import Flask
from flask_login import LoginManager

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
        data={},
        message = "You must be logged in to access that",
        status=401
    ), 401

app.register_blueprint(recipes, url_prefix='/api/v1/recipes')
app.register_blueprint(users, url_prefix='/api/v1/users')

@app.route('/')
def hello_world():
    return "Hello world!"

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
