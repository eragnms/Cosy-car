# -*- coding: utf-8 -*-

import unittest
import logging
import datetime
from unittest.mock import mock_open, patch

from cosycar.constants import Constants
from cosycar.car import Car


class CarTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='tests/data/cosycar.log',
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
        ans = leave_in_date.strftime('%Y,%m,%d,%H,%M')
        handle.write.assert_called_once_with(ans)


    def test_leave_in_seconds(self):
        """ This one might fail when seconds wrap over to a
        minute, while it get truncated away in the file, not
        using a resultion higher than minutes """
        car = Car()
        now = datetime.datetime.now()
        leave_in_seconds = 125
        leave_in_date = now + datetime.timedelta(seconds=leave_in_seconds)
        m = mock_open()
        with patch('builtins.open', m, create=True):
            car.leave_in_seconds(leave_in_seconds)
        handle = m()
        ans = leave_in_date.strftime('%Y,%m,%d,%H,%M')
        handle.write.assert_called_once_with(ans)


    def test_leave_at(self):
        now = datetime.datetime.now()
        two_hours_back = now - datetime.timedelta(hours=2)
        one_day_forward = two_hours_back + datetime.timedelta(days=1)
        m = mock_open()
        car = Car()
        with patch('builtins.open', m, create=True):
            car.leave_at(two_hours_back.strftime('%H:%M'))
        handle = m()
        ans = one_day_forward.strftime('%Y,%m,%d,%H,%M')
        handle.write.assert_called_once_with(ans)


if __name__ == '__main__':
    unittest.main()
