# -*- coding: utf-8 -*-

import bs4 as BeautifulSoup
import json
import os
import requests
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
from colormath.color_objects import LabColor, sRGBColor

from pycolorname.utilities import PROJECT_PATH


class ColorSystem(dict):
    """
    Provides an interface for a color system.
    """

    def value_preprocess(self, value):
        if isinstance(value, list) and len(value) == 3:
            return tuple(value)
        return value

    def __getitem__(self, key):
        return self.value_preprocess(dict.__getitem__(self, key))

    def items(self):
        return ((key, self.value_preprocess(val))
                for key, val in dict.items(self))

    def data_file(self):
        modulename = self.__module__
        return os.path.join(PROJECT_PATH, "data", modulename + ".json")

    def load(self, filename=None, refresh=False):
        """
        Try to load the data from a pre existing data file if it exists.
        If the data file does not exist, refresh the data and save it in
        the data file for future use.
        The data file is a json file.

        :param filename: The filename to save or fetch the data from.
        :param refresh:  Whether to force refresh the data or not
        """
        filename = filename or self.data_file()
        dirname = os.path.dirname(filename)

        if refresh is False:
            try:
                data = None
                with open(filename) as fp:
                    data = json.load(fp)
                self.clear()
                self.update(data)
                return
            except (ValueError, IOError):
                # Refresh data if reading gave errors
                pass

        data = self.refresh()
        self.clear()
        self.update(data)

        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with open(filename, 'w') as fp:
            json.dump(data, fp,
                      sort_keys=True,
                      indent=2,
                      separators=(',', ': '))

    def refresh(self):
        """
        Refreshes the cached data from the URL provided for this color system.
        """
        raise NotImplementedError

    def request(self, *args, **kwargs):
        """
        Gets the request using the `_url` and converts it into a
        beautiful soup object.

        :param args:            The args to pass on to `requests`.
        :param kwargs:          The kwargs to pass on to `requests`.
        """
        response = requests.request(*args, **kwargs)
        return BeautifulSoup.BeautifulSoup(response.text, "html.parser")

    def hex_to_rgb(self, value):
        val = value

        if val[0] == '#':  # Remove # if it's present
            val = val[1:]

        # Convert to array with 3 hex values
        if len(val) == 3:  # Catch cases where 3 letter hex is used eg: #aaa
            val = [val[i] * 2 for i in range(len(val))]
        elif len(val) == 6:
            val = [val[i:i+2] for i in range(0, len(val), 2)]
        else:
            raise ValueError("Invalid value given for hex {0}".format(value))

        return tuple(int(v, 16) for v in val)

    def find_closest(self, color):
        """
        Find the closest color in the system to the given rgb values.

        :param color: Tuple of r, g, b values (scaled to 255).
        :returns:     Tuple of name and rgb closest to the given color.
        """
        # Find distance between colors and find name based on closest color
        rgb = sRGBColor(*color)
        lab = convert_color(rgb, LabColor, target_illuminant='D65')
        min_diff = float("inf")
        min_name, min_color = "", ()
        for known_name, known_color in self.items():
            known_rgb = sRGBColor(*known_color)
            known_lab = convert_color(known_rgb, LabColor,
                                      target_illuminant='D65')
            diff = delta_e_cie1976(lab, known_lab)
            if min_diff > diff:
                min_diff = diff
                min_name = known_name
                min_color = known_color
        return min_name, min_color
