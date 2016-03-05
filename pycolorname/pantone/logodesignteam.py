# -*- coding: utf-8 -*-

import cssutils
import logging
import re
import requests

from pycolorname.color_system import ColorSystem


class LogoDesignTeam(ColorSystem):

    def __init__(self, *args, **kwargs):
        ColorSystem.__init__(self, *args, **kwargs)
        cssutils.log.setLevel(logging.CRITICAL)
        self.load()

    def refresh(self):
        full_data = self.request(
            'GET',
            'http://www.logodesignteam.com/logo-design-pantone-color-chart'
            '.html')
        css_request = requests.request(
            'GET',
            'http://www.logodesignteam.com/css/style.css')

        # Parse css and save only required data
        css_data = cssutils.parseString(css_request.text, validate=False)
        css_rules = {}
        for css_rule in css_data.cssRules:
            if not isinstance(css_rule, cssutils.css.CSSStyleRule):
                continue
            css_bgcolor = css_rule.style.backgroundColor
            if not css_bgcolor:
                continue
            for css_selector in css_rule.selectorList:
                if css_selector.selectorText.startswith(".color"):
                    css_classname = css_selector.selectorText.replace(".", "")
                    css_rules[css_classname] = css_bgcolor

        name_uls = full_data.find_all('ul', {'class': "color_text"})
        color_uls = full_data.find_all('ul', {'class': "colors"})

        data = {}
        for name_ul, color_ul in zip(name_uls, color_uls):
            name_lis = name_ul.find_all('li')
            color_lis = color_ul.find_all('li')
            for name_li, color_li in zip(name_lis, color_lis):
                for color_class in color_li['class']:
                    color = css_rules.get(color_class, None)
                    # Color not found or invalid color class
                    if color is None or not color_class.startswith("color"):
                        continue
                    color = self.hex_to_rgb(color)
                    name = name_li.text.strip()
                    if 'Pantone' not in name:
                        name = 'Pantone ' + name
                    name = re.sub(r'Pantone (?P<ID>\d+)', r'PMS \g<ID>', name)
                    data[name] = color
                    break
        data['White'] = [255, 255, 255]  # Add white
        return data
