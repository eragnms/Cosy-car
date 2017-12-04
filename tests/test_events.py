# -*- coding: utf-8 -*-

import unittest
import logging

from cosycar.constants import Constants
from cosycar.car import Car
from cosycar.events import Events


class EventsTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(filename='tests/data/cosycar.log',
                            level='DEBUG',
                            format=Constants.log_format)

    def tearDown(self):
        pass

    def test_fetch_coming_file_event(self):
        leaving_in = 27
        car = Car()
        car.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertLess(next_event - leaving_in, 1)

    def test_fetch_coming_file_event_set_twice(self):
        car = Car()
        leaving_in = 27
        car.leave_in(leaving_in + 10)
        car.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertLess(next_event - leaving_in, 1)

    def test_fetch_coming_file_event_long_into_future(self):
        car = Car()
        leaving_in = 2745
        car.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertLess(next_event - leaving_in, 1)

    def test_fetch_coming_file_event_in_the_past(self):
        car = Car()
        leaving_in = -27
        car.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertIsNone(next_event)

    def test_running_on_overtime(self):
        """ Should run for a while on overtime. """
        car = Car()
        leaving_in = -2
        car.leave_in(leaving_in)
        events = Events()
        next_event = events.fetch_next_event()
        self.assertLess(next_event - leaving_in, 1)

    def test_running_on_overtime_is_zero(self):
        car = Car()
        leaving_in = 0
        car.leave_in_seconds(leaving_in)
        # We need to test that car makes decision to keep the
        # heaters running when minutes to next event is 0
        self.assertTrue(True)
        
if __name__ == '__main__':
    unittest.main()
