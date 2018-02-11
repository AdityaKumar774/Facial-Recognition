from flask import Flask, json, Response, request
from werkzeug.utils import secure_filename
from os import path, getcwd

app = Flask(__name__)

app.config['file_allowed'] = ['image/png', 'image/jpeg', 'image/jpg']
app.config['storage'] = path.join(getcwd(), 'storage')


def success_handle(output, status=200, mimetype='application/json'):
    return Response(output, status=status, mimetype=mimetype)


def error_handle(error_message, status=500, mimetype='application/json'):
    return Response(json.dumps({"error": {"message": error_message}}), status=status, mimetype=mimetype)


@app.route('/', methods=['GET'])
def homepage():

    output = json.dumps({"api": "1.0"})
    return success_handle(output)

@app.route('/api/train', methods=['POST'])
def train():
    output = json.dumps({"Success": True})

    if 'file' not in request.files:
        print("Face image is required")
        return error_handle("Face image is required!")
    else:
        print("File request", request.files)
        file = request.files['file']
        if file.mimetype not in app.config['file_allowed']:
            print("File extension is not allowed!")
            return error_handle("We are allowed to upload only files with extension *.png, *.jpeg, *.jpg")
        else:
            print("File is allowed and will be saved in ", app.config['storage'])
            filename = secure_filename(file.filename)
            file.save(path.join(app.config['storage'], filename))
            # saving files to our storage

        print("Request contain image")

    return success_handle(output)


app.run()
