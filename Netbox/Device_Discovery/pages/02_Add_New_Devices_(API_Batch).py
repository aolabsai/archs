# -*- coding: utf-8 -*-
"""
Page 2 of App - Netbox Device Discovery

Purpose: to display the results of an Agent's deivce role predictions

"""

# 3rd Party Modules
import numpy as np
import streamlit as st
import pandas as pd


if 'nb_account_added' not in st.session_state: st.text("You have to connect your Netbox account first.")
else:

# variables loaded from st.session_state (client session)#####################
#########
    USER_num_test_devices = st.session_state.USER_num_test_devices
    test_devices_in =       st.session_state.test_devices_in
    test_devices_out_roles= st.session_state.test_devices_out_roles    
    
    correct_count = st.session_state.correct_count
    noguess_count = st.session_state.noguess_count
#########


    # app front end
    st.title('Netbox Demo - powered by aolabs.ai')
    st.write("")
    st.markdown("## Programmatically Add New Devices")

    
    # create device_discovery to contain table of results
    if st.session_state.device_discovery is False:
        device_discovery = np.zeros([USER_num_test_devices, 6], dtype="O")
        i= 0    
        for d in test_devices_in:
            device_discovery[i, 0] = d.__str__()                           # name
            device_discovery[i, 1] = d.device_type.manufacturer.__str__()  # manufacturer
            device_discovery[i, 2] = d.device_type.__str__()               # device type
            device_discovery[i, 3] = d.site.__str__()                      # site 
            device_discovery[i, 4] = ""                          # PREDICTED role
            device_discovery[i, 5] = d.device_role.__str__()               # role, actual
            i += 1
########   Save it to st.session_state
        st.session_state.device_discovery = device_discovery
    
        
    # On USER click, return results from st.session_state from the main app page    
    if st.button("Add this batch of new devices (i.e. run/view test)", key="view_results", type="primary"):
    
        # Add results to 5th column, PREDICTED ROLE
        st.session_state.device_discovery[:, 4] = st.session_state.test_devices_out_roles
        
        # Display % accuracy + no guesses and other info
        correct_percentage =   ( correct_count / USER_num_test_devices ) * 100
        noguess_percentage = ( noguess_count / USER_num_test_devices ) * 100
        
        st.write("Out of "+str(USER_num_test_devices)+" devices added, the role was predicted correctly "+str(correct_count)+" times out of "+str(USER_num_test_devices)+".")
        st.write("Or "+str(correct_percentage)+" %.")
        st.write("Also, there were no predictions "+str(noguess_count)+" times, or "+str(noguess_percentage)+" %.")

    # use pandas dataframe + streamlit to display results for USER
    device_discovery_df = pd.DataFrame( st.session_state.device_discovery, columns=['Name', 'Manufacturer', 'Type', 'Site', 'PREDICTED ROLE', 'Role'])        
    st.write(device_discovery_df)