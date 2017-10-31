# -*- coding: utf-8 -*-

import unittest
import logging

from cosycar.constants import Constants
from cosycar.sections import Sections


class CarTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='tests/data/cosycar.log',
            level='DEBUG',
            format=Constants.log_format)

    def tearDown(self):
        pass

    def test_check_in_use(self):
        sections = Sections()
        in_use = sections.check_in_use('SECTION_ENGINE')
        here mock the config.getboolean method...
        self.assertFalse(in_use)

    def test_check_heater_name(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
