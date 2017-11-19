# -*- coding: utf-8 -*-

import unittest
import logging
from unittest.mock import patch
import configparser

from cosycar.constants import Constants
from cosycar.sections import Sections

CFG_FILE = 'tests/data/cosycar_template.cfg'


class CarSectionTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='tests/data/cosycar.log',
            level='DEBUG',
            format=Constants.log_format)
        self._config = configparser.ConfigParser()
        self._config.read(CFG_FILE)

    def tearDown(self):
        pass

    @patch('configparser.ConfigParser.getboolean')
    def test_check_in_use(self, getboolean_mock):
        sections = Sections()
        section = 'SECTION_ENGINE'
        sections.check_in_use(section)
        getboolean_mock.assert_any_call(section, 'in_use')

    @patch('configparser.ConfigParser.get')
    def test_get_heater_name(self, get_mock):
        sections = Sections()
        section = 'SECTION_ENGINE'
        sections.get_heater_name(section)
        get_mock.assert_any_call(section, 'heater')

    @patch('cosycar.sections.Sections._read_config')
    def test_get_heaterdata(self, read_config_mock):
        read_config_mock.return_value = self._config
        sections = Sections()
        heater_name = '"block_heater"'
        power = sections.get_heater_power(heater_name)
        self.assertEqual(power, 1000)

    @patch('cosycar.sections.Sections._read_config')
    def test_get_heater_power_2(self, read_config_mock):
        read_config_mock.return_value = self._config
        sections = Sections()
        heater_name = '"compartment_heater_1"'
        power = sections.get_heater_power(heater_name)
        self.assertEqual(power, 1500)

    @patch('cosycar.sections.Sections._read_config')
    def test_get_heater_zwave_id(self, read_config_mock):
        read_config_mock.return_value = self._config
        sections = Sections()
        heater_name = '"compartment_heater_1"'
        zwave_id = sections.get_heater_zwave_id(heater_name)
        self.assertEqual(zwave_id, 14)

    @patch('cosycar.sections.Sections._read_config')
    def test_get_heater_zwave_id_2(self, read_config_mock):
        read_config_mock.return_value = self._config
        sections = Sections()
        heater_name = '"block_heater"'
        zwave_id = sections.get_heater_zwave_id(heater_name)
        self.assertEqual(zwave_id, 21)

    @patch('cosycar.sections.Sections._read_config')
    def test_get_heater_zwave_id_none(self, read_config_mock):
        read_config_mock.return_value = self._config
        sections = Sections()
        heater_name = '"compartment_heater_111"'
        zwave_id = sections.get_heater_zwave_id(heater_name)
        self.assertIsNone(zwave_id)


if __name__ == '__main__':
    unittest.main()
