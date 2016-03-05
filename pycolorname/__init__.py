# -*- coding: utf-8 -*-

import os

from pycolorname.utilities import PROJECT_PATH


with open(os.path.join(PROJECT_PATH, "VERSION")) as fp:
    __version__ = fp.read().strip()
