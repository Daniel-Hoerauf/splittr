from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired

class SignUpForm(Form):
    remember_me = BooleanField('remember_me', default=False)
    username = StringField('Username', [validators.Length(min=4, max= 25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
    	validators.DataRequired(),
    	validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    remember_me = BooleanField('remember_me', default=False)
    username = StringField('Username', [validators.Length(min=4, max= 25)])
    password = PasswordField('Password', [
    	validators.DataRequired(),
    ])