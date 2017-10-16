#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time

PORT = 8085
HTTP_LOG_FILE = 'tests/data/http_log_file.log'
COSYCAR_RUN_PERIOD = 2
NO_HEATER_RUNNING = 0
BLOCK_HEATER_RUNNING = 1
COMP_HEATER_1_RUNNING = 2
COMP_HEATER_2_RUNNING = 4
INTERVALS = [(2, NO_HEATER_RUNNING),
             (2, BLOCK_HEATER_RUNNING),
             (2, BLOCK_HEATER_RUNNING | COMP_HEATER_1_RUNNING),
             (2, NO_HEATER_RUNNING)]

class IntegrationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)    
        
def setup():
    try:
        os.remove(HTTP_LOG_FILE)
    except:
        pass
    # Modify config file
    # Start HTTP monitor

def teardown():
    pass

def main():
    setup()

    time_to_run = 0
    for interval_length, c in INTERVALS:
        time_to_run += interval_length
    start_time = time.time()
    end_time = start_time + time_to_run
    next_run = start_time

    current_interval = 1
    while test_is_not_ready(end_time):
        if time_to_run_cosycar(next_run):
            result = os.system('cosycar >/dev/null 2>&1')    
            if result:
                teardown()
                error = "Cosycar failed in interval {} with code {}"
                raise IntegrationError(error.format(current_interval, result))
           is_correct_heaters_running(current_interval)
              
            next_run += COSYCAR_RUN_PERIOD
        current_interval = check_current_interval(current_interval, start_time)
        
    teardown()

def test_is_not_ready(end_time):
    return time.time() < end_time

def time_to_run_cosycar(next_run):
    return time.time() >= next_run

def check_current_interval(current_interval, start_time):
    next_interval_start = start_time
    for n in range (0, current_interval):
        interval_length, c = INTERVALS[n]
        next_interval_start += interval_length
    now = time.time()
    if now > next_interval_start:
        return current_interval + 1
    else:
        return current_interval
     
 def is_correct_heaters_running(current_interval):
     running_heaters = which_heaters_are_running()
     expected_heaters = which_heaters_should_run(current_interval)
     if running_heaters != expected_heaters:
        error('Wrong heateres running ininterval {}, expected {}, got {}')
        raise IntegrationeError(error)
     return True

if __name__ == "__main__":
    main()    
