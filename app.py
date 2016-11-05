from werkzeug.wsgi import DispatcherMiddleware
from web.frontend import app as frontend
from web.api import app as api
from flask import Flask

app = Flask(__name__)

# API endpoint for a health check
@app.route('/health/')
def healthcheck():
    return 'Healthy', 200

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    # Frontend
    '': frontend,
    # API
    '/api/v0': api,
})

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run('localhost', 8000)
