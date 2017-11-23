from flask import Response, json

def send_success_response(content):
    body = json.dumps(content)
    return Response(body, status=200, mimetype='application/json')

def send_error_response(error_code, error):
    body = json.dumps(error)
    return Response(body, status=error_code, mimetype='application/json')