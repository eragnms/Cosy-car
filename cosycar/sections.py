# -*- coding: utf-8 -*-

import logging

from cosycar.constants import Constants
import configparser

log = logging.getLogger(__name__)

class Sections():
    def __init__(self):
        pass

    def available_sections(self):
        available_sections = [Engine(),
                              Compartment(),
                              Windscreen()]
        return available_sections
    
    def check_in_use(self, section):
        config = self._read_config()
        return config.getboolean(section, 'in_use')

    def check_heater_name(self, section):
        config = self._read_config()
        return config.get(section, 'heater')
                            
    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(Constants.cfg_file)
        return config
    
class Engine(Sections):
    _section_name = 'SECTION_ENGINE'
    def __init__(self):
        super().__init__()
        self.in_use = self.check_in_use(self._section_name) 
        self.heater_name = check_heater_name(self._section_name)
        # make unittests pass
        # instanciate a heater and let its init set pwr, id
        
class Compartment():
    def __init__(self):
        self.in_use = False


class Windscreen():
    def __init__(self):
        self.in_use = False
    
