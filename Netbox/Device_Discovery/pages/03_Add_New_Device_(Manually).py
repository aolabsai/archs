# -*- coding: utf-8 -*-
"""
Page 3 of App - Netbox Device Discovery

Purpose: to display the results of an Agent's deivce role prediction as an autofill recommender that can be live-trained

"""

# 3rd Party Modules
import streamlit as st
import numpy as np
import pandas as pd

# App Modules
from Netbox_App import agent_api_call


# need to move these to main app page after Shane's fixes
st.session_state.recs = 0
st.session_state.mistakes = 0


def Recommendation_Callback():            
    # Run Agent API
    INPUT = format(manufacturer_id, '010b') + format(type_id, '010b') + format(site_id, '010b')
    response = agent_api_call(st.session_state.agent_id, INPUT, st.session_state.api_key)
    print("RECOMMENDED - "+response)

    st.session_state.recs += 1
    try:
        st.session_state.recommendation = roles[response]
        st.write("**Predicted** *Device Role*:  "+ st.session_state.recommendation)
    except KeyError:
        st.session_state.mistakes += 1
        st.write("Oops, no recommendation to offer; this happened "+str( st.session_state.mistakes)+" out of "+str( st.session_state.recs)+" recs so far") 


def Confirm_Recommendation_Callback():               
    # Run Agent API
    INPUT = format(manufacturer_id, '010b') + format(type_id, '010b') + format(site_id, '010b')
    LABEL = format(role_id, '010b')
    response = agent_api_call(st.session_state.agent_id, INPUT, st.session_state.api_key, label=LABEL)
    print("CONFIRMED - "+response)
    st.write("Device confirmed; has been trained.") 


## front end
st.title('Netbox Demo - powered by aolabs.ai')
st.sidebar.image("https://raw.githubusercontent.com/netbox-community/netbox/develop/docs/netbox_logo.svg", use_column_width=True) 
st.write("")
st.markdown("## Manually Add a New Device")
st.write("")
st.markdown("Welcome! This is a prototype of a context aware autocomplete AI for local relational data, powered by [aolabs.ai](https://www.aolabs.ai/).")

if 'trained' not in st.session_state:
    st.write("")
    st.text("You have to connect your Netbox account first.")

else:

    # generate table of devices to be added / recommended    
    if st.session_state.new_test_ran is True:
        test_devices = st.session_state.test_devices_in
        test_devices_table = np.zeros([len(test_devices), 4], dtype='O')
        for i in range(len(test_devices)):
            d = test_devices[i]
            test_devices_table[i, 0] = d.__str__()
            test_devices_table[i, 1] = d.device_type.manufacturer.__str__()
            test_devices_table[i, 2] = d.site.__str__()
            test_devices_table[i, 3] = d.device_type.__str__()
        st.session_state.test_devices_table = pd.DataFrame( test_devices_table, columns=['Name', 'Manufacturer', 'Site', 'Type'])
    st.markdown("For the purposes of this demo you are a network admin adding the following devices to your current Netbox configuration as you would on [this Netbox page](https://demo.netbox.dev/dcim/devices/add/):")
    st.write(st.session_state.test_devices_table)
    st.write("")

    # load session data
    manufacturers = st.session_state.manufacturers
    roles = st.session_state.roles
    sites = st.session_state.sites
    types = st.session_state.device_types  

    # USER input fields    
    manufacturer_selected = st.selectbox('Manufacturer *', list(manufacturers.values()))
    site_selected = st.selectbox('Site *', list(sites.values()))
    type_selected = st.selectbox("Type *", list(types.values()))
    role_selected = st.selectbox('Device Role *', list(roles.values()))

    #converting user input to IDs
    manufacturer_id = list(manufacturers.keys())[list(manufacturers.values()).index(manufacturer_selected)]
    site_id = list(sites.keys())[list(sites.values()).index(site_selected)]
    type_id = list(types.keys())[list(types.values()).index(type_selected)]
    role_id = list(roles.keys())[list(roles.values()).index(role_selected)]
    
    # recommend a device whenever any input changes on this page
    Recommendation_Callback()

    # offer USER ability to confirm recommendation and postively reinforce Agent    
    st.write("")
    st.button("Add as new device", on_click= Confirm_Recommendation_Callback)
    st.write("")