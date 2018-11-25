'''MySQL Credentials.'''

import os

class Config(object):
    SECRET_KEY = os.environ.get('S2_SECRET_KEY')
    MYSQL_HOST = os.environ.get('S2_HOST')
    MYSQL_USER = os.environ.get('S2_USER')
    MYSQL_PASSWORD = os.environ.get('S2_PASSWORD')
    MYSQL_DB = os.environ.get('S2_DB')
