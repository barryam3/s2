# s2 API
*A mostly RESTful web service.*

## Technical Overview
We're using Python because we want to host this on scripts.mit.edu which only supports PHP, Perl, and Python; Python is by far the most popular of the three at MIT. We're using Python 2 because it seems to have better support on the server. We're using a MySQL database because it's provided for free by MIT SIPB.

We are using Flask and SQLAlchemy.

## Prerequisite Knowledge
- Basic knowledge of Python
- Basic knowledge of SQL
- An understanding of web services
    - Routes
    - Methods
    - Status Codes
    - JSON Request & Response Bodies
    - URL & Query Params
    - REST

## Technical Prerequisites
- Python 2
- MySQL

## Getting Started

### Set FLASK_APP
- (Mac/Linux) `export FLASK_APP=serve.py`
    - add this line to `~/.bash_profile` or `~/.bashrc` to make permanent
- (Windows) `set FLASK_APP=serve.py`
    - do `setx FLASK_APP serve.py` instead to make permanent

### MySQL Credentials
Do one of the following:
1. Set Environment Variables
    - `S2_SECRET_KEY`
    - `S2_USER`
    - `S2_PASSWORD`
    - `S2_HOST`
    - `S2_DB`
2. Copy `config.py` to `realconfig.py` and replace the values in `realconfig.py` with your actual credentials. `realconfig.py` is in `.gitignore`. There is a `realconfig.py` in the `crossp` Athena locker with the production database credentials.

### Creating a Virtual Environment (After Fresh Clone Only)
- `python -m virtualenv venv`

### Loading the Virtual Environment (For New Terminal)
- (Mac/Linux) `. venv/bin/activate`
- (Windows) `venv\Scripts\activate`

*At this point we assume you are in the virtual environment.*

### Install Dependencies (First Time Only)
- `pip install -r requirements.txt`

### If You Add a Dependency
- `pip freeze > requirements.txt`

### Start the App
- `flask run`

## Tests
Run `py.test` to run all of the tests. We are using the `pylint` framework with `pylint-flask`.

Before you run the tests, you need to set environment variables:
- `S2_TEST_SECRET_KEY`
- `S2_TEST_USER`
- `S2_TEST_PASSWORD`
- `S2_TEST_HOST`
- `S2_TEST_DB`

**Note that running the tests will wipe whatever database you are testing on.**
Relatedly, each test function runs with a fresh database.
