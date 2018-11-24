from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


bcrypt = Bcrypt()
lm = LoginManager()
mysql = MySQL(cursorclass=DictCursor)
