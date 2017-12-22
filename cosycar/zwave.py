# -*- coding: utf-8 -*-

import pyvera
import logging
import configparser

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
        log.debug("Controller: {}".format(controller_address))
        self._controller = pyvera.VeraController(controller_address)
        self._devices = self._controller.get_devices('On/Off Switch')
        self._mapping_id_to_ix = {}
        for index, value in enumerate(self._devices):
            self._mapping_id_to_ix[value.device_id] = index
        self._index = self._mapping_id_to_ix[self.zwave_id]
        log.debug("ix: {}, id: {}".format(self._index, self.zwave_id))

    def get_mapping(self):
        return self._index


class Switch(Zwave):
    def __init__(self, zwave_id):
        super().__init__(zwave_id)

    def turn_on(self):
        log.debug("Switching on: {}".format(self.zwave_id))
        self._devices[self._index].switch_on()

    def turn_off(self):
        log.debug("Switching off: {}".format(self.zwave_id))
        self._devices[self._index].switch_off()

    def is_on(self):
        is_on = self._devices[self._index].is_switched_on()
        log.debug("Switch {} is on: {}".format(self.zwave_id, is_on))
        return is_on
