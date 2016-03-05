# -*- coding: utf-8 -*-

import re

from pycolorname.color_system import ColorSystem
from pycolorname.utilities import u


class PantonePaint(ColorSystem):

    def __init__(self, *args, **kwargs):
        ColorSystem.__init__(self, *args, **kwargs)
        self.load()

    def refresh(self):
        full_data = self.request(
            'POST',
            'http://www.pantonepaint.co.kr/color/color_chip_ajax.asp',
            data={"cmp": "TPX", "keyword": ""})
        lis = full_data.find_all('li', attrs={"attr_name": re.compile(r".*"),
                                              "attr_number": re.compile(r".*"),
                                              "attr_company": re.compile(r".*"),
                                              "id": re.compile(r".*")})

        data = {}
        style_regex = re.compile(r'.*background-color *: *'
                                 r'rgb\((?P<rgb>[\d,]+ *).*')
        for li in lis:
            name = u("PMS {} {} ({})").format(li['attr_number'],
                                              li['attr_company'],
                                              li['attr_name'])
            rgb = re.findall(style_regex, li['style'])[0]
            rgb = map(lambda x: int(x.strip()), rgb.split(","))
            color = list(rgb)
            data[name] = color
        return data
