from flask import Flask
from configparser import ConfigParser
from flask import render_template, request, jsonify

app = Flask(__name__)

with open("./config.ini", "r") as file:
        config = ConfigParser()
        config.read_file(file)
        app.config.from_object(config)

@app.route('/')
def page():
    return render_template('index.html')



if __name__ == '__main__':
        app.run()