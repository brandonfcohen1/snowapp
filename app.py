from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    with open('leafletPrep.json', 'r') as file:
        tiles=json.loads(file.read())

    return render_template('leafletkmz.html', tiles = tiles)