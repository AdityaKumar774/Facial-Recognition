import output as output
from flask import Flask, json, Response

app = Flask(__name__)


def success_handle(output, status=200, mimetype='application/json'):
    return Response(output, status=status, mimetype=mimetype)


def error_handle(error_message, status=500, mimetype='application/json'):
    return Response(json.dumps({"error": {"message": error_message}}), status=status, mimetype=mimetype)


@app.route('/', methods=['GET'])
def homepage():
    print('Welcome');

    output = json.dumps({"api": "1.0"})

    return success_handle(output)


app.run()
