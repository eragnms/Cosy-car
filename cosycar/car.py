# -*- coding: utf-8 -*-

import logging
import datetime

from cosycar.constants import Constants

log = logging.getLogger(__name__)

class Car():
    def leave_in(self, leave_in_minutes):
        now = datetime.datetime.now()
        date_to_leave = now + datetime.timedelta(minutes=leave_in_minutes)
        with open(Constants.time_to_leave_file, 'w') as ttl_file:
            ttl_file.write(date_to_leave.strftime('%Y-%m-%d,%H:%M'))
