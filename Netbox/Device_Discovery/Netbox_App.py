# -*- coding: utf-8 -*-
"""
Main Page - Netbox Device Discovery

@author: Shane Polisar, aolabs.ai
"""

# 3rd Party Modules
import numpy as np
import streamlit as st
import requests


#using preset api key for now
api_key = 'buildBottomUpRealAGI'
st.session_state.api_key = api_key     # might cause a bug; as per streamlit docs, the first streamlit command should be st.set_page_config if present; might not apply to st.session_state though see https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config


def agent_api_call(agent_id, input_dat, api_key, label=None):
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
        "X-API-KEY": api_key
    }

    response = requests.post(url, json=payload, headers=headers)
    return response


from PIL import Image
from urllib.request import urlopen
url2 = "https://i.imgur.com/j3jalQE.png"
favicon = Image.open(urlopen(url2))

st.set_page_config(
    page_title="Netbox Device Discovery Demo by aolabs.ai",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "mailto:ali@aolabs.ai",
        'Report a bug': "mailto:ali@aolabs.ai",
        'About': "This is a demo of our AI features. Check out www.aolabs.ai and www.docs.aolabs.ai for more. Thank you!"
    }
)
st.sidebar.image("https://raw.githubusercontent.com/netbox-community/netbox/develop/docs/netbox_logo.svg", use_column_width=True) 

# app front end
st.title('Netbox Device Discovery - demo powered by aolabs.ai')
st.write("")
st.markdown("## Add Your Netbox Account")
instruction_md = "### Welcome \n\
1) This is a demo of AI Agents trained on single Netbox instances, that infer roles of newly discovered devices based on the current local list of devices even as that list changes (Agents are not pre-trained on any other data).\n\
2) After entering the info below to train an Agent, view its predictions in the next page by clicking \"Add New Devices (API Batch)\" in the sidebar"
st.markdown(instruction_md)
# st.markdown("Please enter the information below and then click the **Add Netbox Account** button to get started with this demo.")

# USER inputs
st.session_state.nb_USER_url = st.text_input('Enter your Netbox account URL:', "https://demo.netbox.dev/")
st.session_state.nb_USER_api_token = st.text_input('Enter your Netbox account API token:',  type="password")
st.session_state.USER_num_total_devices = st.number_input('How many of the devices in this Netbox account would you like to use for this demo?' , 0, 200)
x = st.session_state.USER_num_total_devices
st.session_state.USER_num_test_devices = st.number_input("Of those ("+str(x)+") devices, how many should be withheld to TEST this new local Device Discovery AI?" , 0, 100)
st.session_state.agent_id = st.text_input("Enter a unique name/id for this AI Agent")


if st.button("Add Netbox Account & Train Agent", type="primary"):
    
    import pynetbox
    nb = pynetbox.api(
        st.session_state.nb_USER_url,
        token= str(st.session_state.nb_USER_api_token),
        threading=True,
    )

    devices = list(nb.dcim.devices.all())

    manufacturers = {}
    device_types = {}
    sites = {}
    roles = {}
    
    #doing this in a single loop should be more efficient than dictionary comprehensions
    for d in devices:
        manufacturers[d.device_type.manufacturer.id] = d.device_type.manufacturer.__str__()
        device_types[d.device_type.id] = d.device_type.__str__()
        sites[d.site.id] = d.site.__str__()
        roles[d.device_role.id] = d.device_role.__str__()
    
    #save dictionaries to session_state
    st.session_state.manufacturers = manufacturers
    st.session_state.device_types = device_types
    st.session_state.sites = sites
    st.session_state.roles = roles

    
    # shuffle devices, prepare for test and train snapshot
    test_size = st.session_state.USER_num_test_devices
    np.random.shuffle(devices)
    batch = devices[0:st.session_state.USER_num_total_devices]    # batch = devices[:st.session_state.USER_num_total_devices] was not correct indexing
    test_devices_in = batch[0:test_size]
    train_devices_in = batch[test_size:]
    st.session_state.test_devices_in = test_devices_in
    
    count = 0
    prog_bar = st.progress(0, text="Training Progress")
    for d in train_devices_in:
        INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')
        LABEL = format(d.device_role.id, '010b')

        # call API
        response = agent_api_call(st.session_state.agent_id, INPUT, api_key, label=LABEL)

        print("trained on device {} with status code {}".format(count, response))
        count += 1
        

        prog_bar.progress(float(count)/len(train_devices_in), text='Training Progress')

    # display training is DONE message
    prog_bar.progress(1.0, text='Training Done')
    st.write('Training done')
    
    
    st.write("Data successfully loaded, agent is trained from "+st.session_state.nb_USER_url+" via API token: "+st.session_state.nb_USER_api_token)  
    st.write("{num_devices} devices are being used\n- {num_train} for training the agent\n- {num_test} for testing".format(num_devices=st.session_state.USER_num_total_devices, num_train=len(train_devices_in), num_test=test_size))
    # st.write("Out of "+str(len(batch))+" devices, "+str(count)+" were used for training; "+str(st.session_state.USER_num_test_devices)+" were withheld as test devices (to predict their role).")
    st.write("Proceed to the next step in the demo by clicking \"Add New Devices (API Batch)\" in the sidebar")
    st.write("Please remember to re-click the button below if you change the NB account or number of test devices.")

    st.session_state.nb_account_added = True
    st.session_state.new_test_ran = False

else:
    st.write("Add your info before clicking this button")