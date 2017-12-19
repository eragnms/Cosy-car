# -*- coding: utf-8 -*-

import unittest
import logging
from unittest.mock import patch
import configparser
import datetime

from cosycar.constants import Constants
from cosycar.weather import CosyWeather

CFG_FILE = 'tests/data/cosycar_template.cfg'


class CarSectionTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='tests/data/cosycar.log',
            level='DEBUG',
            format=Constants.log_format)
        self._config = configparser.ConfigParser()
        self._config.read(CFG_FILE)
        self._weather_interval = 10

    def tearDown(self):
        pass

    @patch('configparser.ConfigParser.get')
    def test_fetch_from_file(self, get_mock):
        now = datetime.datetime.now()
        timestamp = now - datetime.timedelta(minutes=self._weather_interval)
        get_mock.return_value = timestamp
        weather = CosyWeather("Country",
                              "City",
                              "mykey",
                              "/tmp/test_weather_file",
                              self._weather_interval)
        weather_data = weather.get_weather()
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
