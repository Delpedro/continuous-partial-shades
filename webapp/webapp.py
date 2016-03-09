from PIL import Image
from flask import Flask
from flask import send_file
from flask import render_template
from flask import request
from redis import Redis
from redis.exceptions import ConnectionError

from frames import extract_frames, sequence_frames

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
redis = Redis(host="redis")

redis.delete('frames_in', 'frames_out')

FRAME_EXTENSION = 'jpg'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    extension = file.filename.rpartition('.')[2]

    image = Image.open(file.stream)
    image_format = image.format

    frames_in = list(extract_frames(image, FRAME_EXTENSION))
    frames_out = [None for _ in frames_in]
    done = 0

    for idx, frame in enumerate(frames_in):
        message = encode(idx, FRAME_EXTENSION, frame)
        logger.debug('Sending: {}...'.format(repr(message[:50])))
        redis.rpush('frames_in', message)

    while done < len(frames_in):
        logger.debug("Waiting for frame")
        message = redis.blpop(['frames_out'])[1]
        logger.debug("Got {} bytes".format(len(message)))

        idx, _, frame = decode(message)
        logger.debug("Frame no {}, {} bytes".format(idx, len(frame)))

        frames_out[idx] = frame
        done += 1

    processed_file = sequence_frames(frames_out, extension)
    return send_file(processed_file)


def encode(idx, extension, data):
    return b':'.join([
        str(idx).encode('ascii'),
        extension.encode('ascii'),
        data
    ])


def decode(message):
    idx, extension, data = message.split(b':', 2)
    return int(idx), extension.decode('ascii'), data


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
