# -*- coding: utf-8 -*-

# This script is written with the purpose of finding out what the
# reflect script should respond on http requests from pyvera to good
# enough mimic a vera controller. This is something we need to know to
# be able to use the reflect script for integration tests.

# Aim with the script is to get the functions "vera" and "reflect"
# to printout similar results.

import pyvera
import requests

VERA_ADDRESS = "192.168.0.217"
REFLECT_ADDRESS = "192.168.0.217"
VERA_PORT = 3480
REFLECT_PORT = 8080

def connect_to_controller(address):
    controller = pyvera.VeraController(address)
    return controller
    
def get_devices(base_url):
    request_url = base_url + "/data_request"
    payload = {'id': 'sdata'}
    j = requests.get(request_url, timeout=30, params=payload).json()    
    print(j)

def vera():
    controller_address = "http://{}:{}/".format(VERA_ADDRESS, VERA_PORT)
    controller = connect_to_controller(controller_address)
    get_devices(controller_address)
    
def reflect():
    pass

def main():
    vera()

if __name__ == "__main__":
    main()
