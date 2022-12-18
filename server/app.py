from flask import Flask, render_template, request, jsonify
from configparser import ConfigParser
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html', stations=dataset)

@app.route("/<station>")
def page(station):
    return render_template('index.html', stations=[dataset[int(station)]])



if __name__ == '__main__':
        dataset=[]
        with open("./modenaBusStationDataset.json", "r") as file:
                dataset=json.load(file)

        app.run()
        with open("./config.ini", "r") as file:
                config = ConfigParser()
                config.read_file(file)
                app.config.from_object(config)