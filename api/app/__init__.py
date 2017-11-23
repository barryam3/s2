import time

from flask import Flask, g, request

from app.database import db
from app.extensions import lm, bcrypt
from app.utils import send_success_response
from app.routes.auth import auth


def create_app(config):
    """Returns an initialized Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    @app.before_request
    def before_request():
        """Prepare some things before the application handles a request."""
        g.request_start_time = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)

    @app.route('/', methods=['GET'])
    def index():
        """Basic test request handler."""
        return send_success_response("The API is working!")

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    db.init_app(app)
    lm.init_app(app)
    bcrypt.init_app(app)


def register_blueprints(app):
    """Register blueprints with the Flask application."""
    app.register_blueprint(auth, url_prefix="/auth")
