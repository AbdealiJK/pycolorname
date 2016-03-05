# -*- coding: utf-8 -*-

import unittest

from pycolorname.ral.classic.wikipedia import Wikipedia


class WikipediaTest(unittest.TestCase):

    def setUp(self):
        self.uut = Wikipedia()
        self.uut.load(refresh=True)

    def test_data(self):
        self.assertEqual(len(self.uut), 213)

        # We check a few random colors to be sure that things are fine.
        self.assertEqual(self.uut['RAL 1000 (Green beige)'],
                         [204, 197, 143])
        self.assertEqual(self.uut['RAL 3016 (Coral red)'],
                         [172, 64, 52])
        self.assertEqual(self.uut['RAL 5021 (Water blue)'],
                         [7, 115, 122])
        self.assertEqual(self.uut['RAL 7009 (Green grey)'],
                         [91, 98, 89])
        self.assertEqual(self.uut['RAL 9023 (Pearl dark grey)'],
                         [126, 129, 130])
