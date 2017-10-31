# -*- coding: utf-8 -*-

import logging
import datetime
import configparser

from cosycar.constants import Constants
from cosycar.events import Events
from cosycar.sections import Engine, Sections

log = logging.getLogger(__name__)

class Car():
    def __init__(self):
        self._sections = Sections()
    
    def leave_in(self, leave_in_minutes):
        now = datetime.datetime.now()
        date_to_leave = now + datetime.timedelta(minutes=leave_in_minutes)
        with open(Constants.time_to_leave_file, 'w') as ttl_file:
            ttl_file.write(date_to_leave.strftime('%Y,%m,%d,%H,%M'))

    def check_heaters(self):
        events = Events()
        minutes_to_next_event = events.fetch_next_event()
        # should any heaters be running
        #continue here, with should any heaters be running
        # switch heaters
        sections = Sections()
        available_sections = sections.available_sections()
        for section in available_sections:
            print(section.in_use)
        
        
        
