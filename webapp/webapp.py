from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from redis import Redis
from redis.exceptions import ConnectionError

app = Flask(__name__)
logger = app.logger
redis = Redis(host="redis")

# while True:
#     try:
#         redis.keys('*')
#     except ConnectionError:
#         logger.debug('Redis is unavailable - sleeping')
#         sleep(1)

redis.delete('frames_in', 'frames_out')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    frames_in = [file.read()]
    frames_out = [None for _ in frames_in]
    done = 0

    for idx, frame in enumerate(frames_in):
        message = bytes(str(idx), encoding='ascii') + b':' + frame
        logger.debug('Sending: {}...'.format(repr(message[:50])))
        redis.rpush('frames_in', message)

    while done < len(frames_in):
        logger.debug("Waiting for frame")
        message = redis.blpop(['frames_out'])[1]
        logger.debug("Got {} bytes".format(len(message)))

        idx, frame = message.split(b':', 1)
        logger.debug("Frame no {}, {} bytes".format(idx, len(frame)))

        frames_out[int(idx)] = frame
        done += 1

    resp = make_response(frames_out[0])
    resp.headers['Content-Type'] = request.headers['Content-Type']
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
