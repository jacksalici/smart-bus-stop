from flask import Flask, render_template, jsonify
from configparser import ConfigParser
import requests
import json

app = Flask(__name__)
dataset=[]

def getBusRoutes(stop_id):
    with requests.get(f"https://opendata.comune.bologna.it/api/v2/catalog/datasets/tper-vigente-mattina/records?limit=100&offset=0&refine=stop_id%3A{stop_id}&timezone=Europe%2FBerlin") as res:
        if (res.status_code == 200):
            routes = [elem["record"]["fields"] for elem in res.json()["records"] ]
            print(routes)
            return routes



@app.route("/")
def home():
    return render_template('index.html', stations=dataset, name = "Bus Stops Map")

@app.route("/<station>")
def page(station):

    nametext = "\""+ dataset[station]["name"] + "\"" if dataset[station]["name"] != "" else ""
    return render_template('station.html', routes = getBusRoutes(station), stations={station: dataset[station]}, name="Bus Stop "+ nametext + " #"+station)



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
