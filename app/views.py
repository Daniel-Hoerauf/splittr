from flask import render_template, redirect, jsonify
from app import app
from .forms import LoginForm, SignUpForm, GroupForm
from .database import register_user, login_user, check_username_avail, search_user
from Crypto.Hash import SHA256

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

@app.route('/find_user/', methods=['GET'])
@app.route('/find_user/<user_snippet>/', methods=['GET'])
def find_user(user_snippet=''):
    users = search_user(user_snippet)
    return jsonify(users)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if(not check_username_avail(form.username.data)):
            return render_template('signup.html',
                                   title='Sign Up',
                                   form=form,
                                   taken=True)
        # Hash password before storing it in database.
        pwHash = SHA256.new(form.password.data.encode()).hexdigest()
        user_id = register_user(form.username.data,
                                pwHash, form.email.data)
        response = redirect('/')
        response.set_cookie('SplittrUserId', user_id)
        return response
    return render_template('signup.html',
                           title='Sign Up',
                           form=form, taken=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Hash password before calling database
        pwHash = SHA256.new(form.password.data.encode()).hexdigest()
        user_id = login_user(form.username.data, pwHash)
        if user_id:
            response = redirect('/')
            response.set_cookie('SplittrUserId', user_id)
            return response
        else:
            # Go back to back with message of incorrect username or
            # password
            return render_template('login.html',
                                   title='Log In',
                                   form=form,
                                   incorrect_pw_or_user=True)

    return render_template('login.html',
                           title='Login',
                           form=form, incorrect_pw_or_user=False)

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/')
def home():
    groups = ["Naked & Afraid", "Frat stars", "bitches", "schmoes", "Rachel"]
    username = "Kevin Kozlowski"
    return render_template('home.html',
                           groups=groups,
                           username=username)

@app.route('/group')
def group():
    members = [{'name': "bob jones", 'money': 70},
               {'name': "malcolm", 'money': 80},
               {'name': "diana", 'money': -3},
               {'name': "stanley payne", 'money': 666}]
    groupname = "Twelve"
    return render_template('group.html',
                           members=members,
                           groupname=groupname)

@app.route('/creategroup', methods=['GET', 'POST'])
def creategroup():
    form = GroupForm()
    if form.validate_on_submit():
        return redirect('/index')
    return render_template('creategroup.html',
                           title='Create Group',
                           form=form)
