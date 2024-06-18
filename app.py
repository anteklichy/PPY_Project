from flask import Flask, jsonify, request, render_template
import http.client
import json

app = Flask(__name__)

API_HOST = "all-in-one-recipe-api.p.rapidapi.com"
API_KEY = "4d7b74dd71msh2bd81859d05f84ap194666jsn47b043c41ccb"

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}


def get_api_response(endpoint):
    conn = http.client.HTTPSConnection(API_HOST)
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data.decode("utf-8")


def post_api_response(endpoint, payload):
    conn = http.client.HTTPSConnection(API_HOST)
    headers['Content-Type'] = "application/json"
    conn.request("POST", endpoint, payload, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return data.decode("utf-8")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cuisines', methods=['GET'])
def get_cuisines():
    response = get_api_response("/cuisines")
    return render_template('cuisines.html', data=response)


@app.route('/cuisines/<cuisine>', methods=['GET'])
def get_recipes_by_cuisine(cuisine):
    response = get_api_response(f"/cuisines/{cuisine}")
    return render_template('recipes_by_cuisine.html', data=response)


@app.route('/categories', methods=['GET'])
def get_categories():
    response = get_api_response("/categories")
    return render_template('categories.html', data=response)


@app.route('/categories/<category>', methods=['GET'])
def get_recipes_by_category(category):
    response = get_api_response(f"/categories/{category}")
    return render_template('recipes_by_category.html', data=response)


@app.route('/recipe/<recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):
    response = get_api_response(f"/details/{recipe_id}")
    return render_template('recipe_details.html', data=response)


@app.route('/search/<phrase>', methods=['GET'])
def search_recipes(phrase):
    response = get_api_response(f"/search/{phrase}")
    return render_template('search.html', data=response)


@app.route('/recommendations/<recipe_id>', methods=['GET'])
def get_recommendations(recipe_id):
    response = get_api_response(f"/recommendations/{recipe_id}")
    return render_template('recommendations.html', data=response)


@app.route('/random', methods=['GET'])
def get_random_recipe():
    response = get_api_response("/random")
    return render_template('recipe_details.html', data=response)


@app.route('/search_ingredients', methods=['GET', 'POST'])
def search_by_ingredients():
    if request.method == 'POST':
        ingredients = request.form['ingredients']
        payload = json.dumps({"ingredients": ingredients})
        response = post_api_response("/search", payload)
        return render_template('search_ingredients.html', data=response)
    return render_template('search_ingredients.html')


@app.route('/generate_meal_plan', methods=['GET', 'POST'])
def generate_meal_plan():
    if request.method == 'POST':
        preference = request.form['preference']
        payload = json.dumps({"preference": preference})
        response = post_api_response("/generate/meal_plan", payload)
        return render_template('meal_plan.html', data=response)
    return render_template('meal_plan.html')


@app.route('/create_shopping_list', methods=['GET', 'POST'])
def create_shopping_list():
    if request.method == 'POST':
        recipe_id = request.form['recipe_id']
        payload = json.dumps({"id": recipe_id})
        response = post_api_response("/generate/shopping_list", payload)
        return render_template('shopping_list.html', data=response)
    return render_template('shopping_list.html')


@app.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    text = request.form['text']
    payload = json.dumps({"text": text})
    conn = http.client.HTTPSConnection("whin2.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "whin2.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    conn.request("POST", "/send", payload, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return jsonify(data.decode("utf-8"))


if __name__ == '__main__':
    app.run(debug=True)
