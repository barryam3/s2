"""MySQL Credentials."""

import os

# pylint: disable=R0903
class BaseConfig: # pylint: disable=R0205
    """Default configuration options.

    This has to be an object."""

    SITE_NAME = 's2'

    SECRET_KEY = os.environ.get('S2_SECRET', 'secrets')

    MYSQL_DATABASE_HOST = os.environ.get('S2_DB_HOST', 'localhost')
    MYSQL_DATABASE_USER = os.environ.get('S2_DB_USER', 'root')
    MYSQL_DATABASE_PASSWORD = os.environ.get('S2_DB_PASS', 'AcKgFHhihBhXCf2THfnQrwFx')
    MYSQL_DATABASE_DB = os.environ.get('S2_DB_NAME', 'barryam3+s2')