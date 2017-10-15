#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time

PORT = 8085
HTTP_LOG_FILE = 'tests/data/http_log_file.log'
NO_HEATER_RUNNING = 0
BLOCK_HEATER_RUNNING = 1
COMP_HEATER_1_RUNNING = 2
COMP_HEATER_2_RUNNING = 4
INTERVALS = [(10, NO_HEATER_RUNNING),
             (10, BLOCK_HEATER_RUNNING),
             (10, BLOCK_HEATER_RUNNING | COMP_HEATER_1_RUNNING),
             (10, NO_HEATER_RUNNING)]

class IntegrationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def setup():
    os.remove(HTTP_LOG_FILE)
    # Modify config file
    # Start HTTP monitor

def teardown():
    pass

setup()


total_run_time = sum of intervals...
start_time = time.time()
end_time = start_time + 
now = time.time()

while now < end_time:
    
    now = time.time()



result = os.system('cosycar >/dev/null 2>&1')
if result:
    teardown()
    raise IntegrationError('Integration test failed with: {}'.format(result))
else:
    print('Integration test OK!')

teardown()
