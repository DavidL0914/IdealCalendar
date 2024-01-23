import json, jwt
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests

# Change variable names and API details
spoonacular_api = Blueprint('spoonacular_api', __name__, url_prefix='/api/spoonacular')
api = Api(spoonacular_api)

class SpoonacularAPI:
    class RecipeSearch(Resource):
        def post(self):
            ''' Read data from the JSON body '''
            body = request.get_json()

            ''' Avoid garbage in, error checking '''
            # Extract dietary preferences from the request
            glutenfree = body.get('glutenfree', False)
            ketogenic = body.get('ketogenic', False)
            vegan = body.get('vegan', False)
            vegetarian = body.get('vegetarian', False)
            sustainable = body.get('sustainable', False)
            healthy = body.get('healthy', False)

            ''' #1: Key code block, setup parameters for Spoonacular API '''
            params = {
                'apiKey': 'bda6dcbd9ea9479995b632addb9f3761',
                'number': 1,  # Specify the number of recipes to retrieve
                'glutenFree': glutenfree,
                'ketogenic': ketogenic,
                'vegan': vegan,
                'vegetarian': vegetarian,
                'sustainable': sustainable,
                'healthy': healthy
            }

            spoonacular_endpoint = 'https://api.spoonacular.com/recipes/complexSearch'
            response = requests.get(spoonacular_endpoint, params=params)

            if response.status_code == 200:
                # Parse and return the Spoonacular response
                spoonacular_data = response.json()
                return jsonify(spoonacular_data)
            else:
                return {'error': 'Unable to fetch Spoonacular data'}

    # Building REST API endpoint
    api.add_resource(RecipeSearch, '/recipe_search')