
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    ukey = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id