# -*- coding: utf-8 -*-

import unittest

from pycolorname.pantone.cal_print import CalPrint


class CalPrintTest(unittest.TestCase):
    def setUp(self):
        self.uut = CalPrint()
        self.uut.load(refresh=True)

    def test_data(self):
        self.assertEqual(len(self.uut), 992)
        self.assertIn("White (White)", self.uut)

        # We check a few random colors to be sure that things are fine.
        self.assertEqual(self.uut['PMS 245 (Pantone Purple)'],
                         [232, 127, 201])
        self.assertEqual(self.uut['PMS 202 (Pantone Rubine Red 2X)'],
                         [140, 38, 51])
        self.assertEqual(self.uut['Pantone Cool Gray 5 (Pantone Cool Gray 5)'],
                         [186, 183, 175])
        self.assertEqual(self.uut['PMS 1345 (Pantone Warm Gray 2)'],
                         [255, 214, 145])
        self.assertEqual(self.uut['Pantone Purple (Pantone Purple)'],
                         [191, 48, 181])


        # Check that the nearest color to named colors are themselves.
        # As, delta_e for named colors with themselves should be minimum.
        for name, color in self.uut.items():
            if not name.startswith("PMS"):
                original_name, nearest_name = name.split(" (")
                nearest_name = nearest_name.replace(")", "")
                self.assertEqual(original_name, nearest_name)
