import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash

from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint('users', 'users')

# @users.route('/', methods=['GET'])
# def test_user_resource():
#     return "IT WORKS!!!"

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()

    payload['username'] = payload['username'].lower()
    payload['email'] = payload['email'].lower()

    try:
        models.User.get(models.User.email == payload['email'])

        return jsonify(
            data={},
            message=f"A user with the email {payload['email']} already exists",
            status=401
        ), 401

    except models.DoesNotExist:
        pw_hash = generate_password_hash(payload['password'])

        created_user = models.User.create(
            username=payload['username'],
            email=payload['email'],
            password=pw_hash
        )

        login_user(created_user)

        created_user_dict = model_to_dict(created_user)

        created_user_dict.pop('password')

        return jsonify(
            data=created_user_dict,
            message="Sucessfully registered user",
            status=201
        ), 201

@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['username'] = payload['username'].lower()

    try:
        user = models.User.get(models.User.username == payload['username'])

        user_dict = model_to_dict(user)

        password_is_good = check_password_hash(user_dict['password'], payload['password'])

        if (password_is_good):
            login_user(user)
            user_dict.pop('password')

            return jsonify(
                data=user_dict,
                message="Successfully logged in {}".format(user_dict['username']),
                status=200
            ), 200

        else:
            return jsonify(
                data={},
                message="Email or password is incorrect",
                status=401
            ), 401

    except models.DoesNotExist:

        return jsonify(
            data={},
            message="Email or password is incorrect",
            status=401
        ), 401


@users.route('/<id>', methods=['PUT'])
@login_required
def update_user(id):
    payload = request.get_json()

    user_to_update = models.User.get_by_id(id)

    if user_to_update.id == current_user.id:
        if 'username' in payload:
            user_to_update.username = payload['username']
        if 'email' in payload:
            user_to_update.email = payload['email']
        if 'password' in payload:
            pw_hash = generate_password_hash(payload['password'])
            user_to_update.password = pw_hash

        user_to_update.save()

        updated_user_dict = model_to_dict(user_to_update)

        updated_user_dict.pop('password')

        return jsonify(
            data=updated_user_dict,
            message="Successfully updated user with id {}".format(id),
            status=200
        ), 200

    else:
        return jsonify(
            data={},
            message="You're not the account owner.",
            status=403
        ), 403

@users.route('/<id>', methods=['DELETE'])
@login_required
def delete_user(id):
    try:

        user_to_delete = models.User.get_by_id(id)

        user_recipes = current_user.recipes

        for recipe in user_recipes:
            recipe.delete_instance()

        if user_to_delete.id == current_user.id:
            user_to_delete.delete_instance()

            return jsonify(
                data={},
                message="Successfully deleted user with id {}".format(id),
                status=200
            ), 200



        else:

            return jsonify(
                data={},
                message="You're not the account owner",
                status=403
                ), 403

    except models.DoesNotExist:
        return jsonify(
            data={},
            message="There is no user with this id",
            status=404
        ), 404


@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        data={},
        message="Successfully logged out!",
        status=200
    ), 200
