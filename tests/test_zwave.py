# -*- coding: utf-8 -*-

import unittest
import logging
import datetime
from unittest.mock import patch

from cosycar.constants import Constants
from cosycar.zwave import Zwave, Switch


class ZwaveTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='tests/data/cosycar.log',
            level='DEBUG',
            format=Constants.log_format)
        self._device_mock = ['VeraSwitch (id=3 category=On/Off Switch name=Lampa i fönster)', 'VeraSwitch (id=445 category=On/Off Switch name=Lampa bokhylla)', 'VeraSwitch (id=5 category=On/Off Switch name=Lampa vid sekretär)', 'VeraSwitch (id=6 category=On/Off Switch name=Lampa i fönster 1)']
        
    def tearDown(self):
        pass

    @patch('pyvera.VeraController.get_devices')
    def test_device_mapping_in_init_1(self,
                                    get_devices_mock):
        
        get_devices_mock.return_value = self._device_mock
        switch = Switch(445)
        mapping = switch.get_mapping()
        self.assertEqual(mapping, 1)

    @patch('pyvera.VeraController.get_devices')
    def test_device_mapping_in_init_2(self,
                                    get_devices_mock):
        
        get_devices_mock.return_value = self._device_mock
        switch = Switch(3)
        mapping = switch.get_mapping()
        self.assertEqual(mapping, 0)
        
if __name__ == '__main__':
    unittest.main()
