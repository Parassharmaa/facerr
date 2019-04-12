import pymongo
import numpy as np


def get_db():
    client = pymongo.MongoClient(
        "mongodb+srv://user_1:helloworld@cluster0-taek0.mongodb.net/test?retryWrites=true")
    db = client.facer
    return db


def save_encoding(data):
    db = get_db()
    coll = db['encodings']
    return coll.insert_one({'encoding': data})


def fetch_image_data(image_id):
    db = get_db()
    coll = db['idata']
    return coll.find_one({"image_id": image_id})


def save_image_data(data, image_id):
    db = get_db()
    coll = db['idata']
    return coll.insert_one({'data': data, 'image_id': image_id})


def fetch_encoding():
    db = get_db()
    coll = db['encodings']
    known_faces = []
    image_ids = []
    for e in coll.find():
        known_faces.append(np.frombuffer(e['encoding']))
        image_ids.append(str(e['_id']))
    return known_faces, image_ids
