# -*- coding: utf-8 -*-

import unittest
import logging
from unittest.mock import mock_open, patch
import datetime

from cosycar.create_events import CreateEvent
from cosycar.constants import Constants

class CreateEventTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='tests/data/cosycar.log',
            level='DEBUG',
            format=Constants.log_format)

    def tearDown(self):
        pass

    def test_leave_in(self):
        new_event = CreateEvent()
        now = datetime.datetime.now()
        leave_in_minutes = 13
        leave_in_date = now + datetime.timedelta(minutes=leave_in_minutes)
        m = mock_open()
        with patch('builtins.open', m, create=True):
            new_event.leave_in(leave_in_minutes)
        handle = m()
        ans = leave_in_date.strftime('%Y,%m,%d,%H,%M')
        handle.write.assert_called_once_with(ans)


    def test_leave_in_seconds(self):
        """ This one might fail when seconds wrap over to a
        minute, while it get truncated away in the file, not
        using a resultion higher than minutes """
        new_event = CreateEvent()
        now = datetime.datetime.now()
        leave_in_seconds = 125
        leave_in_date = now + datetime.timedelta(seconds=leave_in_seconds)
        m = mock_open()
        with patch('builtins.open', m, create=True):
            new_event.leave_in_seconds(leave_in_seconds)
        handle = m()
        ans = leave_in_date.strftime('%Y,%m,%d,%H,%M')
        handle.write.assert_called_once_with(ans)


    def test_leave_at(self):
        now = datetime.datetime.now()
        two_hours_back = now - datetime.timedelta(hours=2)
        one_day_forward = two_hours_back + datetime.timedelta(days=1)
        m = mock_open()
        new_event = CreateEvent()
        with patch('builtins.open', m, create=True):
            new_event.leave_at(two_hours_back.strftime('%H:%M'))
        handle = m()
        ans = one_day_forward.strftime('%Y,%m,%d,%H,%M')
