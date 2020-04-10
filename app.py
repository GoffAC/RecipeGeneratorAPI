import json
import flask
from flask import request, jsonify, make_response
from pprint import pprint
import functools
from functools import wraps

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# A route for browsers to see
@app.route('/', methods=['GET'])
def home():
    return "<h1>Food Suggestions</h1><p> If you give this endpoint a list of items it, hopefully, will give you a " \
           "meal suggestion</p> "


# A route to return all of the available recipes in our catalog.
@app.route('/api/v1/recipes/all', methods=['GET'])
def api_all():
    # Load data from external json
    with open('recipes.json', 'r') as f:
        recipes = json.load(f)

    results = []
    for recipes in recipes["recipes"]:
        results.append(recipes["name"])

    return jsonify(results)


# A route to return meals when given ingredients
@app.route('/api/v1/suggestRecipes', methods=['POST'])
def api_suggest_recipes():
    # Get data from POST
    data = request.get_json() or {}
    if 'ingredients' not in data:
        return EnvironmentError

    # Get data from components json
    with open('./components.json') as f:
        components = json.load(f)

    results_components = []
    for ingredient in data["ingredients"]:
        # Search the components to get all possible components from your input
        for component in components["components"]:
            for componentIngredient in component["ingredients"]:
                if componentIngredient == ingredient:
                    results_components.append(component["name"])

    with open('./recipes.json') as f:
        recipes = json.load(f)

    # Intersection function from https://www.geeksforgeeks.org/python-intersection-two-lists/
    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    results_meals = []
    # For each recipe check that all components are filled. Ie, Steak and chips
    for recipe in recipes["recipes"]:

        # Store the recipes' components
        components_required = recipe["components"]

        # Count the number of components needed in the recipe to compare later
        components_required_count = len(components_required)

        # Find if the components_needed intersect (&) hence are contained in the available results_components
        components_crossover = intersection(components_required, results_components)

        # Save all available meals to return to user
        if components_required_count == len(components_crossover):
            results_meals.append(recipe["name"])

    return jsonify(results_meals)


app.run()
