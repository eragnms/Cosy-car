# -*- coding: utf-8 -*-

import logging
import datetime
import configparser

from cosycar.constants import Constants
from cosycar.events import Events
from cosycar.sections import Sections

log = logging.getLogger(__name__)

class Car():
    def __init__(self):
        self._sections = Sections()
    
    def leave_in(self, leave_in_minutes):
        log.debug("Running leave in minutes: {}".format(leave_in_minutes))
        now = datetime.datetime.now()
        date_to_leave = now + datetime.timedelta(minutes=leave_in_minutes)
        with open(Constants.time_to_leave_file, 'w') as ttl_file:
            ttl_file.write(date_to_leave.strftime('%Y,%m,%d,%H,%M'))

    def check_heaters(self):
        events = Events()
        minutes_to_next_event = events.fetch_next_event()
        if minutes_to_next_event:
            log_text = "Minutes to next event: {}"
            sections = Sections()
            available_sections = sections.available_sections()
            log.debug("sections: {}".format(available_sections))
            for section in available_sections:
                log.debug("section: {}".format(section))
                section.set_heater_state(minutes_to_next_event)
        
        
        
