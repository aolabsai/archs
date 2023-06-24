# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 01:58:15 2023

@author: alebr
"""

# # AO Labs Modules
# import ao_core as ao

# 3rd Party Modules
import numpy as np
import streamlit as st
import pandas as pd

# from netbox_ai_app.main_netbox import binaryListToDecimal

#show results button from first page?


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
    
    USER_num_test_devices = test_devices_array_IO.shape[0]
    
    
    st.title('Netbox Demo - powered by aolabs.ai')
    st.write("")
    st.markdown("## Programmatically Add New Devices")
            
    def Batch_New_Devices_Callback():
        #run agent on test data
        i=0
        st.session_state.test_devices_roles_PREDICTED = np.zeros(USER_num_test_devices, dtype='O')
        for d in test_devices_array_IO:
            st.session_state.agent.reset_state()
            st.session_state.agent.next_state(d['manufacturerBin'] + d['siteBin'] + d['typeBin'],
                                              print_result=False, unsequenced=True)
            st.session_state.agent.next_state(d['manufacturerBin'] + d['siteBin'] + d['typeBin'],
                                              print_result=False, unsequenced=True)
        
            recs_bin = st.session_state.agent.story[ st.session_state.agent.state-1,  st.session_state.agent.arch.Z__flat]
            recs_dec = binaryListToDecimal(recs_bin.astype(int))
            
            try:
                st.session_state.test_devices_roles_PREDICTED[i] = roles_id_to_str[recs_dec]
            except KeyError:
                st.session_state.mistakes_batch += 1
                st.session_state.test_devices_roles_PREDICTED[i] = 'NO GUESS'
    
            i += 1

    st.button("Add this batch of new (test) devices", on_click= Batch_New_Devices_Callback)

    device_discovery = np.zeros([USER_num_test_devices, 6], dtype="O")
    device_discovery[:, 0] = test_devices_info[:, 0]  # name
    device_discovery[:, 1] = test_devices_info[:, 1]  # manufacturer
    device_discovery[:, 2] = test_devices_info[:, 2]  # site 
    device_discovery[:, 3] = test_devices_info[:, 3]  # type 
    device_discovery[:, 4] = st.session_state.test_devices_roles_PREDICTED
    device_discovery[:, 5] = test_devices_info[:, 4]  # role, actual

    device_discovery_df = pd.DataFrame( device_discovery, columns=['Name', 'Manufacturer', 'Site', 'Type', 'PREDICTED ROLE', 'role'])
    
    st.write(device_discovery_df)
    
    correct_predicitons = sum(device_discovery[:, 4] == device_discovery[:, 5])
    correct_percentage = (correct_predicitons/USER_num_test_devices) * 100
    noguesses_percentage = (st.session_state.mistakes_batch/USER_num_test_devices) * 100

    st.write("Out of "+str(USER_num_test_devices)+" devices added, the role was predicted correctly "+str(correct_predicitons)+" times out of "+str(USER_num_test_devices)+".")
    st.write("Or "+str(correct_percentage)+" %.")
    st.write("Also, there were no predictions "+str(st.session_state.mistakes_batch)+" times, or "+str(noguesses_percentage)+" %.")    
