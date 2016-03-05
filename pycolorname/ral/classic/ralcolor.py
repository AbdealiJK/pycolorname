# -*- coding: utf-8 -*-

import re

from pycolorname.color_system import ColorSystem
from pycolorname.utilities import u


class RALColor(ColorSystem):

    def __init__(self, *args, **kwargs):
        ColorSystem.__init__(self, *args, **kwargs)
        self.load()

    def refresh(self):
        full_data = self.request('GET', "http://www.ralcolor.com/")
        trs = full_data.find_all('tr')

        data = {}
        for tr in trs:
            tds = tr.find_all('td')
            # The tds are in the order:
            # RAL code, hyphen rgb, rgb-hex, dutch name, english name, etc.

            if len(tds) < 5:
                continue

            if (not tds[0].text.strip().startswith("RAL") and
                    tds[1].text.strip().startswith("RAL") and
                    tds[1].text.strip() != "RAL"):  # omit head of table
                # Note: In some places there is an extra empty td at the
                #       beginning. We ignore that.
                tds = tds[1:]

            ral_code = re.sub(re.compile(r"\s+"), " ", tds[0].text.strip())
            # Replace &nbsp with space also
            eng_name = re.sub(re.compile(u(r"[\s\u00A0]+")), " ",
                              tds[4].text.strip())

            if ral_code.startswith("RAL"):
                name = "{0} ({1})".format(ral_code, eng_name)
                # Note: We replace `#` as some hex values in the site are
                #       named wrongly as ##FFFF00.
                #       Also, we use the 3rd column - which holds the hex
                #       value. The 2nd column has the r-g-b and they don't
                #       match !
                color = self.hex_to_rgb(tds[2].text.strip().replace("#", ""))
                data[name] = color
        return data
