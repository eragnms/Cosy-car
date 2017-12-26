# -*- coding: utf-8 -*-

import unittest
import logging
from unittest.mock import patch
import configparser

from cosycar.constants import Constants
from cosycar.sections import Sections
from cosycar.sections import Engine
from cosycar.sections import Compartment
from cosycar.sections import Windscreen

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

    def test_find_required_energy_engine_1(self):
        section = Engine()
        weather = {'temperature': 10} 
        energy = section.find_req_energy(weather)
        self.assertEqual(energy, 500)

    def test_find_required_energy_engine_2(self):
        section = Engine()
        weather = {'temperature': 1} 
        energy = section.find_req_energy(weather)
        self.assertEqual(energy, 600)

    def test_find_required_energy_compartment_1(self):
        section = Compartment()
        weather = {'temperature': 10} 
        energy = section.find_req_energy(weather)
        self.assertEqual(energy, 500)

    def test_find_required_energy_windscreen_1(self):
        section = Windscreen()
        weather = {'temperature': 10} 
        energy = section.find_req_energy(weather)
        self.assertEqual(energy, 500)

    @patch('cosycar.zwave.Switch')
    @patch('cosycar.zwave.Switch.is_on')
    @patch('cosycar.zwave.Switch.turn_off')
    @patch('cosycar.zwave.Switch.turn_on')
    def test_should_be_on_currently_off(self,
                                        mock_turn_off,
                                        mock_turn_on,
                                        mock_is_on,
                                        switch_mock,
                                    ):
        section = Engine()
        section.minutes_to_next_event = 10        
        section.req_energy = 100
        section.heater_power = 200
        mock_is_on.return_value = False
        switch_should_be_on = section.should_be_on()
        self.assertTrue(switch_should_be_on)

    @patch('cosycar.zwave.Switch')
    @patch('cosycar.zwave.Switch.is_on')
    @patch('cosycar.zwave.Switch.turn_off')
    @patch('cosycar.zwave.Switch.turn_on')
    def test_should_be_on_currently_on(self,
                                       mock_turn_off,
                                       mock_turn_on,
                                       mock_is_on,
                                       switch_mock,
                                   ):
        section = Engine()
        section.minutes_to_next_event = 10        
        section.req_energy = 100
        section.heater_power = 200
        mock_is_on.return_value = True
        switch_should_be_on = section.should_be_on()
        self.assertTrue(switch_should_be_on)

    @patch('cosycar.zwave.Switch')
    @patch('cosycar.zwave.Switch.is_on')
    @patch('cosycar.zwave.Switch.turn_off')
    @patch('cosycar.zwave.Switch.turn_on')
    def test_should_be_off_currently_on(self,
                                        mock_turn_off,
                                        mock_turn_on,
                                        mock_is_on,
                                        switch_mock,
                                    ):
        section = Engine()
        section.minutes_to_next_event = 40        
        section.req_energy = 100
        section.heater_power = 200
        mock_is_on.return_value = True
        switch_should_be_on = section.should_be_on()
        self.assertFalse(switch_should_be_on)


if __name__ == '__main__':
    unittest.main()
