# -*- coding: utf-8 -*-

# - Reduce the rate with which we read weather data from wunder. Write read data to a file when fetched, and stamp it with 
#   a timestamp. If the timestamp is older than X then read new data from wunder. Store the weather data in a configparser 
#   file to make it easy to write and parse.
# - Move the tables to the config file, see example config read below.
# - Write testcases for method selecting energy required. Test the section, mock weather check and check the energy coming out.
# - Once the above test cases are in place add the whole table for engine.
# - Update the documentation and release 1.0.0

# >>> config.read('example.ini')
# ['example.ini']
# >>> config.sections()
# ['bitbucket.org', 'topsecret.server.com']
# >>> 'bitbucket.org' in config
# True
# >>> topsecret = config['topsecret.server.com']
# >>> topsecret['ForwardX11']


import logging
import configparser

from cosycar.constants import Constants
from cosycar.zwave import Switch
from cosycar.weather import SATWeather

log = logging.getLogger(__name__)


class Sections():
    def __init__(self):
        self.minutes_to_next_event = None
        self.required_energy = 0
        config = self._read_config()
        self._country = config.get('WUNDER_WEATHER', 'country')
        self._city = config.get('WUNDER_WEATHER', 'city')
        self._wunder_key = config.get('WUNDER_WEATHER', 'wunder_key')
    
    def available_sections(self):
        available_sections = [Engine(), Compartment(), Windscreen()]
        return available_sections

    def check_in_use(self, section):
        config = self._read_config()
        return config.getboolean(section, 'in_use')

    def get_heater_name(self, section):
        config = self._read_config()
        return config.get(section, 'heater')

    def get_heater_power(self, heater_name):
        config = self._read_config()
        heater_section = self._find_heater_section(heater_name)
        if heater_section:
            return config.getint(heater_section, 'power')
        else:
            return None

    def get_heater_zwave_id(self, heater_name):
        config = self._read_config()
        heater_section = self._find_heater_section(heater_name)
        if heater_section:
            return config.getint(heater_section, 'zwave_id')
        else:
            return None

    def _find_heater_section(self, heater_name):
        config = self._read_config()
        sections = config.sections()
        for section in sections:
            items = config.items(section)
            for item, value in items:
                if item == 'heater_name' and value == heater_name:
                    return section
        return None

    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(Constants.cfg_file)
        return config

    def _there_is_an_event(self):
        return self.minutes_to_next_event is not None

    def should_be_on(self):
        if self.in_use:
            switch = Switch(self.heater_zwave_id)
            currently_on = switch.is_on()
            if self._there_is_an_event():
                h_to_run_before_event = self.required_energy / self.heater_power
                minutes_to_run_before_event = h_to_run_before_event * 60
                log.debug("Checking for on/off")
                if minutes_to_run_before_event >= self.minutes_to_next_event:
                    if not currently_on:
                        log.info("Turn switch on: {}".format(self.heater_zwave_id))
                    switch.turn_on()
                else:
                    if currently_on:
                        log.info("Turn switch off: {}".format(self.heater_zwave_id))
                    switch.turn_off()
            else:
                if currently_on:
                    log.info("Turn switch off: {}".format(self.heater_zwave_id))
                switch.turn_off()        
        else:
            log.debug("Section {} not in use".format(self._section_name))
            
    def fetch_weather(self):
        local_weather = SATWeather(self._country, self._city, self._wunder_key)
        weather_json = local_weather.get_weather()
        weather = {}
        weather['temperature'] = weather_json['current_observation']['temp_c']
        weather['wind_speed'] = weather_json['current_observation']['wind_kph']
        return weather

    def find_required_energy(self, weather):
        energy = 0
        temperature = weather['temperature']
        keys = list(self._required_energy.keys())
        keys = list(map(int, keys))
        max_temperature = max(keys)
        min_temperature = min(keys)
        if temperature >= max_temperature:
            temp_key = max_temperature
        elif temperature <= min_temperature:
            temp_key = min_temperature
        else:
            temp_key = min(keys, key=lambda x:abs(x-temperature))
        energy = self._required_energy[str(temp_key)]
        return energy
            
    
class Engine(Sections):
    _section_name = 'SECTION_ENGINE'
    _required_energy = {'11': 0,
                        '10': 500,
                        '-16': 2000,
                        '-17': 2000,}

    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Engine set_heater_state")
        self.minutes_to_next_event = minutes_to_next_event
        weather = self.fetch_weather()
        self.required_energy = self.find_required_energy(weather)
        self.should_be_on()


class Compartment(Sections):
    _section_name = 'SECTION_COMPARTMENT'
    _required_energy = 0

    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Compartment_heater_state")
        self.minutes_to_next_event = minutes_to_next_event
        self.required_energy = self._required_energy
        self.should_be_on()


class Windscreen(Sections):
    _section_name = 'SECTION_WINDSCREEN'
    _required_energy = 700

    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Windscreen set_heater_state")
        self.minutes_to_next_event = minutes_to_next_event
        self.required_energy = self._required_energy
        self.should_be_on()



