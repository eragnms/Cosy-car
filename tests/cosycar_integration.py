#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class IntegrationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def setup():
    pass

def teardown():
    pass

setup()
result = os.system('cosycar >/dev/null 2>&1')
if result:
    teardown()
    raise IntegrationError('Integration test failed with: {}'.format(result))
else:
    print('Integration test OK!')
teardown()
