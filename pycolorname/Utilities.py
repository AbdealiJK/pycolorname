# -*- coding: utf-8 -*-

import os
import sys
import tempfile

from contextlib import contextmanager


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))


if sys.version_info < (3,):
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x


@contextmanager
def make_temp(suffix="", prefix="tmp", dir=None):
    """
    Creates a temporary file with a closed stream and deletes it when done.

    :return: A contextmanager retrieving the file path.
    """
    temporary = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    os.close(temporary[0])
    try:
        yield temporary[1]
    finally:
        os.remove(temporary[1])
