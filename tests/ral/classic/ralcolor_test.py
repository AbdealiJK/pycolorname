# -*- coding: utf-8 -*-

import unittest

from pycolorname.ral.classic.ralcolor import RALColor
from pycolorname.utilities import u


class RALColorTest(unittest.TestCase):
    def setUp(self):
        self.uut = RALColor()
        self.uut.load(refresh=True)

    def test_data(self):
        self.assertEqual(len(self.uut), 213)
        
        # We check a few random colors to be sure that things are fine.
        self.assertEqual(self.uut['RAL 1000 (Green beige)'],
                         [190, 189, 127])
        self.assertEqual(self.uut['RAL 3016 (Coral red)'],
                         [179, 40, 33])
        self.assertEqual(self.uut['RAL 5021 (Water blue)'],
                         [37, 109, 123])
        self.assertEqual(self.uut['RAL 7009 (Green grey)'],
                         [77, 86, 69])
        self.assertEqual(self.uut['RAL 9023 (Pearl dark grey)'],
                         [130, 130, 130])
