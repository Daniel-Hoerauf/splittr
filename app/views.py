from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
from .forms import SignUpForm
from werkzeug.wsgi import DispatcherMiddleware
from web.api import app as api
from flask import Flask, render_template

# index view function suppressed for brevity
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)
    
# API endpoint for a health check
@app.route('/health/')
def healthcheck():
    return 'Healthy', 200

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('signup.html', 
                           title='Sign Up',
                           form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', 
                           title='Login',
                           form=form)

@app.route('/landing')
def landing():
    return render_template('landing.html')
