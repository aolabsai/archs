# -*- coding: utf-8 -*-
"""
Page 2 of App - Netbox Device Discovery

Purpose: to display the results of an Agent's deivce role predictions

"""

# 3rd Party Modules
import numpy as np
import streamlit as st
import pandas as pd


# from netbox_ai_app.main_netbox import binaryListToDecimal
from Netbox_App import agent_api_call

#show results button from first page?
def Batch_New_Devices_Callback():
    #run agent on test data
    i=0
    
    st.session_state.predicted_roles = np.zeros(len(test_devices), dtype=int)
    correct_count = 0
    missing_count = 0
    prog_bar = st.progress(0, text="Testing Progress")
    for i in range(len(test_devices)):
        d = test_devices[i]
        INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')
        response = agent_api_call(st.session_state.agent_id, INPUT, st.session_state.api_key)
        print(response)
        story = response.json()['story']
        st.session_state.predicted_roles[i] = int(story, 2)
        expected = d.device_role.id
        if expected == int(story, 2):
            correct_count += 1
        elif st.session_state.predicted_roles[i] not in roles:
            missing_count += 1
        prog_bar.progress(float(i)/len(test_devices), text='Testing Progress')
    prog_bar.progress(100, text='Testing Done')
    
    st.session_state.correct_count = correct_count
    st.session_state.missing_count = missing_count


st.sidebar.image("https://raw.githubusercontent.com/netbox-community/netbox/develop/docs/netbox_logo.svg", use_column_width=True) 

# app front end
st.title('Netbox Demo - powered by aolabs.ai')
st.write("")
st.markdown("## Programmatically Add New Devices")

if 'test_devices_in' not in st.session_state: st.text("You have to connect your Netbox account first.")

else:
    # load session data
    manufacturers = st.session_state.manufacturers
    roles = st.session_state.roles
    sites = st.session_state.sites
    types = st.session_state.device_types
    
    api_key = st.session_state.api_key

    test_devices = st.session_state.test_devices_in
    agent_id = st.session_state.agent_id

           
    st.button("Add this batch of new (test) devices", on_click= Batch_New_Devices_Callback, type="primary")
    
    devices = np.zeros([len(test_devices), 6], dtype='O')
    for i in range(len(test_devices)):
        d = test_devices[i]
        devices[i, 0] = d.__str__()
        devices[i, 1] = d.device_type.manufacturer.__str__()
        devices[i, 2] = d.site.__str__()
        devices[i, 3] = d.device_type.__str__()
        if 'predicted_roles' not in st.session_state:    # if the prediction hasn't been run yet, no results to display
            devices[i, 4] = ""
        elif st.session_state.predicted_roles[i] in roles:    # if the 
            devices[i, 4] = roles[st.session_state.predicted_roles[i]]
        else:
            devices[i, 4] = "NO GUESS"        
        devices[i, 5] = roles[d.device_role.id]
    

    devices_df = pd.DataFrame( devices, columns=['Name', 'Manufacturer', 'Site', 'Type', 'PREDICTED ROLE', 'EXPECTED ROLE'])
    
    st.dataframe(devices_df)
    
    if 'correct_count' in st.session_state:
        correct_percentage = (st.session_state.correct_count/len(test_devices))*100
        missing_percentage = (st.session_state.missing_count/len(test_devices))*100

        st.write("Out of "+str(len(test_devices))+" devices added, the role was predicted correctly "+str(st.session_state.correct_count)+" times out of "+str(len(test_devices))+".")
        st.write("Or "+str(correct_percentage)+" %.")
        st.write("Also, there were no predictions "+str(st.session_state.missing_count)+" times, or "+str(missing_percentage)+" %.")   

