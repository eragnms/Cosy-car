#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess
import traceback
import signal
import re

HTTP_LOG_FILE = 'tests/data/http_log_file.log'

def main():
    test_cases = init_test_cases()
    for test_case in test_cases:
        process = setup()
        try:
            test_case.run()
        except TestFailure as e:
            teardown(process)
            raise TestFailure(test_case.name) from e
        except Exception:
            teardown(process)
            raise Exception(traceback.format_exc())

def init_test_cases():
    test_cases = [TestForcedStart(),
                  TestSomethingElse()]
    return test_cases

def setup():
    try:
        os.remove(HTTP_LOG_FILE)
    except:
        pass
    process = subprocess.Popen(['tests/reflect.py', '-p 8085'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return process

def teardown(process):
    os.kill(process.pid, signal.SIGTERM)


class TestForcedStart():
    name = 'Test Forced Start'
    comp_heater_zwave_id = 11
    block_heater_zwave_id = 10
    total_run_time = 20
    block_heater_expected_start_time = 5
    block_heater_expected_stop_time = 20
    comp_heater_expected_start_time = 15
    comp_heater_expected_stop_time = 20

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
        test_engine.run(self.total_run_time)
                
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
        self.touched = False

    def check_status(self, now, is_actually_on):
        is_expected_to_be_on = self._should_heater_be_on(now)
        if is_actually_on != is_expected_to_be_on:
            if is_actually_on:
                current_status = 'ON'
            else:
                currne_status = 'OFF'
            if is_expected_to_be_on:
                expected_status = 'ON'
            else:
                expected_status = 'OFF'
            error_text = 'Heater with id {} is {}, but is expected to be {}'
            error_text += ', time is now {}'
            raise TestFailure(error_text.format(self.zwave_id,
                                                     current_status,
                                                     expected_status,
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
                    try:
                        heater.check_status(now,
                                            heater_statuses[heater.zwave_id])
                        heater.touched = True
                    except KeyError:
                        pass
                next_cosycar_run += self._cosycar_run_period
            now = time.time() - test_start_time
        self._have_heaters_been_touched(self.heaters)

    def _check_heater_statuses(self):
        try:
            heater_statuses = {}
            with open(HTTP_LOG_FILE, 'r') as log_file:
                for line in log_file:
                    device_id = self._extract_device_id(line)
                    device_state = self._extract_device_state(line)
                    if device_id and device_state:
                        heater_statuses['device_id'] = device_state
        except (FileNotFoundError, FileExistsError):
            pass
        return heater_statuses

    def _extract_device_id(self, line):
        device_id = self._extract_info('DeviceNum', line)
        return device_id

    def _extract_device_state(self, line):
        target_value = self._extract_info('TargetValue', line)
        if target_value:
            return True
        else:
            return False

    def _extract_info(self, text, line):
        info_with_text = re.findall(text + '\d+', line)
        info = None
        if info_with_text:
            info = re.findall('\d+', str(info_with_text[0]))
            if info:
                info = selftr(info[0])
        return info

    def _have_heaters_been_touched(self, heaters):
        for heater in heaters:
            if not heater.touched:
                error_text = 'Heater with zwave ID {} has not been switched '
                error_text += 'during the test.'
                raise TestFailure(error_text.format(heater.zwave_id))

     # On = http://$ip_address:3480/data_request?id=action&output_format=xml&DeviceNum=$my_id&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=1
     # Off = http://$ip_address:3480/data_request?id=action&output_format=xml&DeviceNum=$my_id&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=0


    
class TestFailure(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


if __name__ == "__main__":
    main()    
