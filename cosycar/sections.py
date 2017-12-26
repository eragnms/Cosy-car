# -*- coding: utf-8 -*-

# 1- Write testcases for method selecting energy required. Test
#   the section, mock weather check and check the energy coming out.
# 2- Once the above test cases are in place add the whole table for engine.
# 3- Use properties to build a list of available sections, see page 194 in Clean Python.
# 4- Move the tables to the config file, see example config read below.
# 5- Update the documentation and release 1.0.0

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
from cosycar.weather import CosyWeather

log = logging.getLogger(__name__)


class Sections():
    def __init__(self):
        self.minutes_to_next_event = None
        self.req_energy = 0
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
        switch_should_be_on = False 
        if self.in_use:
            switch = Switch(self.heater_zwave_id)
            currently_on = switch.is_on()
            if self._there_is_an_event():
                h_to_run_before_event = self.req_energy / self.heater_power
                minutes_to_run_before_event = h_to_run_before_event * 60
                log.debug("Checking for on/off")
                if minutes_to_run_before_event >= self.minutes_to_next_event:
                    if not currently_on:
                        log.info("Turn on: {}".format(self.heater_zwave_id))
                    switch.turn_on()
                    switch_should_be_on = True
                else:
                    if currently_on:
                        log.info("Turn off: {}".format(self.heater_zwave_id))
                    switch.turn_off()
                    switch_should_be_on = False
            else:
                if currently_on:
                    log.info("Turn off: {}".format(self.heater_zwave_id))
                switch.turn_off()
                switch_should_be_on = False
        else:
            log.debug("Section {} not in use".format(self._section_name))
        return switch_should_be_on

    def fetch_weather(self):
        local_weather = CosyWeather(self._country, self._city,
                                    self._wunder_key, Constants.weather_file,
                                    Constants.weather_interval)
        weather = local_weather.get_weather()
        return weather

    def find_req_energy(self, weather):
        energy = 0
        temperature = weather['temperature']
        keys = list(self._req_energy.keys())
        keys = list(map(int, keys))
        max_temperature = max(keys)
        min_temperature = min(keys)
        if temperature >= max_temperature:
            temp_key = max_temperature
        elif temperature <= min_temperature:
            temp_key = min_temperature
        else:
            temp_key = min(keys, key=lambda x: abs(x - temperature))
        energy = self._req_energy[str(temp_key)]
        return energy


   11 => 0,                                                                                                                                                             10 => 30,                                                                                                                                                            9 => 30,                                                                                                                                                             8 => 30,                                                                                                                                                             7 => 30,                                                                                                                                                             6 => 30,                                                                                                                                                             5 => 30,                                                                                                                                                             4 => 40,                                                                                                                                                             3 => 40,                                                                                                                                                             2 => 50,                                                                                                                                                             1 => 50,                                                                                                                                                             0 => 60,                                                                                                                                                             -1 => 60,                                                                                                                                                            -2 => 70,                                                                                                                                                            -3 => 70,                                                                                                                                                            -4 => 80,                                                                                                                                                            -5 => 80,                                                                                                                                                            -6 => 90,                                                                                                                                                            -7 => 90,                                                                                                                                                            -8 => 100,                                                                                                                                                           -9 => 100,                                                                                                                                                           -10 => 110,                                                                                                                                                          -11 => 110,                                                                                                                                                          -12 => 120,                                                                                                                                                          -13 => 120,                                                                                                                                                          -14 => 120,                                                                                                                                                          -15 => 120,                                                                                                                                                          -16 => 120,                                                                                                                                                          -17 => 120,                                                                                                                                                      );


   Compartment



        11 => 0,                                                                                                                                                             10 => 10,                                                                                                                                                            9 => 10,                                                                                                                                                             8 => 10,                                                                                                                                                             7 => 10,                                                                                                                                                             6 => 10,                                                                                                                                                             5 => 15,                                                                                                                                                             4 => 15,                                                                                                                                                             3 => 15,                                                                                                                                                             2 => 15,                                                                                                                                                             1 => 15,                                                                                                                                                             0 => 20,                                                                                                                                                             -1 => 30,                                                                                                                                                            -2 => 30,                                                                                                                                                            -3 => 30,                                                                                                                                                            -4 => 40,                                                                                                                                                            -5 => 40,                                                                                                                                                            -6 => 40,                                                                                                                                                            -7 => 50,                                                                                                                                                            -8 => 50,                                                                                                                                                            -9 => 50,                                                                                                                                                            -10 => 50,                                                                                                                                                           -11 => 50,                                                                                                                                                           -12 => 50,                                                                                                                                                           -13 => 60,                                                                                                                                                           -14 => 60,                                                                                                                                                           -15 => 60,                                                                                                                                                           -16 => 60,                                                                                                                                                           -17 => 60


    
class Engine(Sections):
    _section_name = 'SECTION_ENGINE'
    _req_energy = {
        '11': 0,
        '10': 500,
        '9': 500,
        '8': 500,
        '7': 500,
        '6': 500,
        '5': 500,
        '4': 500,
        '3': 500,
        '2': 500,
        '1': 500,
        '0': 500,
        '-1': 500,
        '-2': 500,
        '-3': 500,
        '-4': 500,
        '-5': 500,
        '-6': 500,
        '-7': 500,
        '-8': 500,
        '-9': 500,
        '-10': 500,
        '-11': 500,
        '-12': 500,
        '-13': 500,
        '-14': 500,
        '-15': 500,
        '-16': 2000,
        '-17': 2000,
    }

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
        self.req_energy = self.find_req_energy(weather)
        self.should_be_on()


class Compartment(Sections):
    _section_name = 'SECTION_COMPARTMENT'
    _req_energy = 0

    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Compartment_heater_state")
        self.minutes_to_next_event = minutes_to_next_event
        self.req_energy = self._req_energy
        self.should_be_on()


class Windscreen(Sections):
    _section_name = 'SECTION_WINDSCREEN'
    _req_energy = 700

    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Windscreen set_heater_state")
        self.minutes_to_next_event = minutes_to_next_event
        self.req_energy = self._req_energy
        self.should_be_on()
