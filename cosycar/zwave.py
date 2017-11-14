# -*- coding: utf-8 -*-

import pyvera
import logging

from cosycar.constants import Constants

log = logging.getLogger(__name__)

class Zwave():
    def __init__(self):
        # ask Vera for all its devices
        # map device num to zwave id in dictionary
        pass
        
class Switch(Zwave):
    def __init__(self, zwave_id):
        super().__init__()
        self.zwave_id = zwave_id

    def turn_on(self):
        pass

    def turn_off(self):
        pass
