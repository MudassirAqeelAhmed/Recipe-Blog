from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from models import Recipe

recipe_ns = Namespace("recipe", description='A namespace for recipes')

recipe_model = recipe_ns.model(
    'Recipe', {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String()
    }
)



@recipe_ns.route('/recipes')
class RecipesResource(Resource):

    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes"""
        recipes = Recipe.query.all()
        return recipes
    
    @jwt_required()
    @recipe_ns.expect(recipe_model)
    @recipe_ns.marshal_with(recipe_model)
    def post(self):
        """Create a recipe"""
        data = request.get_json()

        new_recipe = Recipe(title=data['title'], description=data['description'])
        new_recipe.save()
        return new_recipe, 201

@recipe_ns.route('/recipe/<int:id>')
class RecipeResource(Resource):

    @recipe_ns.marshal_with(recipe_model)
    def get(self, id):
        """Get a recipe by id"""
        recipe = Recipe.query.get_or_404(id)
        return recipe
    
    @jwt_required()
    @recipe_ns.expect(recipe_model)
    @recipe_ns.marshal_with(recipe_model)
    def put(self, id):
        """Update a recipe by id"""
        recipe_to_update =Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe_to_update.update(data['title'],data['description'])
        return recipe_to_update

    @jwt_required()
    @recipe_ns.marshal_with(recipe_model)
    def delete(self, id):
        """Delete a recipe by id"""
        recipe_to_delete =Recipe.query.get_or_404(id)
        recipe_to_delete.delete()
        return recipe_to_delete
