from . import app
from flask import request

@app.route('/test/')
def hello():
    return 'Hello'
