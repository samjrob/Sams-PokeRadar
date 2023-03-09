import functions

from flask import Flask, render_template, request

from functions import poke_with_ability, poke_with_type, Pokemon_Info, get_pokemon_info
# Create an instance of Flask
app = Flask(__name__)


# Create a view function for /
@app.route("/")
def index():
    return render_template("index.html")


# Create a view function for /results
@app.route("/pokecard", methods=['GET', 'POST'])
def pokecard():
    if request.method == 'POST':
        pokemon = Pokemon_Info(get_pokemon_info(request.form["pokemon"]))
        return render_template("pokecard.html", pokemon=pokemon)
    else:
        return "Error: was expecting a POST request", 400


@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        try:
            query = request.form["type"]
            poke_list = poke_with_type(query)
        except KeyError:
            query = request.form["ability"]
            poke_list = poke_with_ability(query)
        return render_template("results.html", query=query, poke_list=poke_list)
    else:
        return "Error: was expecting a POST request", 400
