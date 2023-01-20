
from creator import db
from flask_login import UserMixin

class Booking(db.Model):
    __tablename__ = "bookings"
    stopid = db.Column(db.String(10), db.ForeignKey('stops.id'), primary_key=True)
    busid = db.Column(db.String(10), primary_key=True)
    userid = db.Column(db.String(10), db.ForeignKey('users.id'), primary_key=True)
    time = db.Column(db.Integer(), primary_key=True)


    

     

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    ukey = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id
    
    
class Stop(db.Model):
    __tablename__ = "stops"
    
    id = db.Column(db.String(10), primary_key=True)
    position = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(50), nullable=True)
    people = db.Column(db.Integer(), nullable=True)
    hButton = db.Column(db.Integer(), nullable=True)



    def __repr__(self):
        return '<Stop %r>' % self.id
    
    
class Bus(db.Model):
    __tablename__ = "buses"
    
    id = db.Column(db.String(10), primary_key=True)
    position = db.Column(db.String(80), unique=False, nullable=False)
    stop_id = db.Column(db.String(50), nullable=True)
    seatsCount = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        return '<Bus %r>' % self.id
    
    
