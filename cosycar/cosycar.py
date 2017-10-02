# -*- coding: utf-8 -*-

import pkg_resources

from .calendar_events import CalendarEvents

# Version numbering scheme, see
# https://packaging.python.org/distributing/#choosing-a-versioning-scheme
# 1.2.0.dev1  # Development release
# 1.2.0a1     # Alpha Release
# 1.2.0b1     # Beta Release
# 1.2.0rc1    # Release Candidate
# 1.2.0       # Final Release
# 1.2.0.post1 # Post Release
__version__ = '0.0.1.dev2'


def main():
    print('Hello world!')
    version = pkg_resources.get_distribution("cosycar").version
    print(version)

if __name__ == "__main__":
    main()
