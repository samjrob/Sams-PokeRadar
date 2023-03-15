from flask import Flask, render_template, request

from functions import poke_with_ability, poke_with_type, Pokemon_Info, get_pokemon_info, poke_with_move, \
    poke_in_generation, poke_forms

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pokecard", methods=['GET', 'POST'])
def pokecard():
    if request.method == 'POST':
        query = request.form["pokemon"].strip().replace(" ", "-").lower()
        form_dict = poke_forms()
        if query in form_dict:
            return render_template("results.html", search=query, poke_list=form_dict[query], form_message=True)
        else:
            if query.__contains__("-base-form"):
                query = query[0:query.find("-")]
            pokemon = Pokemon_Info(get_pokemon_info(query))
            return render_template("pokecard.html", pokemon=pokemon, query=query, form_dict=form_dict)
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
        return render_template("results.html", search=search, poke_list=poke_list, form_message=False)
    else:
        return "Error: was expecting a POST request", 400
