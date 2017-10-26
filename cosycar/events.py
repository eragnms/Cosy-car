# -*- coding: utf-8 -*-

import logging
import os
import datetime
from datetime import timedelta

from cosycar.constants import Constants

log = logging.getLogger(__name__)

class Events():
    def fetch_next_event(self):
        minutes_to_file_event = self._minutes_to_file_event()
        minutes_to_cal_event = None
        minutes_to_next_event = self._pick_time_to_use(minutes_to_cal_event,
                                                       minutes_to_file_event)
        return minutes_to_next_event
        
    def _pick_time_to_use(self, event_1, event_2):
        if event_1 and event_2:
            time_to_use = min(event_1, event_2)
        elif event_1:
            time_to_use = event_1
        elif event_2:
            time_to_use = event_2
        else:
            time_to_use = None
        return time_to_use

    def _minutes_to_file_event(self):
        minutes_to_file_event = None
        event = self._file_event()
        if event:
            now = datetime.datetime.now()
            delta = event - now
            minutes_to_file_event = delta.seconds / 60
            minutes_to_file_event += delta.days * 24 * 60
            if minutes_to_file_event < 0:
                minutes_to_file_event = None
        return minutes_to_file_event
        
    def _file_event(self):
        event = None
        file_name = Constants.time_to_leave_file
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r') as file:
                    for line in file:
                        time_pieces = line.split(",")
                event = datetime.datetime(year=int(time_pieces[0]),
                                          month=int(time_pieces[1]),
                                          day=int(time_pieces[2]),
                                          hour=int(time_pieces[3]),
                                          minute=int(time_pieces[4]))
            except:
                text = "Event file {} exists, but no time to leave info "
                text += "could be extracted"
                log.warning(text.format(file_name))
        return event
