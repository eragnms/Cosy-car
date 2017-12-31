# -*- coding: utf-8 -*-

import unittest
import logging

from cosycar.constants import Constants


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
