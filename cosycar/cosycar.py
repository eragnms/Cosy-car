# -*- coding: utf-8 -*-

import pkg_resources

from .calendar_events import CalendarEvents

def main():
    print('Hello world!')
    version = pkg_resources.get_distribution("cosycar").version
    print(version)

if __name__ == "__main__":
    main()
