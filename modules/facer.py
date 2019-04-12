import face_recognition


def get_encodings(image):
    image = face_recognition.load_image_file(image)
    return face_recognition.face_encodings(image)


def match_encodings(unknown, known):
    image_id = None
    known_e, known_i = known
    matches = face_recognition.compare_faces(known_e, unknown)
    if True in matches:
        first_match_index = matches.index(True)
        image_id = known_i[first_match_index]
    return image_id
