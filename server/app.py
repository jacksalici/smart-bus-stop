from flask import Flask, render_template, request, jsonify
from configparser import ConfigParser
import json

app = Flask(__name__)
dataset=[]


@app.route("/")
def home():
    return render_template('index.html', stations=dataset, name = "Bus Stops Map")

@app.route("/<station>")
def page(station):
    nametext = "\""+ dataset[int(station)]["name"] + "\"" if dataset[int(station)]["name"] != "" else ""
    return render_template('index.html', stations=[dataset[int(station)]], name="Bus Stop "+ nametext + " #"+station)



if __name__ == '__main__':
   
    
    
    with open("./busStopDataset.json", "r") as file:
        dataset=json.load(file)

    with open("./config.ini", "r") as file:
        config = ConfigParser()
        config.read_file(file)
        flask_config = dict(config.items("Flask"))
        for cfg_key in flask_config:
            app.config[cfg_key.upper()] = flask_config[cfg_key]

    app.run()
