import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from graphene import ObjectType, String, List, Schema
from flask_graphql import GraphQLView

app = Flask(__name__)
CORS(app, origins=["http://localhost:3006"], supports_credentials=True)

API_KEY = "zP+P7AySdHgg0dHEPf105g==OUOeAMxcNSOR0CIn"

class RecipeType(ObjectType):
    title = String()
    ingredients = String()
    instructions = String()

class Query(ObjectType):
    top_recipes = List(RecipeType, query=String(default_value="salad"))

    @staticmethod
    def resolve_top_recipes(self, info, query):
        url = f"https://api.api-ninjas.com/v1/recipe?query={query}"
        response = requests.get(url, headers={"X-Api-Key": API_KEY})
        data = response.json()
        return [
            {
                "title": recipe.get("title", "Untitled"),
                "ingredients": recipe.get("ingredients", "N/A"),
                "instructions": recipe.get("instructions", "N/A")
            } for recipe in data[:3]
        ]

schema = Schema(query=Query)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

@app.route('/recipe', methods=['GET'])
def get_recipe():
    query = request.args.get('query', 'salad').strip()
    if not query:
        return jsonify({"error": "Query is required"}), 400

    api_url = f"https://api.api-ninjas.com/v1/recipe?query={query}"

    try:
        response = requests.get(api_url, headers={"X-Api-Key": API_KEY})

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch recipe"}), 500

        data = response.json()
        if not data:
            return jsonify([])

        recipes = []
        for item in data[:3]:
            recipes.append({
                "title": item.get("title", "Untitled Recipe"),
                "ingredients": item.get("ingredients", "No ingredients listed."),
                "instructions": item.get("instructions", "No instructions available.")
            })

        return jsonify(recipes)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
