# -*- coding: utf-8 -*-

import unittest
import logging
import datetime
from unittest.mock import patch
import pyvera

from cosycar.constants import Constants
from cosycar.zwave import Zwave, Switch


class ZwaveTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='tests/data/cosycar.log',
            level='DEBUG',
            format=Constants.log_format)
               
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
