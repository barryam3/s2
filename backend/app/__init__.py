'''Initializes a Flask app for the web service.'''

from flask import Flask, g, send_from_directory

from app.extensions import bcrypt, lm, db

from app.routes.auth import auth
from app.routes.users import users
from app.routes.songs import songs
from app.routes.groups import groups

# models must be imported for create_all to work
from models.comment import Comment
from models.link import Link
from models.rating import Rating
from models.song import Song
from models.group import Group
from models.user import User


def create_app(config):
    '''Returns an initialized Flask application.'''

    app = Flask(__name__, static_folder='public')
    app.app_context().push()

    configure(app, config)
    top_level_routes(app)
    register_extensions(app)
    register_blueprints(app)

    return app


def configure(app, config):
    '''Configure the app.'''

    app.config.from_mapping(
        SITE_NAME='s2',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    app.config.from_object(config)
    assert app.config['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (
        app.config['MYSQL_USER'],
        app.config['MYSQL_PASSWORD'],
        app.config['MYSQL_HOST'],
        app.config['MYSQL_DB']
    )


def top_level_routes(app):
    '''Routes beginning with /'''
    @app.route('/<path:path>')
    def send_static_files(path):
        '''Serve a basic webapp for sending requests.'''
        return send_from_directory(app.static_folder, path)


def register_extensions(app):
    '''Register extensions with the Flask application.'''

    bcrypt.init_app(app)
    lm.init_app(app)
    db.init_app(app)


def register_blueprints(app):
    '''Register blueprints with the Flask application.'''

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(songs, url_prefix='/songs')
    app.register_blueprint(groups, url_prefix='/groups')


def initialize_database(app):
    '''Create tables if they don't exist and create an initial user if needed.'''

    db.create_all()
    if Group.query.count() == 0:
        initial_group = Group()
        db.session.add(initial_group)
    if User.query.count() == 0:
        initial_user = User('crossp', 'xprod05', admin=True)
        db.session.add(initial_user)
    db.session.commit()
