from flask import Blueprint, send_from_directory

from app.utils import res

test = Blueprint('test', __name__)

@app.route('/')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/stylesheets/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/javascripts/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
    

