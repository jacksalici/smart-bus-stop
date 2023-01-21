from flask import Flask, render_template, jsonify, Blueprint
from configparser import ConfigParser
import requests
import json

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restplus import Api


from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from mqtt import MqttClient


try: 
    from flask_restplus import Api, Resource
except ImportError:
    import werkzeug, flask.scaffold
    werkzeug.cached_property = werkzeug.utils.cached_property
    flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
    from flask_restplus import Api, Resource

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"



db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mqttClient = MqttClient()
api = Api(default="Smart Bus Api", default_label="Get info about the enhanced public transport system.")

def create_app():   
    app = Flask(__name__)

    blueprint = Blueprint('api', __name__, url_prefix='/api')

    
    with open("./config.ini", "r") as file:
        config = ConfigParser()
        config.read_file(file)
        flask_config = dict(config.items("flask"))
        for cfg_key in flask_config:
            app.config[cfg_key.upper()] = flask_config[cfg_key]
    

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    mqttClient.client.loop_start()

    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    return app
