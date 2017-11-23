import os
# athena uses MySQLdb but I couldn't get it working locally
mysqlconnector = False
try:
    import MySQLdb
except ImportError:
    mysqlconnector = True


class base_config(object):
    """Default configuration options."""
    SITE_NAME = 's2'

    SECRET_KEY = os.environ.get('SECRET_KEY', 'secrets')

    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASS = os.environ.get('MYSQL_PASS', 'password')
    MYSQL_DB = os.environ.get('MYSQL_DB', 's2')

    SQLALCHEMY_DATABASE_URI = 'mysql%s://%s:%s@%s/%s' % (
        '+mysqlconnector' if mysqlconnector else '',
        MYSQL_USER,
        MYSQL_PASS,
        MYSQL_HOST,
        MYSQL_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
