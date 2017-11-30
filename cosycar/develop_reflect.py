# -*- coding: utf-8 -*-

# This script is written with the purpose of finding out what the
# reflect script should respond on http requests from pyvera to good
# enough mimic a vera controller. This is something we need to know to
# be able to use the reflect script for integration tests.

# Aim with the script is to get the functions "vera" and "reflect"
# to printout similar results. This means that also the reflect
# function should call the function switch_device.

import pyvera
import requests
import time

VERA_ADDRESS = "192.168.0.217"
REFLECT_ADDRESS = "localhost"
VERA_PORT = 3480
REFLECT_PORT = 8080
ZWAVE_DEVICE_ID = 7

def main():
    #vera()
    #time.sleep(2)
    reflect()

def vera():
    switch_device(VERA_ADDRESS, VERA_PORT)
    
def reflect():
    switch_device(REFLECT_ADDRESS, REFLECT_PORT)
    #switch_device_reflect_test(VERA_ADDRESS, VERA_PORT)
    
def switch_device_reflect_test(address, port):
    controller_address = "http://{}:{}/".format(address, port)
    controller = connect_to_controller(controller_address)
    devices = get_devices(controller)
    mapping_id_to_ix = {}
    for index, value in enumerate(devices):
        mapping_id_to_ix[value.device_id] = index
    index = mapping_id_to_ix[ZWAVE_DEVICE_ID]
    devices[index].switch_on()
    time.sleep(2)
    devices[index].switch_off()

def switch_device_vera_test(address, port):
    controller_address = "http://{}:{}/".format(address, port)
    controller = connect_to_controller(controller_address)
    devices = get_devices(controller)
    print(devices)
    mapping_id_to_ix = {}
    for index, value in enumerate(devices):
        mapping_id_to_ix[value.device_id] = index
    index = mapping_id_to_ix[ZWAVE_DEVICE_ID]
    devices[index].switch_on()
    time.sleep(2)
    devices[index].switch_off()
    
def switch_device(address, port):
    controller_address = "http://{}:{}/".format(address, port)
    controller = connect_to_controller(controller_address)
    devices = get_devices(controller)
    mapping_id_to_ix = {}
    for index, value in enumerate(devices):
        mapping_id_to_ix[value.device_id] = index
    index = mapping_id_to_ix[ZWAVE_DEVICE_ID]
    devices[index].switch_on()
    time.sleep(2)
    devices[index].switch_off()

def connect_to_controller(address):
    controller = pyvera.VeraController(address)
    return controller

def get_devices(controller):
    return controller.get_devices('On/Off Switch')
    
def get_devices_test(base_url):
    request_url = base_url + "/data_request"
    payload = {'id': 'sdata'}
    j = requests.get(request_url, timeout=30, params=payload).json() 
    
    categories = {}
    cats = j.get('categories')
    for cat in cats:
        categories[cat.get('id')] = cat.get('name')

    device_id_map = {}
    devs = j.get('devices')
    for dev in devs:
        dev['categoryName'] = categories
        device_id_map[dev.get('id')] = dev
        
    payload = {'id': 'status', 'output_format': 'json'}
    j = requests.get(request_url, timeout=30, params=payload).json() 


if __name__ == "__main__":
    main()
