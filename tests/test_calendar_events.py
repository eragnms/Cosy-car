# -*- coding: utf-8 -*-

import unittest
import logging

from cosycar.calendar_events import CalendarEvents

class CalendarEventsTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            filename='tests/data/cosycar.log',
            level='DEBUG',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def tearDown(self):
        pass

    def test_instance_of_calendar_Event(self):
        events = CalendarEvents()
        self.assertIsInstance(events, CalendarEvents)
        
    def test_add_more_tests(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
