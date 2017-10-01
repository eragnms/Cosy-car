#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# see https://softwareengineering.stackexchange.com/questions/333761/where-do-you-put-the-main-function-of-a-python-app
import pkg_resources


def main():
    print('Hello world!')
    version = pkg_resources.get_distribution("cosycar").version
    print(version)

if __name__ == "__main__":
    main()
