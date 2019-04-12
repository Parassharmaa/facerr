from flask import Flask, request
import json
from modules.facer import get_encodings, match_encodings
from modules.db import save_encoding, save_image_data, fetch_encoding, fetch_image_data
import logging
import traceback

api = Flask(__name__)


@api.route("/image/upload", methods=['POST'])
def add_image():
    '''Upload image

    Params:
        image -- Image File

    Returns:
        image_id -- [id of the image]
    '''

    try:
        f = request.files['image']
        e = get_encodings(f)

        if len(e) > 0:
            resp = save_encoding(e[0].tobytes())
            return json.dumps({'image_id': str(resp.inserted_id)}), 200
        else:
            return json.dumps({'message': 'no face found'}), 500

    except Exception as e:
        logging.error(str(e))
        return json.dumps({'message': 'Something went wrong'}), 500


@api.route("/image/data", methods=['POST'])
def add_data():
    '''Add image data to image id

    Header:
        Content-Type: application/json
    Params:
        image_id -- [id of the image]
        data -- data of the coressponding image
    '''

    try:
        content = request.json

        image_id = content['image_id']
        resp = save_image_data(content['data'], image_id)
        return json.dumps({'id': str(resp.inserted_id)})
    except Exception as e:
        logging.error(str(e))
        return json.dumps({'message': 'Something went wrong'}), 500


@api.route("/image/query", methods=['POST'])
def query_image():
    '''Query image data

    Params:
        image -- Image File
    '''

    try:
        f = request.files['image']
        e = get_encodings(f)

        if len(e) > 0:
            all_e = fetch_encoding()
            image_id = match_encodings(e[0], all_e)
            if image_id:
                resp = fetch_image_data(image_id)
                if resp:
                    resp['_id'] = str(resp['_id'])
                    return json.dumps(resp)
            return json.dumps({'message': 'No match found'})
        else:
            return json.dumps({'message': 'no face found'}), 200
    except Exception as e:
        logging.error(str(e))
        print(traceback.print_exc())
        return json.dumps({'message': 'Something went wrong'}), 500


if __name__ == "__main__":
    api.run(debug=True)
