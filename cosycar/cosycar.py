# -*- coding: utf-8 -*-

from .calendar_events import CalendarEvents
from pkg_resources import Requirement, resource_filename
import os

# On = http://$ip_address:3480/data_request?id=action&output_format
# =xml&DeviceNum=$my_id&serviceId=urn:upnp-org:serviceId:SwitchPowe
# r1&action=SetTarget&newTargetValue=1
# Off = http://$ip_address:3480/data_request?id=action&output_forma
# t=xml&DeviceNum=$my_id&serviceId=urn:upnp-org:serviceId:SwitchPow
# er1&action=SetTarget&newTargetValue=0


# Version numbering scheme, see
# https://packaging.python.org/distributing/#choosing-a-versioning-scheme
# 1.2.0.dev1  # Development release
# 1.2.0a1     # Alpha Release
# 1.2.0b1     # Beta Release
# 1.2.0rc1    # Release Candidate
# 1.2.0       # Final Release
# 1.2.0.post1 # Post Release
__version__ = '0.0.1.dev11'


def main():
    print('Hello world!')
    print(__version__)
    print('The config file is in {}/.config'.format(os.environ['HOME']))


if __name__ == "__main__":
    main()
