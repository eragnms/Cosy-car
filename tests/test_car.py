# -*- coding: utf-8 -*-

import unittest
import logging
import datetime
from unittest.mock import mock_open, patch

from cosycar.constants import Constants
from cosycar.car import Car


class CarTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(filename='tests/data/cosycar.log',
                            level='DEBUG',
                            format=Constants.log_format)

    def tearDown(self):
        pass

    def test_leave_in(self):
        car = Car()
        now = datetime.datetime.now()
        leave_in_minutes = 13
        leave_in_date = now + datetime.timedelta(minutes=leave_in_minutes)
        m = mock_open()
        with patch('builtins.open', m, create=True):
            car.leave_in(leave_in_minutes)
        handle = m()
        ans = leave_in_date.strftime('%Y-%m-%d,%H:%M')
        handle.write.assert_called_once_with(ans)
        
if __name__ == '__main__':
    unittest.main()
