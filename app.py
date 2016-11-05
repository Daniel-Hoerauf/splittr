from werkzeug.wsgi import DispatcherMiddleware
from web.api import app as api
from flask import Flask, render_template


app = Flask(__name__)

from app import app

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    # API
    '/api/v0': api,
})


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run('localhost', 8000)

