import tempfile
import subprocess

import logging
logger = logging.getLogger(__name__)


def extract_frames(image, extension):
    logger.debug('Extracting frames from {} as {}'.format(image.format, extension))

    _, out_file = tempfile.mkstemp('.{}'.format(extension))
    idx = 0

    while True:
        try:
            image.convert('RGB').save(out_file)
            data = open(out_file, 'rb').read()
            logger.debug('Frame {}: {} bytes'.format(idx, len(data)))
            yield data
            idx += 1
            image.seek(idx)
        except EOFError:
            break


def sequence_frames(frames, extension):
    _, out_file = tempfile.mkstemp('.{}'.format(extension))

    frame_files = [save_frame(data, extension) for data in frames]

    cmd = ['convert']
    cmd += frame_files
    cmd.append(out_file)
    check_call(cmd)

    return out_file


def save_frame(data, extension):
    file, path = tempfile.mkstemp('.{}'.format(extension))
    with open(file, 'w+b') as fd:
        fd.write(data)
    return path


def check_call(cmd, *args, **kwargs):
    logger.info("$ %s" % " ".join(cmd))
    output = ""

    try:
        output = subprocess.check_output(cmd, *args, **kwargs)
    except subprocess.CalledProcessError:
        log.error(output)
        raise
