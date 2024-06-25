from flask import Flask, request, render_template
import http.client
import json

app = Flask(__name__)

API_HOST = "all-in-one-recipe-api.p.rapidapi.com"
API_KEY = "4d7b74dd71msh2bd81859d05f84ap194666jsn47b043c41ccb"

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}


def def_res(conn):
    res = conn.getresponse()
    if res.status == 404 | res.status == 500:
        raise Exception()
    return res.read()


def get_api_response(endpoint):
    conn = http.client.HTTPSConnection(API_HOST)
    conn.request("GET", endpoint, headers=headers)
    data = def_res(conn)
    conn.close()
    return json.loads(data.decode("utf-8"))


def post_api_response(endpoint, payload):
    conn = http.client.HTTPSConnection(API_HOST)
    headers['Content-Type'] = "application/json"
    conn.request("POST", endpoint, payload, headers)
    data = def_res(conn)
    conn.close()
    return json.loads(data.decode("utf-8"))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cuisines', methods=['GET'])
def get_cuisines():
    try:
        api_response = get_api_response("/cuisines")
        cuisines = api_response['cuisines']['data']
        return render_template('cuisines.html', cuisines=cuisines)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        api_response = get_api_response("/categories")
        categories = api_response['categories']['data']
        return render_template('categories.html', categories=categories)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/random', methods=['GET'])
def get_random_recipe():
    try:
        response = get_api_response("/random")
        recipe = response['recipe']
        return render_template('base_recipe.html', data=recipe['data'], id=recipe['id'])
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/search/cuisines', methods=['GET'])
def search_recipes_by_cuisine():
    cuisine = request.args.get('cuisine')
    try:
        response = get_api_response(f"/cuisines/{cuisine}")
        recipes = response['cuisines']['data']
        return render_template('search.html', data=recipes)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/search/categories', methods=['GET'])
def get_recipes_by_category():
    category = request.args.get('category')
    try:
        response = get_api_response(f"/categories/{category}")
        recipes = response['categories']['data']
        return render_template('search.html', data=recipes)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/recipe', methods=['GET'])
def get_recipe_details():
    recipe_id = request.args.get('recipe_id')
    try:
        response = get_api_response(f"/details/{recipe_id}")
        recipe = response['recipe']
        return render_template('base_recipe.html', data=recipe['data'], id=recipe['id'])
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    recipe_id = request.args.get('recipe_id')
    try:
        response = get_api_response(f"/recommendations/{recipe_id}")
        recommendations = response['recommendations']
        return render_template('recommendations.html', data=recommendations['data'], targetID=recommendations['targetID'])
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/phrase', methods=['GET'])
def search_recipes():
    phrase = request.args.get('phrase')
    try:
        response = get_api_response(f"/search/{phrase}")
        recipes = response['recipes']
        return render_template('search.html', data=recipes['data'])
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/search_ingredients', methods=['POST'])
def search_by_ingredients():
    ingredients = request.form['ingredients']
    payload = json.dumps({"ingredients": ingredients})
    try:
        response = post_api_response("/search", payload)
        recipes = response['recipe']['data']
        return render_template('search.html', data=recipes)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/generate_meal_plan', methods=['POST'])
def generate_meal_plan():
    preference = request.form['preference']
    payload = json.dumps({"preference": preference})
    try:
        response = post_api_response("/generate/meal_plan", payload)
        meal_plan = response['recipe']['data']
        return render_template('meal_plan.html', data=meal_plan)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/create_shopping_list', methods=['GET', 'POST'])
def create_shopping_list():
    if request.method == 'POST':
        recipe_id = request.form['recipe_id']
        payload = json.dumps({"id": recipe_id})
        try:
            response = post_api_response("/generate/shopping_list", payload)
            shopping_list = response['lists']['data']
            return render_template('shopping_list.html', data=shopping_list)
        except Exception as e:
            return render_template('error.html', message=str(e))
    return render_template('shopping_list.html')


#try jest tylko w tej metodzie, bo send_whatsapp_form i send_whatsapp mogą być otworzone tylko za pomocą tej metody
@app.route('/whatsapp_instructions', methods=['GET'])
def whatsapp_instructions():
    message_type = request.args.get('message_type')
    message_content = request.args.get('message_content')
    try:
        return render_template('whatsapp_instructions.html', message_type=message_type, message_content=message_content)
    except Exception as e:
        return render_template('error.html', message=str(e))


@app.route('/send_whatsapp_form', methods=['GET'])
def send_whatsapp_form():
    message_type = request.args.get('message_type')
    message_content = request.args.get('message_content')
    return render_template('whatsapp_send.html', message_content=message_content, message_type=message_type)


@app.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    text = request.form['text']
    payload = json.dumps({"text": text})
    conn = http.client.HTTPSConnection("whin2.p.rapidapi.com")
    header = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "whin2.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    conn.request("POST", "/send", payload, header)
    conn.close()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
