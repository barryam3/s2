"""Flask extensions"""

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
lm = LoginManager()
db = SQLAlchemy()
