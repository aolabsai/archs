# -*- coding: utf-8 -*-
"""
Script to Run Device Discovery AI Agents for Self-Host NetBox
a local version of this app: https://aolabs-netbox.streamlit.app/

- run this script in the env where you host your NetBox instance; it uses the pynetbox module to connect to your device info only
- Agents are persistently hosted on our Agents-as-a-Service API, reference https://docs.aolabs.ai/reference/agentinvoke
- for this script the API is throttled, so latency per Agent per device is around 1.38 seconds; we can beef this up for your production needs, just ping us
- if Agents prove useful, you can also host Agents locally (on simple python env); again just ping us for access

www.aolabs.ai
"""

# 3rd Party Modules
import requests
import pynetbox  # Netbox interface


def agent_api_call(agent_id, input_data, label=None):

    url = "https://7svo9dnzu4.execute-api.us-east-2.amazonaws.com/v0dev/kennel/agent"
    payload = {
        "kennel_id": "v0dev/TEST-Netbox_DeviceDiscovery",  # using this arch https://github.com/aolabsai/archs/blob/main/Architectures/netbox-device_discovery.py
        "agent_id": agent_id,
        "INPUT": input_data,
        "control": {
            "US": True
        }
    }
    if label != None:
        payload["LABEL"] = label
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "buildBottomUpRealAGI"
    }
    response = requests.post(url, json=payload, headers=headers)
    response = response.json()['story']  # we can expose the HTTP response here, too
    return response


# Getting Devices list from NetBox
nb = pynetbox.api(
    "https://demo.netbox.dev/",
    token= "a5d05d1136c262036d0525de49df3f59d231b7c1", # insert API token here as a string, get from https://demo.netbox.dev/user/api-tokens/ use username: admin password: admin
    threading=True)
try:
    devices = list(nb.dcim.devices.all())
except pynetbox.RequestError as e:
    print(e+"::  could not connect to netbox via pynetbox")

discovered_devices = []


# Name your Agent; you can create as many as you need; Agents are not pre-trained
agent_id = "Test Agent 1"


# Training your Agent on Devices list
for d in devices:
    INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')
    LABEL = format(d.device_role.id, '010b')

    response = agent_api_call( agent_id, INPUT, LABEL)
    print("Role ID response: " +str( int(response, 2) ))

print("Trained on all "+ str(len(devices)))

    
# Using your Agent - same as above, just without a label
for d in discovered_devices:
    INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')

    response = agent_api_call( agent_id, INPUT )
    # response will be a string of 10-binary digits corresponding to the Role ID of the inputed device


# Using your Agent on 1 device
INPUT = "0000000011"+"0000000111"+"0000001010"
response = agent_api_call( agent_id, INPUT )
print("Role ID response: " +str( int(response, 2) ))

    
# Need to re-train Agent? Any time label is passed through, Agent learns it
# Need more than 3 input fields for your *platform* use-case? This Agent was configured with 3 inputs to 1 output; its configuration is easy to expand and can be found here: https://github.com/aolabsai/archs/blob/main/Architectures/netbox-device_discovery.py


# Agents are also fully interpertable (not a blackbox) by design, as they store all past states in their lookup table (only states labelled by a label or instinct trigger are used for learning; the rest is pruned)
# you can view the history below
def retreive_agent_history(agent_id):

    url = "https://7svo9dnzu4.execute-api.us-east-2.amazonaws.com/v0dev/kennel/agent"
    payload = {
        "kennel_id": "v0dev/TEST-Netbox_DeviceDiscovery",
        "agent_id": agent_id,
        "request": "story",
        "control": {
            "US": True
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "buildBottomUpRealAGI"
    }
    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    return response

history = retreive_agent_history(agent_id)

import numpy as np
history_array = np.asarray(list( history['story']), dtype=int).reshape( 74, history['state'])     # 74 is the total number of neurons in this Agent, as per it's arch https://github.com/aolabsai/archs/blob/main/Architectures/netbox-device_discovery.py


