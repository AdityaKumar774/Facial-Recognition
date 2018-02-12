from flask import Flask, json, Response, request
from werkzeug.utils import secure_filename
from os import path, getcwd
from db import Database
import time

app = Flask(__name__)

app.config['file_allowed'] = ['image/png', 'image/jpeg', 'image/jpg']
app.config['storage'] = path.join(getcwd(), 'storage')
app.db = Database()


def success_handle(output, status=200, mimetype='application/json'):
    return Response(output, status=status, mimetype=mimetype)


def error_handle(error_message, status=500, mimetype='application/json'):
    return Response(json.dumps({"error": {"message": error_message}}), status=status, mimetype=mimetype)

def get_user_by_id(user_id):
    user = {}
    results = app.db.select('SELECT users.id, users.name, users.created, faces.id, faces.user_id, faces.filename, faces.created FROM users LEFT JOIN faces ON faces.user_id = user_id WHERE users.id = ?', [user_id])
    for row in results:
        print(row)

    return user
def delete_user_by_id(user_id):
    print("Ok do it later")

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

            # get name in form data
            name = request.form['name']
            print("Information of that face is", name)
            print("File is allowed and will be saved in ", app.config['storage'])
            filename = secure_filename(file.filename)
            file.save(path.join(app.config['storage'], filename))
            # saving files to our storage

            # save files to sqlite3 database.db
            created = int(time.time())
            user_id = app.db.insert('INSERT INTO users(name, created) VALUES (?, ?)', [name, created])

            if user_id:
                print("User saved in database", name, user_id)
                # user has been saved with user_id and name now its timw to save faces
                face_id = app.db.insert('INSERT INTO faces(user_id, filename, created) VALUES (?, ?, ?)', [user_id, filename, created])

                if face_id:
                    print("Face has been saved to database")
                    face_data = {"id": face_id, "filename": filename, "created": created}
                    return_output = json.dumps({"id": user_id, "name": name, "face": [face_data]})
                    return success_handle(return_output)
                else:
                    print("Error in saving face image")
                    return error_handle("An error had occured while saving the face")

            else:
                print("Something went wrong")
                return error_handle("Error in inserting data to database")

        print("Request contain image")

    return success_handle(output)


# routing for user profile
@app.route('/api/users/<int:user_id>', methods=['GET', 'DELETE'])
def user_profile(user_id):
    if request.method == 'GET':
        user = get_user_by_id(user_id)

        return success_handle(user, 200)
    if request.method == 'DELETE':
        delete_user_by_id(user_id)
        return success_handle(json.dumps({"deleted": True}))

app.run()
