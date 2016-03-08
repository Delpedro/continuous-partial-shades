import shades
import logging
from redis import Redis
from redis.exceptions import ConnectionError
from time import sleep
from tempfile import NamedTemporaryFile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

redis = Redis(host="redis")

redis.delete('frames_in', 'frames_out')

def process(frame):
    in_file = NamedTemporaryFile(suffix='.jpg', delete=False)
    in_file.write(frame)
    in_file.close()

    out_file = NamedTemporaryFile(suffix='.jpg', delete=False)
    out_file.close()

    shades.add_shades(in_file.name, out_file.name)

    return open(out_file.name, 'rb').read()

while True:
    logger.debug("Waiting for frame")
    message = redis.blpop(['frames_in'])[1]
    logger.debug("Got {} bytes".format(len(message)))

    idx, frame = message.split(b':', 1)
    logger.debug("Frame no {}, {} bytes".format(idx, len(frame)))

    processed_frame = process(frame)
    logger.debug('Processed frame no {}, {} bytes'.format(idx, len(processed_frame)))

    reply = idx + b':' + processed_frame

    logger.debug('Sending: {}...'.format(repr(reply[:50])))
    redis.lpush('frames_out', reply)
