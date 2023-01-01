from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User
from forms import login_form,register_form

import requests, json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()
dataset=[]


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


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


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        name="Login",
        btn_action="Login"
        )

# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data
            
            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

with open("./busStopDataset.json", "r") as file:
        dataset=json.load(file)
app.run()