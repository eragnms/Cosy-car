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

    def leave_in_seconds(self, leave_in_seconds):
        log.debug("Running leave in seconds: {}".format(leave_in_seconds))
        now = datetime.datetime.now()
        date_to_leave = now + datetime.timedelta(seconds=leave_in_seconds)
        with open(Constants.time_to_leave_file, 'w') as ttl_file:
            ttl_file.write(date_to_leave.strftime('%Y,%m,%d,%H,%M'))

    def leave_at(self, leave_at):
        now = datetime.datetime.now()
        now_date = now.strftime('%Y:%m:%d')
        date_to_leave =  "{}:{}".format(now_date, leave_at)
        date_to_leave = datetime.datetime.strptime(date_to_leave,
                                                   '%Y:%m:%d:%H:%M')
        if (date_to_leave <= now):
            date_to_leave = date_to_leave - datetime.timedelta(days=1)
        with open(Constants.time_to_leave_file, 'w') as ttl_file:
            ttl_file.write(date_to_leave.strftime('%Y,%m,%d,%H,%M'))
        
            
    def check_heaters(self):
        events = Events()
        minutes_to_next_event = events.fetch_next_event()
        log.debug("Checking heaters: {}".format(minutes_to_next_event))
        log.debug("Next event in: {}".format(minutes_to_next_event))
        sections = Sections()
        available_sections = sections.available_sections()
        log.debug("sections: {}".format(available_sections))
        for section in available_sections:
            log.debug("Checking section: {}".format(section))
            section.set_heater_state(minutes_to_next_event)
        
        
        
