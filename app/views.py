from flask import render_template, redirect
from app import app
from .forms import LoginForm
from .forms import SignUpForm
from .database import register_user, login_user
from .forms import GroupForm

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
        # TODO: Check if username is available before registering user
        # TODO: Hash password before storing it in database
        user_id = register_user(form.username.data,
                                form.password.data, form.email.data)
        response = redirect('/')
        response.set_cookie('SplittrUserId', user_id)
        return response
    return render_template('signup.html',
                           title='Sign Up',
                           form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO: Hash password before calling database
        user_id = login_user(form.username.data, form.password.data)
        if user_id:
            response = redirect('/')
            response.set_cookie('SplittrUserId', user_id)
            return response
        else:
            # TODO: Go back to back with message of incorrect username or
            # password
            pass

    return render_template('login.html',
                           title='Login',
                           form=form)

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/')
def home():
    groups = ["Naked & Afraid", "Frat stars", "bitches", "schmoes","Rachel"]
    username = "Kevin Kozlowski"
    return render_template('home.html',
                            groups=groups,
                            username=username)

@app.route('/group')
def group():
    members = [{'name': "bob jones", 'money': 70},
              {'name': "malcolm", 'money': 80},
              {'name': "diana", 'money': -3},
              {'name': "stanley payne",'money': 666}]
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
