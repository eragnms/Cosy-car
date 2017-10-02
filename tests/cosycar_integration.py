#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

def setup():
    pass

def teardown():
    pass

setup()
result = os.system('./cosycar-runner.py >/dev/null 2>&1')
if result:
    print('Integration test failed!')
else:
    print('Integration test OK!')
teardown()
