import shades
from redis import Redis
from redis.exceptions import ConnectionError
from time import sleep
from tempfile import NamedTemporaryFile

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

redis = Redis(host="redis")

redis.delete('frames_in', 'frames_out')


def process(frame, extension):
    suffix = '.{}'.format(extension)

    in_file = NamedTemporaryFile(suffix=suffix, delete=False)
    in_file.write(frame)
    in_file.close()

    out_file = NamedTemporaryFile(suffix=suffix, delete=False)
    out_file.close()

    shades.add_shades(in_file.name, out_file.name)

    return open(out_file.name, 'rb').read()


def encode(idx, extension, data):
    return b':'.join([
        str(idx).encode('ascii'),
        extension.encode('ascii'),
        data
    ])


def decode(message):
    idx, extension, data = message.split(b':', 2)
    return int(idx), extension.decode('ascii'), data


while True:
    logger.debug("Waiting for frame")
    message = redis.blpop(['frames_in'])[1]
    logger.debug("Got {} bytes".format(len(message)))

    idx, extension, frame = decode(message)
    logger.debug("Frame no {}, extension: {}, {} bytes".format(idx, extension, len(frame)))

    processed_frame = process(frame, extension)
    logger.debug('Processed frame no {}, {} bytes'.format(idx, len(processed_frame)))

    reply = encode(idx, extension, processed_frame)
    logger.debug('Sending: {}...'.format(repr(reply[:50])))
    redis.lpush('frames_out', reply)
