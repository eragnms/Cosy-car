# -*- coding: utf-8 -*-

import logging
import configparser

from cosycar.constants import Constants
from cosycar.zwave import Switch

log = logging.getLogger(__name__)


class Sections():
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

    def _there_is_an_event(self, minutes_to_next_event):
        return minutes_to_next_event is not None


class Engine(Sections):
    _section_name = 'SECTION_ENGINE'
    _required_energy = 700

    def __init__(self):
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Engine set_heater_state")
        switch = Switch(self.heater_zwave_id)
        if self._there_is_an_event(minutes_to_next_event):
            h_to_run_before_event = self._required_energy / self.heater_power
            minutes_to_run_before_event = h_to_run_before_event * 60
            log.debug("Checking for on/off")
            if minutes_to_run_before_event >= minutes_to_next_event:
                log.info("Turn switch on: {}".format(self.heater_zwave_id))
                switch.turn_on()
            else:
                log.info("Turn switch off: {}".format(self.heater_zwave_id))
                switch.turn_off()
        else:
            log.info("Turn switch off: {}".format(self.heater_zwave_id))
            switch.turn_off()


class Compartment(Sections):
    _section_name = 'SECTION_COMPARTMENT'

    def __init__(self):
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Compartment set_heater_state")
        pass


class Windscreen(Sections):
    _section_name = 'SECTION_WINDSCREEN'
    _required_energy = 700

    def __init__(self):
        self.in_use = self.check_in_use(self._section_name)
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)

    def set_heater_state(self, minutes_to_next_event):
        log.debug("Windscreen set_heater_state")
        switch = Switch(self.heater_zwave_id)
        if self._there_is_an_event(minutes_to_next_event):
            h_to_run_before_event = self._required_energy / self.heater_power
            minutes_to_run_before_event = h_to_run_before_event * 60
            log.debug("Checking for on/off")
            if minutes_to_run_before_event >= minutes_to_next_event:
                log.info("Turn switch on: {}".format(self.heater_zwave_id))
                switch.turn_on()
            else:
                log.info("Turn switch off: {}".format(self.heater_zwave_id))
                switch.turn_off()
        else:
            log.info("Turn switch off: {}".format(self.heater_zwave_id))
            switch.turn_off()
