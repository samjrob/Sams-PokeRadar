from flask import Flask, render_template, request

from functions import poke_with_ability, poke_with_type, Pokemon_Info, get_pokemon_info, poke_with_move, poke_in_generation

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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
        query = list(request.form.keys())[0]
        if query == "type":
            search = query + ": " + request.form["type"]
            poke_list = poke_with_type(request.form["type"])
        elif query == "ability":
            search = query + ": " + request.form["ability"]
            poke_list = poke_with_ability(request.form["ability"])
        elif query == "move":
            search = query + ": " + request.form["move"]
            poke_list = poke_with_move(request.form["move"])
        elif query == "gen":
            search = query + ": " + request.form["gen"]
            poke_list = poke_in_generation(request.form["gen"])
        return render_template("results.html", search=search, poke_list=poke_list)
    else:
        return "Error: was expecting a POST request", 400
