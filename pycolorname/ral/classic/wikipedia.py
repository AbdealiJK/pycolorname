# -*- coding: utf-8 -*-

import re

from pycolorname.color_system import ColorSystem


class Wikipedia(ColorSystem):

    def __init__(self, *args, **kwargs):
        ColorSystem.__init__(self, *args, **kwargs)
        self.load()

    def refresh(self):
        full_data = self.request(
            'GET',
            "https://en.wikipedia.org/wiki/List_of_RAL_colors")
        trs = full_data.find_all('tr')

        data = {}
        style_regex = re.compile(r'.*background *: *'
                                 r'(?P<rgb_hex>[0-9a-fA-F#]+).*')
        for tr in trs:
            tds = tr.find_all('td')
            # The tds are in the order:
            # RAL code, colored square, L, a, b, german name, english name, desc

            if len(tds) != 8:
                continue
            name = "{} ({})".format(tds[0].text.strip(), tds[6].text.strip())
            rgb_hex = re.findall(style_regex, tds[1]['style'])[0]
            color = self.hex_to_rgb(rgb_hex)
            data[name] = color
        return data
