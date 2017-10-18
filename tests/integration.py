#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess

def main():
    test_cases = init_test_cases()
    for test_case in test_cases:
        process = setup()
        test_case.run()
        teardown(process)

def init_test_cases():
    test_cases = [TestForcedStart(),
                  TestSomethingElse()]
    return test_cases

def setup():
    try:
        os.remove(HTTP_LOG_FILE)
    except:
        pass
    process = subprocess.Popen(['tests/reflect.py'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def teardown(process):
    os.kill(process.pid, signal.SIGTERM)


class TestForcedStart():
    description = 'Test Forced Start'
    run_time = 60
    block_heater_zwave_id = 10
    block_heater_expected_start_time = 10
    block_heater_expected_stop_time = 50
    comp_heater_zwave_id = 11
    comp_heater_expected_start_time = 25
    comp_heater_expected_stop_time = 50

    def __init__(self):
        block_heater = Heater(self.block_heater_zwave_id,
                              self.block_heater_expected_start_time,
                              self.block_heater_expected_stop_time)
        comp_heater = Heater(self.comp_heater_zwave_id,
                             self.comp_heater_expected_start_time,
                             self.comp_heater_expected_stop_time)
        self.heaters = [block_heater, comp_heater]
            
    def run(self):
        os.system('cosycar >/dev/null 2>&1')
        test_engine = TestEngine(self.heaters)
        try:
            test_engine.run(self.run_time)
        except IntegrationError as e:
            raise IntegrationError(self.description + ': ' + e.value)
        
class TestSomethingElse():
    def __init__(self):
        self.description = 'TestSomethingElse'

    def run(self):
        pass
        

class Heater():
    def __init__(self, zwave_id, start_time, stop_time):
        self.zwave_id = zwave_id 
        self.start_time = start_time
        self.stop_time = stop_time

    def check_status(self, now, is_actually_on):
        expected_to_be_on = self._should_heater_be_on(now)
        if is_actually_on != expected_to_be_on:
            error_text = 'Heater with id {} has status {}, expected'
            error_text += ' status {}, time is {}'
            raise IntegrationError(error_text.format(self.zwave_id,
                                                     is_actually_on,
                                                     expected_to_be_on,
                                                     now))
        
    def _should_heater_be_on(self, now):
        if (now >= self.start_time) and (now < self.stop_time):
            return True
        else:
            return False


class TestEngine():
    _cosycar_run_period = 2
    def __init__(self, heaters):
        self.heaters = heaters

    def run(self, run_time):
        test_start_time = time.time()
        now = 0
        next_cosycar_run = now
        while now < run_time:
            if now >= next_cosycar_run:
                os.system('cosycar >/dev/null 2>&1')
                heater_statuses = self._check_heater_statuses()
                for heater in self.heaters:
                    heater.check_status(now, heater_statuses[heater.zwave_id])
                next_cosycar_run += self._cosycar_run_period
            now = time.time() - test_start_time

    def _check_heater_statuses(self):
        statuses = {10: False, 11: False}
        return statuses

     # On = http://$ip_address:3480/data_request?id=action&output_format=xml&DeviceNum=$my_id&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=1
     # Off = http://$ip_address:3480/data_request?id=action&output_format=xml&DeviceNum=$my_id&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=0

    

class IntegrationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


if __name__ == "__main__":
    main()    
