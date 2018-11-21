from flask import Response, json

def res(body={}, status=200):
    json_body = json.dumps(body)
    return Response(json_body, status=status, mimetype='application/json')
