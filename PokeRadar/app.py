import functions

from flask import Flask, render_template, request

from functions import wikipedia_locationsearch
# Create an instance of Flask
app = Flask(__name__)


# Create a view function for /
@app.route("/")
def index():
    return render_template("index.html")


# Create a view function for /results
@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        place = request.form["place"]
        max_results = int(request.form["num_results"])
        radius = float(request.form["radius"])
        try:
            request.form["list_sorted"]
            sort = True
        except KeyError:
            sort = False
        wiki_list = wikipedia_locationsearch(place, max_results, radius, sort)
        return render_template("results.html", place=place, wiki_list=wiki_list)
    else:
        return "Error: was expecting a POST request", 400
