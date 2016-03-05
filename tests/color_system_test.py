# -*- coding: utf-8 -*-

import json
import requests
import unittest

from pycolorname.color_system import ColorSystem
from pycolorname.utilities import make_temp


class ColorSystemTest(unittest.TestCase):

    def setUp(self):
        self.uut = ColorSystem()

    def test_dict(self):
        self.uut['test_key'] = 'test_val'
        self.assertEqual(len(self.uut), 1)
        self.assertEqual(list(self.uut.keys()), ['test_key'])
        self.assertEqual(list(self.uut.values()), ['test_val'])
        self.assertEqual(list(self.uut.items())[0], ('test_key', 'test_val'))
        self.assertIn('test_key', self.uut)

        self.uut.clear()
        self.assertEqual(len(self.uut), 0)
        self.assertNotIn('test_key', self.uut)

        self.uut.update({"test_key": "test_val"})
        self.assertEqual(list(self.uut.items())[0], ('test_key', 'test_val'))

    def test_load(self):
        old_refresh = self.uut.refresh
        test_data = {"name": "color"}
        try:
            self.uut.refresh = lambda: test_data
            with make_temp() as filename:
                self.uut.load(filename)

                # Test if data loaded into class
                self.assertEqual(dict(self.uut), test_data)

                # Test if data saved into file
                with open(filename) as fp:
                    json_data = json.load(fp)
                self.assertEqual(json_data, test_data)

                # Test if data is being read from file
                self.uut.clear()
                self.uut.refresh = lambda: {}
                self.uut.load(filename)
                self.assertEqual(json_data, test_data)

                # Test if load() respects refresh param and clears old data
                test_data = {"name2": "color2"}
                self.uut.refresh = lambda: test_data
                self.uut.load(filename, refresh=True)
                self.assertEqual(dict(self.uut), test_data)
        finally:
            self.uut.refresh = old_refresh

    def test_request(self):
        test_url = "http://a_url_to_test_with.org"

        def mock_request(url):
            self.assertEqual(url, test_url)

            class MockResponse:
                text = "<title>Test title</title>"
            return MockResponse()

        old_request = requests.request
        try:
            requests.request = mock_request
            bs = self.uut.request(test_url)
            self.assertEqual(bs.title.text, 'Test title')
        finally:
            requests.request = old_request

    def test_hex_to_rgb(self):
        self.assertEqual(self.uut.hex_to_rgb("#000"), [0, 0, 0])
        self.assertEqual(self.uut.hex_to_rgb("#010101"), [1, 1, 1])
        self.assertEqual(self.uut.hex_to_rgb("#aaa"), [170, 170, 170])
        self.assertEqual(self.uut.hex_to_rgb("fff"), [255, 255, 255])
        with self.assertRaises(ValueError):
            self.uut.hex_to_rgb("a")
