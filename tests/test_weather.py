# -*- coding: utf-8 -*-

import unittest
import logging
from unittest.mock import patch
import configparser
import datetime

from cosycar.constants import Constants
from cosycar.weather import CosyWeather

CFG_FILE = 'tests/data/cosycar_template.cfg'


class WeatherTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='tests/data/cosycar.log',
            level='DEBUG',
            format=Constants.log_format)
        self._config = configparser.ConfigParser()
        self._config.read(CFG_FILE)
        self._weather_interval = 10
        self._weather_file = "/tmp/test_weather_file"

    def tearDown(self):
        pass


    @patch('configparser.ConfigParser.options')
    @patch('configparser.ConfigParser.read')
    @patch('cosycar.weather.CosyWeather._fetch_wunder_weather')
    @patch('configparser.ConfigParser.get')
    def test_fetch_from_file(self,
                             get_mock,
                             fetch_mock,
                             read_mock,
                             options_mock):
        now = datetime.datetime.now()
        timestamp = now - datetime.timedelta(minutes=self._weather_interval - 1)
        timestamp = timestamp.strftime('%Y,%m,%d,%H,%M')
        get_mock.return_value = timestamp
        weather = CosyWeather("Country",
                              "City",
                              "mykey",
                              self._weather_file,
                              self._weather_interval)
        weather_data = weather.get_weather()
        self.assertTrue(read_mock.call_count == 2)


    @patch('cosycar.weather.CosyWeather._save_weather')
    @patch('cosycar.weather.CosyWeather._check_weather_data')
    @patch('cosycar.weather.CosyWeather._decode_deserialize')
    @patch('configparser.ConfigParser.options')
    @patch('configparser.ConfigParser.read')
    @patch('cosycar.weather.CosyWeather._fetch_wunder_weather')
    @patch('configparser.ConfigParser.get')
    def test_fetch_from_wunder(self,
                               get_mock,
                               fetch_mock,
                               read_mock,
                               options_mock,
                               decode_mock,
                               check_mock,
                               save_mock
                           ):
        now = datetime.datetime.now()
        timestamp = now - datetime.timedelta(minutes=self._weather_interval + 1)
        timestamp = timestamp.strftime('%Y,%m,%d,%H,%M')
        get_mock.return_value = timestamp
        weather = CosyWeather("Country",
                              "City",
                              "mykey",
                              self._weather_file,
                              self._weather_interval)
        weather_json = {'current_observation': {'temp_c': 10,
                                                'wind_kph': 5}}
        decode_mock.return_value = weather_json
        weather_data = weather.get_weather()
        self.assertTrue(fetch_mock.call_count == 1)


if __name__ == '__main__':
    unittest.main()
