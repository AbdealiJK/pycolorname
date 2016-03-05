# -*- coding: utf-8 -*-

import re
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976

from pycolorname.color_system import ColorSystem


class CalPrint(ColorSystem):

    def __init__(self, *args, **kwargs):
        ColorSystem.__init__(self, *args, **kwargs)
        self.load()

    def refresh(self):
        full_data = self.request('GET',
                                 "http://www.cal-print.com/InkColorChart.htm")
        tds = full_data.find_all('td', attrs={"bgcolor": re.compile(r".*")})

        raw_data = {}
        known_names = []
        for td in tds:
            table = td.find_parent('table')
            name = table.find("font").text
            color = self.hex_to_rgb(td['bgcolor'])

            # remove excess whitespace
            name = re.sub(re.compile(r"\s+"), " ", name.strip())
            if 'PMS' not in name and 'Pantone' not in name:
                name = 'Pantone ' + name
            raw_data[name] = color

            if not name.startswith('PMS'):
                known_names.append(name)
        # Add white
        raw_data['White'] = [255, 255, 255]
        known_names.append('White')

        # Find distance between colors and find better names for unnamed
        # colors in the table.
        data = {}
        for name, color in raw_data.items():
            rgb = sRGBColor(*color)
            lab = convert_color(rgb, LabColor, target_illuminant='D65')
            min_diff = float("inf")
            min_name, min_color = "", ()
            for known_name in known_names:
                known_color = raw_data[known_name]
                known_rgb = sRGBColor(*known_color)
                known_lab = convert_color(known_rgb, LabColor,
                                          target_illuminant='D65')
                diff = delta_e_cie1976(lab, known_lab)
                if min_diff > diff:
                    min_diff = diff
                    min_name, min_color = known_name, known_color
            data['{} ({})'.format(name, min_name)] = color
        return data
