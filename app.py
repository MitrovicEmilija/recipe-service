import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from ariadne import QueryType, graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL

app = Flask(__name__)
CORS(app, origins=["http://localhost:3006"], supports_credentials=True)

API_KEY = "zP+P7AySdHgg0dHEPf105g==OUOeAMxcNSOR0CIn"

# Define type definitions
type_defs = """
    type Recipe {
        title: String!
        ingredients: String!
        instructions: String!
    }

    type Query {
        topRecipes(query: String!): [Recipe!]!
    }
"""

# Define resolver
query = QueryType()

@query.field("topRecipes")
def resolve_top_recipes(_, info, query):
    url = f"https://api.api-ninjas.com/v1/recipe?query={query}"
    response = requests.get(url, headers={"X-Api-Key": API_KEY})
    data = response.json()
    return [
        {
            "title": item.get("title", "Untitled"),
            "ingredients": item.get("ingredients", ""),
            "instructions": item.get("instructions", "")
        } for item in data[:3]
    ]

# Setup schema
schema = make_executable_schema(type_defs, query)

# Playground UI
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return ExplorerGraphiQL().html(None), 200

# GraphQL POST endpoint
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    return jsonify(result)

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
