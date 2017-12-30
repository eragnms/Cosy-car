# -*- coding: utf-8 -*-

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

    def get_energy_table(self):
        # implement this method! Make it read information from the config
        # file. In the config file create a section for each temperature vs
        # energy table and in the heather section refer to which table that is
        # to be used for the actual heater. From that table build a dictionary
        # like dict = {'temp_1': energy_1,
        #             'temp_2': energy_2,}
        energy_table_section = self._read_energy_table()
        #print("{}: {}".format(self.heater_name, energy_table_section))
        if energy_table_section:
            config = self._read_config()
            energy_table_options = config.options(energy_table_section)
            energies = {}
            for option in energy_table_options:
                energies[option] = config.getint(energy_table_section, option)
            return energies
        else:
            return None
                

    def _read_energy_table(self):
        config = self._read_config()
        heater_section = self._find_heater_section(self.heater_name)
        if heater_section:
            return config.get(heater_section, 'energy_table')
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
        keys = list(self.energy_table.keys())
        keys = list(map(int, keys))
        max_temperature = max(keys)
        min_temperature = min(keys)
        if temperature >= max_temperature:
            temp_key = max_temperature
        elif temperature <= min_temperature:
            temp_key = min_temperature
        else:
            temp_key = min(keys, key=lambda x: abs(x - temperature))
        energy = self.energy_table[str(temp_key)]
        return energy


class Engine(Sections):
    _section_name = 'SECTION_ENGINE'
    _req_energy = {
        '11': 0,
        '10': 500,
        '5': 500,
        '4': 666,
        '3': 666,
        '2': 833,
        '1': 833,
        '0': 1000,
        '-1': 1000,
        '-2': 1166,
        '-3': 1166,
        '-4': 1330,
        '-5': 1330,
        '-6': 1500,
        '-7': 1500,
        '-8': 1660,
        '-9': 1660,
        '-10': 1830,
        '-11': 1830,
        '-12': 2000,
        '-17': 2000,
    }

    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)
        self.energy_table = self.get_energy_table()

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Engine set_heater_state")
        self.minutes_to_next_event = minutes_to_next_event
        weather = self.fetch_weather()
        self.req_energy = self.find_req_energy(weather)
        self.should_be_on()


class Compartment(Sections):
    _section_name = 'SECTION_COMPARTMENT'
    _req_energy = {
        '11': 0,
        '10': 233,
        '6': 233,
        '5': 350,
        '1': 350,
        '0': 466,
        '-1': 700,
        '-3': 700,
        '-4': 933,
        '-6': 933,
        '-7': 1166,
        '-12': 1166,
        '-13': 1400,
        '-17': 1400,
    }

    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)
        self.energy_table = self.get_energy_table()

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Compartment_heater_state")
        self.minutes_to_next_event = minutes_to_next_event
        weather = self.fetch_weather()
        self.req_energy = self.find_req_energy(weather)
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
        self.energy_table = self.get_energy_table()

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Windscreen set_heater_state")
        self.minutes_to_next_event = minutes_to_next_event
        weather = self.fetch_weather()
        self.req_energy = self.find_req_energy(weather)
        self.should_be_on()
