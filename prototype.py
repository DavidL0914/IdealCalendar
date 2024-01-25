import requests

search_api_url = "https://api.spoonacular.com/recipes/complexSearch"
info_api_url = "https://api.spoonacular.com/recipes/{id}/information"
api_key = "bda6dcbd9ea9479995b632addb9f3761"
search_params = {"apiKey": api_key,
                 "titleMatch": "noodles",
                 }
info_params = {"apiKey": api_key,}

search_response = requests.get(search_api_url, params=search_params)

if search_response.status_code == 200:
    search_data = search_response.json()
    recipe_ids = [recipe['id'] for recipe in search_data.get("results", [])]

    with open("recipes_details.html", "w", encoding="utf-8") as file:
        file.write("<html><body><h1>Recipes Details</h1><ul>")
        
        for recipe_id in recipe_ids:
            info_response = requests.get(info_api_url.format(id=recipe_id), params=info_params)
            if info_response.status_code == 200:
                info_data = info_response.json()

                file.write(f"<li><strong>{info_data['title']}</strong><br>")
                file.write(f"<img src='{info_data['image']}' alt='{info_data['title']}'><br>")
                file.write(f"Summary: {info_data['summary']}<br><br></li>")
            else:
                print(f"Error fetching details for recipe ID {recipe_id}: {info_response.status_code}")

        file.write("</ul></body></html>")

    print("Detailed information has been written to recipes_details.html.")
else:
    print(f"Error: {search_response.status_code}")
