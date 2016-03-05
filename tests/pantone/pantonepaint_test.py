# -*- coding: utf-8 -*-

import unittest

from pycolorname.pantone.pantonepaint import PantonePaint
from pycolorname.utilities import u


class PantonePaintTest(unittest.TestCase):

    def setUp(self):
        self.uut = PantonePaint()
        self.uut.load(refresh=True)

    def test_data(self):
        self.assertEqual(len(self.uut), 2095)

        # We check a few random colors to be sure that things are fine.
        self.assertEqual(self.uut['PMS 19-5918 TPX (Mountain View)'],
                         [48, 65, 54])
        self.assertEqual(self.uut['PMS 14-2808 TPX (Sweet Lilac)'],
                         [231, 184, 211])
        self.assertEqual(self.uut['PMS 15-4717 TPX (Aqua)'],
                         [99, 162, 176])
        self.assertEqual(self.uut['PMS 16-1720 TPX (Strawberry Ice)'],
                         [227, 134, 143])
        self.assertEqual(self.uut['PMS 19-4056 TPX (Olympian Blue)'],
                         [46, 84, 147])

        # Check names with unicode are working correctly
        self.assertEqual(self.uut[u('PMS 16-5919 TPX (Cr\xe9me de Menthe)')],
                         [114, 162, 139])
