# -*- coding: utf-8 -*-

from .calendar_events import CalendarEvents
from pkg_resources import Requirement, resource_filename
import os
import argparse
import logging

from cosycar.constants import Constants
from cosycar.car import Car

from cosycar.zwave import Switch 

# Off = http://$ip_address:3480/data_request?id=action&output_forma
# t=xml&DeviceNum=$my_id&serviceId=urn:upnp-org:serviceId:SwitchPow
# er1&action=SetTarget&newTargetValue=0

#     print('The config file is in {}/.config'.format(os.environ['HOME']))

# Version numbering scheme, see
# https://packaging.python.org/distributing/#choosing-a-versioning-scheme
# 1.2.0.dev1  # Development release
# 1.2.0a1     # Alpha Release
# 1.2.0b1     # Beta Release
# 1.2.0rc1    # Release Candidate
# 1.2.0       # Final Release
# 1.2.0.post1 # Post Release
__version__ = '0.0.1.dev31'


def main():
    logging.basicConfig(filename='/tmp/should_be_elsewhere.log',
                        level='DEBUG',
                        format=Constants.log_format)
    log = logging.getLogger(__name__)
    log.debug("Cosycar: {}".format(__version__))
    description_text = "Cosycar, the script that keeps your car cosy"
    parser = argparse.ArgumentParser(description=description_text)
    parser.add_argument("-c",
                        "--check_heaters",
                        help="check if any heaters should run",
                        action="store_true")
    parser.add_argument("-l",
                        "--leave_in",
                        help="leave in LEAVE_IN minutes",
                        type=int)
    parser.add_argument("-s",
                        "--leave_in_seconds",
                        help="leave in LEAVE_IN_SECONDS seconds",
                        type=int)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v",
                       "--version",
                       help="print version information",
                       action="store_true")
    group.add_argument("-t",
                       "--test",
                       help="various tests",
                       action="store_true")
    args = parser.parse_args()
    if args.check_heaters:
        car = Car()
        car.check_heaters()
    elif args.leave_in:
        car = Car()
        car.leave_in(args.leave_in)
    elif args.leave_in_seconds:
        car = Car()
        car.leave_in_seconds(args.leave_in_seconds)
    elif args.test:
        # Just for tests...
        switch = Switch(7)
        switch.turn_off()
    elif args.version:
        print('This is cosycar version: {}'.format(__version__))
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
