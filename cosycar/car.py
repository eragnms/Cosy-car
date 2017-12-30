# -*- coding: utf-8 -*-

import logging
import datetime

from cosycar.constants import Constants
from cosycar.events import Events
from cosycar.sections import Sections

log = logging.getLogger(__name__)


class Car():
    def __init__(self):
        pass

    def check_heaters(self):
        events = Events()
        minutes_to_next_event = events.fetch_next_event()
        sections = Sections("hej")
        available_sections = sections.available_sections()
        for section in available_sections:
            section.set_heater_state(minutes_to_next_event)
