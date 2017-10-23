#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To add a new test case, write a class "TestSomething" and add it to the
list "test_cases" in the function "init_test_cases".
"""
import os
import time
import subprocess
import traceback
import signal
import re
import configparser

HTTP_LOG_FILE = '/tmp/cosycar_http_log_file.log'
CONFIG_FILE = '.config/cosycar.cfg'
HTTP_PORT = 8085
SECONDS_PER_MINUTE = 60


def init_test_cases():
    test_cases = [TestGivenTimeToLeave()]
    return test_cases


class TestGivenTimeToLeave():
    name = 'Given time to leave'
    block_heater_zwave_id = 21
    comp_heater_zwave_id = 14
    total_time_to_run = 50 * SECONDS_PER_MINUTE
    cosycar_check_period = 2 * SECONDS_PER_MINUTE
    block_heater_expected_start_time = 5 * SECONDS_PER_MINUTE
    block_heater_expected_stop_time = 45 * SECONDS_PER_MINUTE
    comp_heater_expected_start_time = 20 * SECONDS_PER_MINUTE
    comp_heater_expected_stop_time = 45 * SECONDS_PER_MINUTE

    def __init__(self):
        block_heater = Heater(self.block_heater_zwave_id,
                              self.block_heater_expected_start_time,
                              self.block_heater_expected_stop_time)
        comp_heater = Heater(self.comp_heater_zwave_id,
                             self.comp_heater_expected_start_time,
                             self.comp_heater_expected_stop_time)
        self.heaters = [block_heater, comp_heater]

    def run(self):
        os.system('cosycar --time-to-leave-in 35 >/dev/null 2>&1')
        test_engine = TestEngine(self)
        test_engine.run()


def main():
    test_cases = init_test_cases()
    for test_case in test_cases:
        setup()
        try:
            test_case.run()
        except TestFailure as e:
            teardown()
            error_text = 'Test case: "{}" failed!'
            raise TestFailure(error_text.format(test_case.name)) from e
        except Exception:
            teardown()
            raise Exception(traceback.format_exc())


def setup():
    remove_http_log_file()
    start_http_listen_process()
    modify_cfg_file_for_testing()


def teardown():
    kill_http_listen_process()
    restore_cfg_file()
    remove_http_log_file()


def start_http_listen_process():
    process = subprocess.Popen(
        ['tests/reflect.py', '-p {}'.format(HTTP_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    SetupParams.reflect_process = process


def modify_cfg_file_for_testing():
    home_dir = os.environ['HOME']
    cfg_file = os.path.join(home_dir, CONFIG_FILE)
    config = save_current_cfg_file_settings(cfg_file)
    config['ZWAVE_CONTROLLER']['ip_address'] = 'localhost'
    config['ZWAVE_CONTROLLER']['port'] = str(HTTP_PORT)
    with open(cfg_file, 'w') as configfile:
        config.write(configfile)


def save_current_cfg_file_settings(cfg_file):
    config = configparser.ConfigParser()
    config.read(cfg_file)
    ip_address = config['ZWAVE_CONTROLLER']['ip_address']
    port = config['ZWAVE_CONTROLLER']['port']
    SetupParams.cfg_file = cfg_file
    SetupParams.ip_address = ip_address
    SetupParams.port = port
    return config


def kill_http_listen_process():
    os.kill(SetupParams.reflect_process.pid, signal.SIGTERM)


def restore_cfg_file():
    config = configparser.ConfigParser()
    cfg_file = SetupParams.cfg_file
    config.read(cfg_file)
    config['ZWAVE_CONTROLLER']['ip_address'] = str(SetupParams.ip_address)
    config['ZWAVE_CONTROLLER']['port'] = str(SetupParams.port)
    with open(cfg_file, 'w') as configfile:
        config.write(configfile)


def remove_http_log_file():
    try:
        os.remove(HTTP_LOG_FILE)
    except:
        pass


class SetupParams():
    cfg_file = None
    reflect_process = None
    ip_address = None
    port = None


class Heater():
    def __init__(self, zwave_id, start_time, stop_time):
        self.zwave_id = zwave_id
        self.start_time = start_time
        self.stop_time = stop_time
        self.touched = False

    def check_status(self, now, is_actually_on_now):
        is_expected_to_be_on = self._should_heater_be_on(now)
        current_status = self._decode_status(is_actually_on_now)
        expected_status = self._decode_status(is_expected_to_be_on)
        if current_status != expected_status:
            error_text = 'Heater with id {} is {}, but is expected to be {}'
            error_text += ', time is now {}'
            raise TestFailure(
                error_text.format(self.zwave_id, current_status,
                                  expected_status, now))

    def _decode_status(self, status):
        if status:
            return 'ON'
        else:
            return 'OFF'

    def _should_heater_be_on(self, now):
        if (now >= self.start_time) and (now < self.stop_time):
            return True
        else:
            return False


class TestEngine():
    def __init__(self, test_case):
        self._test_case = test_case

    def run(self):
        test_case_start_time = time.time()
        now = 0
        next_cosycar_check = now
        while now < self._test_case.total_time_to_run:
            if now >= next_cosycar_check:
                os.system('cosycar --check >/dev/null 2>&1')
                self._check_heater_statuses(now)
                next_cosycar_check += self._test_case.cosycar_check_period
            now = time.time() - test_case_start_time
        self._have_heaters_been_touched(self._test_case.heaters)

    def _check_heater_statuses(self, now):
        heater_statuses = self._check_current_heater_statuses()
        for heater in self._test_case.heaters:
            try:
                heater.check_status(now, heater_statuses[heater.zwave_id])
                heater.touched = True
            except KeyError:
                pass

    def _check_current_heater_statuses(self):
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
        device_id = self._extract_info_number('DeviceNum', line)
        return device_id

    def _extract_device_state(self, line):
        target_value = self._extract_info_number('TargetValue', line)
        if target_value:
            return True
        else:
            return False

    def _extract_info_number(self, text, line):
        info_with_text = re.findall(text + '\d+', line)
        info_number = None
        if info_with_text:
            number = re.findall('\d+', str(info_with_text[0]))
            if number:
                info_number = str(number[0])
        return info_number

    def _have_heaters_been_touched(self, heaters):
        for heater in heaters:
            if not heater.touched:
                error_text = 'Heater with zwave ID {} has not been switched '
                error_text += 'during the test.'
                raise TestFailure(error_text.format(heater.zwave_id))


class TestFailure(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == "__main__":
    main()
