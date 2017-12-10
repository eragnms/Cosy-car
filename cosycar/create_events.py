# -*- coding: utf-8 -*-

import logging
import datetime
import os

from cosycar.constants import Constants

log = logging.getLogger(__name__)

class CreateEvent():
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
        date_to_leave = "{}:{}".format(now_date, leave_at)
        date_to_leave = datetime.datetime.strptime(date_to_leave,
                                                   '%Y:%m:%d:%H:%M')
        if (date_to_leave <= now):
            date_to_leave = date_to_leave + datetime.timedelta(days=1)
        with open(Constants.time_to_leave_file, 'w') as ttl_file:
            ttl_file.write(date_to_leave.strftime('%Y,%m,%d,%H,%M'))

    def delete(self):
        try:
            os.remove(Constants.time_to_leave_file)
        except:
            pass
