# -*- coding: utf-8 -*-
"""
Main Page - Netbox Device Discovery

@author: Shane Polisar, aolabs.ai
"""

# 3rd Party Modules
import numpy as np
import streamlit as st
import requests
from PIL import Image
from urllib.request import urlopen
import pynetbox  # Netbox interface


# Returns json, result stored in json as Agent's 'story'
def agent_api_call(agent_id, input_dat, label=None):
    url = "https://7svo9dnzu4.execute-api.us-east-2.amazonaws.com/v0dev/kennel/agent"

    payload = {
        "kennel_id": "v0dev/TEST-Netbox_DeviceDiscovery",
        "agent_id": agent_id,
        "INPUT": input_dat,
        "control": {
            "US": True
        }
    }
    if label != None:
        payload["LABEL"] = label

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": st.secrets['aolabs_api_key']
    }

    response = requests.post(url, json=payload, headers=headers)
    return response


def add_netbox():
    nb = pynetbox.api(
        st.session_state.nb_USER_url,
        token= str(st.session_state.nb_USER_api_token),
        threading=True)
    devices = list(nb.dcim.devices.all())

    #save {id: attribute} dicts of device info to session_state
    manufacturers = {}
    device_types = {}
    sites = {}
    roles = {}    

    for d in devices:
        manufacturers[d.device_type.manufacturer.id] = d.device_type.manufacturer.__str__()
        device_types[d.device_type.id] = d.device_type.__str__()
        sites[d.site.id] = d.site.__str__()
        roles[d.device_role.id] = d.device_role.__str__()
    
    st.session_state.manufacturers = manufacturers
    st.session_state.device_types = device_types
    st.session_state.sites = sites
    st.session_state.roles = roles

    st.session_state.devices = devices
    st.session_state.num_devices = len(st.session_state.devices)
    st.session_state.account_added = True


if 'account_added' not in st.session_state:
    st.session_state.num_devices = 0
    st.session_state.account_added = False


# Trains an Agent on a Netbox instance, first shuffling the list of devices, and for this demo perparing subsets of devices for training and testing
def train_agents():
    devices = st.session_state.devices
    np.random.shuffle(devices)
    
    test_size = st.session_state.USER_num_test_devices
    batch = devices[0:st.session_state.USER_num_total_devices]
    test_devices_in = batch[0:test_size]
    train_devices_in = batch[test_size:]
    st.session_state.test_devices_in = test_devices_in
    st.session_state.train_size = len(train_devices_in)
    
    prog = 0
    prog_bar = st.progress(0, text="Training Progress")
    for d in train_devices_in:
        INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')
        LABEL = format(d.device_role.id, '010b')

        # call Agent via API
        response = agent_api_call(st.session_state.agent_id_field, INPUT, label=LABEL)
        # print("trained on device {} with status code {}".format(count, response))
        
        prog += 1
        prog_bar.progress(float(prog)/len(train_devices_in), text='Training Progress')
    # display training is DONE message
    prog_bar.progress(1.0, text='Training Complete')

    st.session_state.agent_id = st.session_state.agent_id_field
    st.session_state.trained = True
    st.session_state.tested = False
    st.session_state.recs = 0
    st.session_state.mistakes = 0


# Streamlit-powered frontend
url2 = "https://i.imgur.com/j3jalQE.png"
favicon = Image.open(urlopen(url2))
st.set_page_config(
    page_title="Local Device Discovery AI Agent - demo by aolabs.ai",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "mailto:ali@aolabs.ai",
        'Report a bug': "mailto:ali@aolabs.ai",
        'About': "This is a demo of our AI features. Check out www.aolabs.ai and docs.aolabs.ai for more. Thank you!"
    }
)
st.sidebar.image("https://raw.githubusercontent.com/netbox-community/netbox/develop/docs/netbox_logo.svg", use_column_width=True)
st.title('Local AI Agents for Netbox Device Discovery')
st.write("## demo by [aolabs.ai](https://www.aolabs.ai/)")
st.write("")
instruction_md = "### Welcome! \n\
In testing out a new type of locally trained AI Agents, we applied them to Netbox, specifcally to device discovery.\n\
**How it works:** you connect an Agent to a single Netbox instance (enter a netbox url and token); it'll be trained on your list of devices, from the manufacter, type, and site, to infer the role of newly added devices. Agents are not pre-trained on any other data and can live in state with your list of devices if used in your application.\n\
After entering the info below to train an Agent, view its predictions in the sidebar as a batch or as an context-aware auto-complete."
st.markdown(instruction_md)

# Capture USER inputs
left, right = st.columns(2)

## Netbox account
with left:
    st.session_state.nb_USER_url = st.text_input('Enter your Netbox account URL:', "https://demo.netbox.dev/")
    help_netbox_api = "Get your Netbox API key from {your Netbox url}/user/api-tokens/ or from the Netbox public demo by logging in to [demo.netbox.dev](https://demo.netbox.dev/user/api-tokens/) with username 'admin' and password 'admin'"
    st.session_state.nb_USER_api_token = st.text_input('Enter your Netbox account API token:',  type='password', help=help_netbox_api)

    left_filled = len(st.session_state.nb_USER_url) > 0 and len(st.session_state.nb_USER_api_token) > 0
    st.button("Connect Netbox Account", type="primary", on_click=add_netbox, disabled=not(left_filled))
       
    if st.session_state.account_added is True:
        st.write("Agent connected; there {} devices on this Netbox account available for training/testing.".format(st.session_state.num_devices))

## Training and test configuration
with right:
    st.session_state.USER_num_total_devices = st.number_input("How many of the available devices in this Netbox account would you like to use for this demo?" , min_value=2, max_value=st.session_state.num_devices, disabled=not(st.session_state.account_added))
    x = st.session_state.USER_num_total_devices
    max_test_devices = x-1
    help_numtest = "The rest of the devices will be used for training the Agent."
    st.session_state.USER_num_test_devices = st.number_input("Of those ("+str(x)+") devices, how many should be withheld to TEST the Agent?" , min_value=1, max_value=max_test_devices, disabled=not(st.session_state.account_added), help=help_numtest)
    st.session_state.agent_id_field = st.text_input("Enter a unique name for this Agent", disabled=not(st.session_state.account_added))

    right_filled = len(st.session_state.agent_id_field) > 0
    st.button("Train Your Agent", type="primary", on_click=train_agents, disabled=not(st.session_state.account_added) or not(right_filled))

# Post training message
if 'trained' in st.session_state:
    st.write('Agent Training Complete')
    st.write("From "+st.session_state.nb_USER_url+" via API token: "+st.session_state.nb_USER_api_token)  
    device_count = st.session_state.train_size + len(st.session_state.test_devices_in)
    st.write("")
    st.write("- {num_devices} devices are being used\n- {num_train} for training the agent\n- {num_test} for testing".format(num_devices=device_count, num_train=st.session_state.train_size, num_test=len(st.session_state.test_devices_in)))
    st.write("Proceed to testing the Agent by clicking the pages in the sidebar.")