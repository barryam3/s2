# s2 API
*A mostly RESTful web service.*

## Technical Overview
We're using Python because we want to host this on scripts.mit.edu which only supports PHP, Perl, and Python; Python is by far the most popular of the three at MIT. We're using the Flask microframework because it's powerful and easy to pick up. We're using MySQL because it's provided for free by MIT SIPB.

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
- Python 3
- MySQL (local or [remote](https://sql.mit.edu/main/do/index))

## Getting Started

### Set FLASK_APP
- (Mac/Linux) `export FLASK_APP=serve.py`
    - add this line to `~/.bash_profile` or `~/.bashrc` to make permanent
- (Windows) `set FLASK_APP=serve.py`
    - do `setx FLASK_APP serve.py` instead to make permanent

### MySQL Credentials
Do one of the following:
1. Set Environment Variables
    - S2_DB_USER
    - S2_DB_PASS
    - S2_DB_HOST
    - S2_DB-NAME
2. Copy `config.py` to `realconfig.py` and replace the values in `realconfig.py` with your actual credentials. `realconfig.py` is in `.gitignore`. There is a `realconfig.py` in the `crossp` Athena locker with the production database credentials.

### Creating a Virtual Environment (After Fresh Clone Only)
- `python3 -m venv venv`

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

## Contributing
Run `pylint app` and fix any non-TODO errors before each commit.

## DB Note
You can create a database using the dump in `ssdb.sql`. The command to do so (after creating the database) is `mysql yourkerb+s2 < ssdb.sql`. If this does not work, you can paste and execute the SQL manually.
