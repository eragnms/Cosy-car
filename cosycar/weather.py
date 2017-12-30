# -*- coding: utf-8 -*-

"""
Will read the current weather information for ''location'' from wunderground
"""

import urllib3
import json
import logging
import datetime
import configparser
import os

log = logging.getLogger(__name__)


class CosyWeatherError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CosyWeather():
    """ Will read the weather from Wunderground """

    def __init__(self, country, city, wunder_key, weather_file, interval):
        self._country = country
        self._city = city
        self._wunder_key = wunder_key
        self._weather_file = weather_file
        self._interval = interval

    def get_weather(self):
        """
        Avilable keys in json  are: weather, temp_c, pressure_mb,
        wind_kph, wind_dir, relative_humidity, dewpoint_c, windchill_c,
        precip_today_metric, feelslike_c
        """
        weather_data = {}
        if self._should_fetch_from_wunder():
            weather_url = self._build_weather_url()
            weather = self._fetch_wunder_weather(weather_url)
            weather_json = self._decode_deserialize(weather)
            self._check_weather_data(weather_json)
            temp = weather_json['current_observation']['temp_c']
            weather_data['temperature'] = temp
            wind_speed = weather_json['current_observation']['wind_kph']
            weather_data['wind_speed'] = wind_speed
            self._save_weather(weather_data)
        else:
            config = configparser.ConfigParser()
            config.read(self._weather_file)
            weather_infos = config.options('WEATHER_DATA')
            for info in weather_infos:
                weather_data[info] = config.getfloat('WEATHER_DATA', info)
        return weather_data

    def _should_fetch_from_wunder(self):
        config = configparser.ConfigParser()
        if os.path.isfile(self._weather_file):
            config.read(self._weather_file)
            timestamp = str(config.get('TIME_STAMP', 'saved_on'))
            now = datetime.datetime.now()
            weather_timestamp = datetime.datetime.strptime(timestamp,
                                                           '%Y,%m,%d,%H,%M')
            delta = now - weather_timestamp
            minutes_since_timestamp = round(delta.seconds / 60)
            if minutes_since_timestamp > self._interval:
                return True
            else:
                return False
        else:
            return True

    def _save_weather(self, weather):
        """
        weather: should be a dictionary with eg
        weather = {'temperature': 10} 
        """
        now = datetime.datetime.now()
        config = configparser.ConfigParser()
        config['TIME_STAMP'] = {'saved_on': now.strftime('%Y,%m,%d,%H,%M')}
        config['WEATHER_DATA'] = {}
        for key, value in weather.items():
            config['WEATHER_DATA'][key] = str(value)
        with open(self._weather_file, 'w') as configfile:
            config.write(configfile)

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
            raise CosyWeatherError('Must not use åäö in location')
        except urllib3.exceptions.MaxRetryError:
            raise CosyWeatherError('Too many weather fetches')
        return f

    def _decode_deserialize(self, f):
        return json.loads(f.data.decode('utf-8'))

    def _check_weather_data(self, parsed_json):
        try:
            country = parsed_json['location']['country_name']
            city = parsed_json['location']['city']
        except KeyError:
            error_text = 'Keys not found: ' + self._country + '/' + self._city
            raise CosyWeatherError(error_text)
        if self._is_location_not_ok(country, city):
            error_text = 'Wrong location: ' + self._country + '/' + self._city
            raise CosyWeatherError(error_text)

    def _is_location_not_ok(self, country, city):
        if (country != self._country) or (city != self._city):
            return True
        else:
            return False

if __name__ == '__main__':
    weather = CosyWeather("Sweden",
                         "Huddinge",
                         "",
                         "/tmp/cosycar_weather.txt",
                         15)
    #weather_json = weather.get_weather()
    #temperature = weather_json['current_observation']['temp_c']
    #wind_speed = weather_json['current_observation']['wind_kph']
    #print("Temperature: {} C".format(temperature))
    #print("Wind speed: {} kph".format(wind_speed))
    weather_data = {}
    weather_data['temperature'] = 10
    weather_data['wind_speed'] = 5
    weather.save_weather(weather_data)
