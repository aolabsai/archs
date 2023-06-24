# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 01:47:11 2023

@author: alebr
"""

# AO Labs Modules
# import ao_core as ao

# 3rd Party Modules
# import numpy as np
import streamlit as st
import pandas as pd

# from netbox_ai_app.main_netbox import decimalToBinaryList, binaryListToDecimal

if 'nbd' not in st.session_state: st.text("You have to connect your Netbox account first.")
else:

    # load session data
    roles = st.session_state.nbd["roles"]
    manufacturers = st.session_state.nbd['manufacturers']
    sites = st.session_state.nbd['sites']
    types = st.session_state.nbd['types']
    roles_id_to_str = st.session_state.nbd['roles_id_to_str']
    inc = st.session_state.nbd['inc']
    test_devices_info = st.session_state.nbd['test_devices_info']
    test_devices_array_IO = st.session_state.nbd['test_devices_array_IO']
    train_devices_array_IO = st.session_state.nbd['train_devices_array_IO']
    
    st.title('Netbox Demo - powered by aolabs.ai')
    st.write("")
    st.markdown("## Manually Add a New Device")
    # from PIL import Image
    # from urllib.request import urlopen
    # url = ""
    # img = Image.open(urlopen(url))
    # st.image(img)
    st.write("")
    st.markdown("Welcome! This is a prototype of a context aware autocomplete AI for local relational data, powered by [aolabs.ai](https://www.aolabs.ai/).")
    st.markdown("For the purposes of this demo you are a network admin adding the following 10 new devices to your current Netbox configuration as you would on [this Netbox page](https://demo.netbox.dev/dcim/devices/add/):")
    device_discovery_df_batch = pd.DataFrame( test_devices_info[:, 0:4], columns=['Name', 'Manufacturer', 'Site', 'Type'])
    st.write(device_discovery_df_batch)
    st.write("")
    st.markdown("Does our AI autocomplete speed up that process?")
    st.write("The devices and configuration are pulled from https://demo.netbox.dev/dcim/devices/ There are "+str(inc)+" devices there; the 10 devices listed for testing were **excluded** from training (i.e. only "+str(inc-10)+" devices were used for training).")
    st.write("")
    st.markdown("Note: fields marked by '*' are required when adding a new device on Netbox")
    #use on_change to track changes
    
    #%%
    def Recommendation_Callback():
    
        manufacturer_bin = decimalToBinaryList(manufacturers[manufacturer_selected], 10)
        site_bin = decimalToBinaryList(sites[site_selected], 10)
        type_bin = decimalToBinaryList(types[type_selected], 10)
        
        # device type suggestion
        st.session_state.agent.reset_state()
        st.session_state.agent.next_state(manufacturer_bin + site_bin + type_bin, print_result=False, unsequenced=True)
        st.session_state.agent.next_state(manufacturer_bin + site_bin + type_bin, print_result=False, unsequenced=True)
        
        rec_bin = st.session_state.agent.story[ st.session_state.agent.state-1,  st.session_state.agent.arch.Z__flat]
        rec_dec = binaryListToDecimal(rec_bin.astype(int))
    
        st.session_state.rec_dec = rec_dec
        st.session_state.recs += 1
    
    manufacturer_selected = st.selectbox('Manufacturer *', list(manufacturers.keys()))
    site_selected = st.selectbox('Site *', list(sites.keys()))
    type_selected = st.selectbox("Type *", list(types.keys()))
    role_selected = st.selectbox('Device Role *', list(roles.keys()))
    
    Recommendation_Callback()
    
    try:
        st.write("**Predicted** *Device Role*:  "+ roles_id_to_str[st.session_state.rec_dec])
    except KeyError:
        st.session_state.mistakes += 1
        st.write("Oops, no recommendation to offer; this happened "+str( st.session_state.mistakes)+" out of "+str( st.session_state.recs)+" recs so far") 
    
    def New_Device_Callback():
    
        manufacturer_bin = decimalToBinaryList(manufacturers[manufacturer_selected], 10)
        site_bin = decimalToBinaryList(sites[site_selected], 10)
        type_bin = decimalToBinaryList(types[type_selected], 10)
        role_bin = decimalToBinaryList(roles[role_selected], 10)
    
        st.session_state.agent.next_state(manufacturer_bin + site_bin + type_bin,
                            role_bin, print_result=False, unsequenced=True)
        st.session_state.agent.reset_state()
    
    st.write("")
    st.button("Add as new device", on_click= New_Device_Callback)
    st.write("")