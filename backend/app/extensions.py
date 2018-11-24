"""Flask extensions"""

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

BCRYPT = Bcrypt()
LM = LoginManager()
MYSQL = MySQL(cursorclass=DictCursor)
