from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    with open('latest_overlap/nsm_latest.json', 'r') as file:
        layers=json.loads(file.read())

    return render_template('leafletkmz.html', layers = layers)


@app.route("/leaflet")
def leaflet():
    return(render_template('leaflet.html'))