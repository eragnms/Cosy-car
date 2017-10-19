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
            raise TestFailure(test_case.description) from e
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
        test_engine.run(self.run_time)
                
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
            raise TestFailure(error_text.format(self.zwave_id,
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
                    try:
                        heater.check_status(now,
                                            heater_statuses[heater.zwave_id])
                    except KeyError:
                        # ToDo: here we should mark that the heater did not
                        # have any status info and raise an error if the
                        # device never gets any status set.
                        pass
                next_cosycar_run += self._cosycar_run_period
            now = time.time() - test_start_time

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



     # On = http://$ip_address:3480/data_request?id=action&output_format=xml&DeviceNum=$my_id&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=1
     # Off = http://$ip_address:3480/data_request?id=action&output_format=xml&DeviceNum=$my_id&serviceId=urn:upnp-org:serviceId:SwitchPower1&action=SetTarget&newTargetValue=0


    
class TestFailure(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


if __name__ == "__main__":
    main()    
