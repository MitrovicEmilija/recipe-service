import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3006"], supports_credentials=True)

API_KEY = "zP+P7AySdHgg0dHEPf105g==OUOeAMxcNSOR0CIn"

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
