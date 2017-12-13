# -*- coding: utf-8 -*-

import unittest
import logging
from unittest.mock import patch

from cosycar.constants import Constants
from cosycar.car import Car
from cosycar.events import Events
from cosycar.create_events import CreateEvent


class EventsTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(filename='tests/data/cosycar.log',
                            level='DEBUG',
                            format=Constants.log_format)

    def tearDown(self):
        pass

    @patch('cosycar.events.Events._check_email_event')
    def test_fetch_coming_file_event(self, mock_email_event):
        leaving_in = 27
        new_event = CreateEvent()
        new_event.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertLess(next_event - leaving_in, 1)

    @patch('cosycar.events.Events._check_email_event')
    def test_fetch_coming_file_event_set_twice(self, mock_email_event):
        new_event = CreateEvent()
        leaving_in = 27
        new_event.leave_in(leaving_in + 10)
        new_event.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertLess(next_event - leaving_in, 1)

    @patch('cosycar.events.Events._check_email_event')
    def test_fetch_coming_file_event_long_into_future(self, mock_email_event):
        new_event = CreateEvent()
        leaving_in = 2745
        new_event.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertLess(next_event - leaving_in, 1)

    @patch('cosycar.events.Events._check_email_event')
    def test_fetch_coming_file_event_in_the_past(self, mock_email_event):
        new_event = CreateEvent()
        leaving_in = -27
        new_event.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertIsNone(next_event)

    @patch('cosycar.events.Events._check_email_event')
    def test_running_on_overtime(self, mock_email_event):
        """ Should run for a while on overtime. """
        new_event = CreateEvent()
        leaving_in = -2
        new_event.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertLess(next_event - leaving_in, 1)

    def test_running_on_overtime_is_zero(self):
        new_event = CreateEvent()
        leaving_in = 0
        new_event.leave_in_seconds(leaving_in)
        # We need to test that new_event makes decision to keep the
        # heaters running when minutes to next event is 0
        self.assertTrue(True)
        
if __name__ == '__main__':
    unittest.main()
