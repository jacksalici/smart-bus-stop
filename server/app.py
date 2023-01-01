from flask import Flask, render_template, jsonify
from configparser import ConfigParser
import requests
import json

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():   
    app = Flask(__name__)

    app.secret_key = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    """
    with open("./config.ini", "r") as file:
        config = ConfigParser()
        config.read_file(file)
        flask_config = dict(config.items("flask"))
        for cfg_key in flask_config:
            app.config[cfg_key.upper()] = flask_config[cfg_key]
    """

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)


    return app
