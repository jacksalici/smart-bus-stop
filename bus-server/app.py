from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request
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

from creator import create_app,db,login_manager,bcrypt,mqttClient
from models import User, Bus, Stop
from forms import login_form,register_form

import requests, json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app = create_app()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


def getBusRoutes(stop_id):
    
    with requests.get(f"https://opendata.comune.bologna.it/api/v2/catalog/datasets/tper-vigente-mattina/records?limit=100&offset=0&refine=stop_id%3A{stop_id}&timezone=Europe%2FBerlin") as res:
        if (res.status_code == 200):
            routes = [elem["record"]["fields"] for elem in res.json()["records"] ]
            return routes



@app.route("/")
def home():
    dataset=[]
    stops = Stop.query.all()
    for stop in stops:
        dataset.append({"id": stop.id, 
                        "name": stop.name, 
                        "location": json.loads(stop.position),
                        "people": stop.people if stop.people != None else "-", 
                        "hButton": stop.hButton, })
    
    return render_template('index.html', stations=dataset, name = "Bus Stops Map")

@app.route("/bus-admin")
def admin():
    datasetBus=[]
    buses = Bus.query.all()
    
    for bus in buses:
        stop = Stop.query.filter_by(id = bus.stop_id).first()
        datasetBus.append({
            "id": bus.id,
            "loc": bus.position,
            "seats":int(bus.seatsCount),
            "next": stop.id,
            "hButton": stop.hButton,
            "people": int(stop.people) if stop.people != None else 0, 
            "max": 50
        })

   
    return render_template('back.html', data=datasetBus, name = "Admin")



@app.route("/<station>", methods=("GET", "POST"), strict_slashes=False)
def page(station):
    dataset=[]
    stop = Stop.query.filter(Stop.id == station).first()
    dataset.append({"id": stop.id, 
                    "name": stop.name, 
                    "location": json.loads(stop.position), 
                    "people": stop.people if stop.people != None else "-", 
                    "hButton": stop.hButton, })
    

    bus = Bus.query.filter_by(stop_id=str(station)).first()
    if bus:
        busDict = {"id": bus.id, "location": json.loads(bus.position), "counter": str(bus.seatsCount)}
    else:
        busDict = {"id": "", "location": "", "counter": "0"}
        
    
        
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(id=form.id.data).first()
            if check_password_hash(user.ukey, form.key.data):
                login_user(user)
                return redirect(url_for('page', station))
            else:
                flash("Invalid id or key!", "danger")
        except Exception as e:
            flash(e, "danger")

    nametext = "\""+ dataset[0]["name"] + "\"" if dataset[0]["name"] != "" else ""
    return render_template('station.html', 
        routes = getBusRoutes(station), 
        stations=dataset, 
        name="FERMATA "+ nametext + " #"+station, 
        bus=busDict, 
        form=form,
        text="Login",
        btn_action="Login")


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(id=form.id.data).first()
            if check_password_hash(user.ukey, form.key.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Invalid id or key!", "danger")
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
            id = form.id.data
            key = form.key.data
            name = form.name.data
            
            newuser = User(
                id=id,
                name=name,
                ukey=bcrypt.generate_password_hash(key),
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
    return redirect(request.referrer)








if __name__ == '__main__':
    #with open("./busStopDataset.json", "r") as file:
    #       dataset=json.load(file)
    
    app.run()
