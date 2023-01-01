from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
)

from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp ,Optional
import email_validator
from flask_login import current_user
from wtforms import ValidationError,validators
from models import User


class login_form(FlaskForm):
    id = StringField(validators=[InputRequired(), Length(1, 64)])
    key = PasswordField(validators=[InputRequired(), Length(1, 72)])
   


class register_form(FlaskForm):
    id = StringField(validators=[InputRequired(), Length(1, 64)])
    name = StringField(validators=[InputRequired(), Length(1, 64)])
    key = PasswordField(validators=[InputRequired(), Length(1,72)])
    