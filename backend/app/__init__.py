"""Initializes a Flask app for the web service."""

import time
from flask import Flask, g, request, send_from_directory

from app.extensions import LM, BCRYPT, MYSQL
from app.utils import res
from app.routes.auth import AUTH
from app.routes.songs import SONGS
from app.routes.users import USERS

def create_app(config):
    """Returns an initialized Flask application."""
    app = Flask(__name__, static_folder='public')

    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    @app.before_request
    def _before_request():
        """Prepare some things before the application handles a request."""
        g.request_start_time = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)

    # serve static files (for testing only)
    @app.route('/<path:path>')
    def _send_static_files(path):
        return send_from_directory(app.static_folder, path)

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    LM.init_app(app)
    BCRYPT.init_app(app)
    MYSQL.init_app(app)


def register_blueprints(app):
    """Register blueprints with the Flask application."""
    app.register_blueprint(AUTH, url_prefix="/auth")
    app.register_blueprint(SONGS, url_prefix="/songs")
    app.register_blueprint(USERS, url_prefix="/users")
