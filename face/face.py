import face_recognition
from os import path


class Face:
    def __init__(self, app):
        self.storage = app.config["storage"]
        self.db = app.db
        self.faces = []  # store all faces in cache array of face object
        self.known_encoding_faces = []  # faces data for recognition
        self.face_user_keys = {}
        self.load_all()

    def load_train_file_by_name(self, name):
        trained_storage = path.join(self.storage, 'trained')
        return path.join(trained_storage, name)

    def load_all(self):
        print("Hey there")
        results = self.db.select('SELECT faces.id, faces.user_id, faces.filename, faces.created From faces')

        for row in results:
            print(row)
            user_id = row[1]
            filename = row[2]

            face = {
                "id": row[0],
                "user_id": user_id,
                "filename": filename,
                "created": row[3]
            }
            self.faces.append(face)

            face_image = face_recognition.load_image_file(self.load_train_file_by_name(filename))
            face_image_encoding = face_recognition.face_encodings(face_image)[0]
            index_key = len(self.known_encoding_faces)
            self.known_encoding_faces.append(face_image_encoding)
            index_key_string = str(index_key)
            self.face_user_keys['{0}', format(index_key_string)] = user_id

        print(self.faces)
