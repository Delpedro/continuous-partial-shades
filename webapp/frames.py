import tempfile
import subprocess
import os
import shutil
import glob

import logging
logger = logging.getLogger(__name__)


def extract_frames(stream, in_extension, out_extension):
    logger.debug('Extracting frames from {} as {}'.format(in_extension, out_extension))

    try:
        _, in_file = tempfile.mkstemp(suffix='.{}'.format(in_extension))
        with open(in_file, 'w+b') as f:
            f.write(stream.read())

        out_dir = tempfile.mkdtemp()
        save_pattern = '%06d.{}'.format(out_extension)
        search_pattern = os.path.join(out_dir, '*.{}'.format(out_extension))

        check_call(['convert', in_file, os.path.join(out_dir, save_pattern)])

        for path in sorted(glob.glob(search_pattern)):
            with open(path, 'r+b') as f:
                yield f.read()
    finally:
        if in_file:
            os.remove(in_file)
        if out_dir:
            shutil.rmtree(out_dir)

def sequence_frames(frames, extension):
    _, out_file = tempfile.mkstemp('.{}'.format(extension))

    try:
        frame_files = [save_frame(data, extension) for data in frames]

        cmd = ['convert']
        if extension == 'gif':
            cmd += ['-loop', '0', '-delay', '4', '-layers', 'Optimize']
        cmd += frame_files
        cmd.append(out_file)
        check_call(cmd)
    finally:
        for file in frame_files:
            os.remove(file)

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
