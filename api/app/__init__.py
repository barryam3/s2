import time

from flask import Flask, g, request, send_from_directory

from app.extensions import lm, bcrypt, mysql
from app.utils import res

from app.routes.auth import auth
from app.routes.songs import songs
from app.routes.users import users

def create_app(config):
    """Returns an initialized Flask application."""
    app = Flask(__name__, static_folder='public')
    
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    @app.before_request
    def before_request():
        """Prepare some things before the application handles a request."""
        g.request_start_time = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)

    # serve static files (for testing only)
    @app.route('/<path:path>')
    def send_js(path):
        return send_from_directory(app.static_folder, path)

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    lm.init_app(app)
    bcrypt.init_app(app)
    mysql.init_app(app)


def register_blueprints(app):
    """Register blueprints with the Flask application."""
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(songs, url_prefix="/songs")
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(users, url_prefix="/test")
