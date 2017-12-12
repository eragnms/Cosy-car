# -*- coding: utf-8 -*-

"""
Will read the current weather information for ''location'' from wunderground"""

import urllib3
import json
import logging

log = logging.getLogger(__name__)


class SATWeatherError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SATWeather():
    """ Will read the weather from Wunderground """

    def __init__(self, country, city, wunder_key):
        self._country = country
        self._city = city
        self._wunder_key = wunder_key

    def get_weather(self):
        """
        To fetch temperature data from the returned json do:
            temperature = weather_json['current_observation']['temp_c']

        By replacing temp_c with other keys one can fetch more
        information. Avilable keys are: weather, temp_c, pressure_mb,
        wind_kph, wind_dir, relative_humidity, dewpoint_c, windchill_c,
        precip_today_metric, feelslike_c
        """
        weather_url = self._build_weather_url()
        weather = self._fetch_wunder_weather(weather_url)
        weather_json = self._decode_deserialize(weather)
        self._check_weather_data(weather_json)
        return weather_json

    def _build_weather_url(self):
        weather_url = 'http://api.wunderground.com/api/'
        weather_url += self._wunder_key + '/geolookup/conditions/q/'
        weather_url += self._country + '/' + self._city + '.json'
        return weather_url

    def _fetch_wunder_weather(self, url):
        try:
            http = urllib3.PoolManager()
            f = http.request('GET', url)
        except UnicodeEncodeError:
            raise SATWeatherError('Must not use åäö in location')
        except urllib3.exceptions.MaxRetryError:
            raise SATWeatherError('Too many weather fetches')
        return f

    def _decode_deserialize(self, f):
        return json.loads(f.data.decode('utf-8'))

    def _check_weather_data(self, parsed_json):
        try:
            country = parsed_json['location']['country_name']
            city = parsed_json['location']['city']
        except KeyError:
            error_text = 'Keys not found: ' + self._country + '/' + self._city
            raise SATWeatherError(error_text)
        if self._is_location_not_ok(country, city):
            error_text = 'Wrong location: ' + self._country + '/' + self._city
            raise SATWeatherError(error_text)

    def _is_location_not_ok(self, country, city):
        if (country != self._country) or (city != self._city):
            return True
        else:
            return False

if __name__ == '__main__':
    weather = SATWeather("", "", "")
    weather_json = weather.get_weather()
    temperature = weather_json['current_observation']['temp_c']
    wind_speed = weather_json['current_observation']['wind_kph']
    print("Temperature: {} C".format(temperature))
    print("Wind speed: {} kph".format(wind_speed))
