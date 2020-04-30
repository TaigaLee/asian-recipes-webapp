import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict

recipes = Blueprint('recipes', 'recipes')

@recipes.route('/', methods=['GET'])
def recipes_index():
    result = models.Recipe.select().dicts()
    recipes = [recipe for recipe in result]

    recipesLength = len(recipes)

    print(recipes)

    return jsonify(
      data = recipes,
      message ="Successfully found {}".format(recipesLength),
      status = 200
    ), 200


@recipes.route('/', methods=['POST'])
def create_recipe():
    payload = request.get_json()

    new_recipe = models.Recipe.create(
        name=payload['name'],
        poster=payload['poster'],
        origin=payload['origin'],
        ingredients=payload['ingredients'],
        instructions=payload['instructions'],
    )

    recipe_dict = model_to_dict(new_recipe)

    print(recipe_dict)

    return jsonify(
        data=recipe_dict,
        message="Successfully created recipe!",
        status=201
    ), 201
