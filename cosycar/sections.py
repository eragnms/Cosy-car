# -*- coding: utf-8 -*-

import logging
import urllib.request
import configparser

from cosycar.constants import Constants

log = logging.getLogger(__name__)

class Sections():
    def __init__(self):
        config = self._read_config()
        self.ip_address = config.get('ZWAVE_CONTROLLER', 'ip_address')
        self.port = config.get('ZWAVE_CONTROLLER', 'port')

    def available_sections(self):
        available_sections = [Engine(),
                              Compartment(),
                              Windscreen()]
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

    def switch_on(self, zwave_id):
        self._switch(zwave_id, 1)

    def switch_off(self, zwave_id):
        self._switch(zwave_id, 0)

    def _switch(self, zwave_id, on_off):
        switch_command = 'http://{}:{}'.format(self.ip_address, self.port)
        switch_command += '/data_request?id=action&output_format=xml&Devic'
        switch_command += 'eNum={}'.format(zwave_id)
        switch_command += '&serviceId=urn:upnp-org:serviceId:SwitchPower1'
        switch_command += '&action=SetTarget&newTargetValue={}'.format(on_off)
        print(switch_command)
        r = urllib.request.Request(switch_command)

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
    
class Engine(Sections):
    _section_name = 'SECTION_ENGINE'
    _required_energy = 500
    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name) 
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)

    def set_heater_state(self, minutes_to_next_event):
        time_to_run = self._required_energy / self.heater_power
        minutes_to_run = time_to_run * 60
        if minutes_to_run >= minutes_to_next_event:
            self.switch_on(self.heater_zwave_id)
        else:
            self.switch_off(self.heater_zwave_id)
        
class Compartment(Sections):
    _section_name = 'SECTION_COMPARTMENT'
    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name) 
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)
        
    def set_heater_state(self, minutes_to_next_event):
        time_to_run = self._required_energy / self.heater_power
        minutes_to_run = time_to_run * 60
        if minutes_to_run >= minutes_to_next_event:
            self.switch_on(self.heater_zwave_id)
        else:
            self.switch_off(self.heater_zwave_id)
        
class Windscreen(Sections):
    _section_name = 'SECTION_WINDSCREEN'
    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name) 
        self.heater_name = self.get_heater_name(self._section_name)
        self.heater_power = self.get_heater_power(self.heater_name)
        self.heater_zwave_id = self.get_heater_zwave_id(self.heater_name)
        
    def set_heater_state(self, minutes_to_next_event):
        time_to_run = self._required_energy / self.heater_power
        minutes_to_run = time_to_run * 60
        if minutes_to_run >= minutes_to_next_event:
            self.switch_on(self.heater_zwave_id)
        else:
            self.switch_off(self.heater_zwave_id)
