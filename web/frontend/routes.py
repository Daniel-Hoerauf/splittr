from . import app
from flask import request

@app.route('/hello/')
def hello():
    return 'World!'
