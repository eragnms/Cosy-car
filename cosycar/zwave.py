# -*- coding: utf-8 -*-

# devices
# [VeraSwitch (id=15 category=On/Off Switch name=Bookcase Uplighters), VeraSwitch (id=16 category=On/Off Switch name=Bookcase device)]
# devices[1]
# VeraSwitch (id=15 category=On/Off Switch name=Bookcase Uplighters)
# devices[1].is_switched_on()
# devices[1].switch_on()

import pyvera
import logging
import configparser
import re

from cosycar.constants import Constants

log = logging.getLogger(__name__)

class Zwave():
    def __init__(self, zwave_id):
        self.zwave_id = zwave_id
        config = configparser.ConfigParser()
        config.read(Constants.cfg_file)
        ip_address = config.get('ZWAVE_CONTROLLER', 'ip_address')
        port = config.get('ZWAVE_CONTROLLER', 'port')
        controller_address = "http://{}:{}/".format(ip_address, port)
        self._controller = pyvera.VeraController(controller_address)
        self._devices = self._controller.get_devices('On/Off Switch')
        self._mapping_id_to_ix = {}
        for index, value in enumerate(self._devices):
            zwave_id = self._get_id(value)
            self._mapping_id_to_ix[zwave_id] = index
        self._index = self._mapping_id_to_ix[self.zwave_id] 
            
    def _get_id(self, value):
        print(type(value))
        so we have the device id within reach like the below line, use that!
        print(value.device_id)
        value.replace(' ', '')
        print(value)
        p = re.compile('id=\d+')
        m = p.search(value)
        g = m.group()
        print(g)
        p = re.compile('\d+')
        m = p.search(g)
        return int(m.group())
        
    def get_mapping(self):
        return self._index
    
class Switch(Zwave):
    def __init__(self, zwave_id):
        super().__init__(zwave_id)

    def turn_on(self):
        self.devices[self._index].switch_on

    def turn_off(self):
        self.devices[self._index].switch_off
