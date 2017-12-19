cd api
export FLASK_APP=serve.py
if [ -z "$SECRET_KEY" ]; then
    echo "Warning: SECRET_KEY not set."
fi
if [ -z "$MYSQL_HOST" ]; then
    echo "Warning: MYSQL_HOST not set."
fi
if [ -z "$MYSQL_USER" ]; then
    echo "Warning: MYSQL_USER not set."
fi
if [ -z "$MYSQL_PASS" ]; then
    echo "Warning: MYSQL_PASS not set."
fi
if [ -z "$MYSQL_DB" ]; then
    echo "Warning: MYSQL_DB not set."
fi
flask run
