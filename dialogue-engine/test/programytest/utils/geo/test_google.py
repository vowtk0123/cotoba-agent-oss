"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import unittest
import os
import json

from programy.utils.geo.google import GoogleMaps, GoogleDistance, GoogleDirections
from programy.utils.geo.latlong import LatLong


class MockGoogleMaps(GoogleMaps):

    def __init__(self, data_file_name):
        self._data_file_name = data_file_name

    def _get_response_as_json(self, url):
        with open(self._data_file_name, "r", encoding="utf-8") as data_file:
            return json.load(data_file)


class GoogleMapsTests(unittest.TestCase):

    def test_location(self):
        filename = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        self.assertTrue(os.path.isfile(filename))
        googlemaps = MockGoogleMaps(filename)
        self.assertIsNotNone(googlemaps)

        latlng = googlemaps.get_latlong_for_location("KY3 9UR")
        self.assertIsNotNone(latlng)
        self.assertIsInstance(latlng, LatLong)
        self.assertEqual(latlng.latitude, 56.0720397)
        self.assertEqual(latlng.longitude, -3.1752001)

    def test_distance_uk_driving_imperial(self):
        filename = os.path.dirname(__file__) + os.sep + "distance.json"
        self.assertTrue(os.path.isfile(filename))
        googlemaps = MockGoogleMaps(filename)
        self.assertIsNotNone(googlemaps)

        distance = googlemaps.get_distance_between_addresses("Edinburgh", "London", country="UK", mode="driving", units="imperial")
        self.assertIsNotNone(distance)
        self.assertIsInstance(distance, GoogleDistance)
        self.assertEqual("25.1 mi", distance._distance_text)

    def test_directions(self):
        filename = os.path.dirname(__file__) + os.sep + "directions.json"
        self.assertTrue(os.path.isfile(filename))
        googlemaps = MockGoogleMaps(filename)
        self.assertIsNotNone(googlemaps)

        directions = googlemaps.get_directions_between_addresses("Edinburgh", "London")
        self.assertIsNotNone(directions)
        self.assertIsInstance(directions, GoogleDirections)
