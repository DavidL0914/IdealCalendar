from flask import Flask, render_template, request
import requests

app = Flask(__name__)

search_api_url = "https://api.spoonacular.com/recipes/complexSearch"
info_api_url = "https://api.spoonacular.com/recipes/{id}/information"
api_key = "bda6dcbd9ea9479995b632addb9f3761"
info_params = {"apiKey": api_key}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        search_params = {"apiKey": api_key, "query": query}
        search_response = requests.get(search_api_url, params=search_params)

        if search_response.status_code == 200:
            search_data = search_response.json()
            recipe_ids = [recipe['id'] for recipe in search_data.get("results", [])]

            recipes = []
            for recipe_id in recipe_ids:
                info_response = requests.get(info_api_url.format(id=recipe_id), params=info_params)
                if info_response.status_code == 200:
                    info_data = info_response.json()
                    recipes.append({
                        "title": info_data['title'],
                        "image": info_data['image'],
                        "summary": info_data['summary']
                    })
                else:
                    print(f"Error fetching details for recipe ID {recipe_id}: {info_response.status_code}")

            return render_template('index.html', query=query, recipes=recipes)
        else:
            return f"Error: {search_response.status_code}"

    return render_template('index.html', query=query, recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
