from flask.app import Flask
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, IntegerField, PasswordField, TextAreaField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Email, Length
from datetime import date, timedelta
from flask import session
from wtforms.csrf.session import SessionCSRF
from models import *

class BaseForm(FlaskForm):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'zyxwv98765'
        csrf_time_limit = timedelta(minutes=30)

class SignUpForm(BaseForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    email = StringField("Email", validators=[DataRequired()])

class LoginForm(BaseForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])

class NewPasswordForm(BaseForm):
    old_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=8)])

class ProfileEditForm(BaseForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    bio = TextAreaField("Biography")
    profile_image = StringField("Profile Image URL")

class ReviewForm(BaseForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])

class RatingForm(BaseForm):
    score_choices = [
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
        (9,'9'),
        (10,'10')
    ]
    score = SelectField("Score", choices=score_choices)

