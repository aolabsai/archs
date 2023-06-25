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
from Netbox_App import agent_api_call

#show results button from first page?
def Batch_New_Devices_Callback():
    #run agent on test data
    i=0
    # st.session_state.test_devices_roles_PREDICTED = np.zeros(USER_num_test_devices, dtype='O')
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
        # np.append(test_devices_out, story)
        expected = d.device_role.id
        # expected = format(d.device_role.id, '010b')
        if expected == int(story, 2):
            correct_count += 1
        elif st.session_state.predicted_roles[i] not in roles:
            missing_count += 1
        prog_bar.progress(float(i)/len(test_devices), text='Testing Progress')
    prog_bar.progress(100, 'Training Done')
    
    st.session_state.correct_count = correct_count
    st.session_state.missing_count = missing_count

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

    # st.session_state.predicted_roles = np.zeros(len(test_devices))
    # roles = st.session_state.nbd["roles"]
    # manufacturers = st.session_state.nbd['manufacturers']
    # sites = st.session_state.nbd['sites']
    # types = st.session_state.nbd['types']
    # roles_id_to_str = st.session_state.nbd['roles_id_to_str']
    # inc = st.session_state.nbd['inc']
    # test_devices_info = st.session_state.nbd['test_devices_info']
    # test_devices_array_IO = st.session_state.nbd['test_devices_array_IO']
    # train_devices_array_IO = st.session_state.nbd['train_devices_array_IO']
    
    # USER_num_test_devices = test_devices_array_IO.shape[0]
    
    
    st.title('Netbox Demo - powered by aolabs.ai')
    st.write("")
    st.markdown("## Programmatically Add New Devices")
    
    

    
        # for d in test_devices_array_IO:
        #     st.session_state.agent.reset_state()
        #     st.session_state.agent.next_state(d['manufacturerBin'] + d['siteBin'] + d['typeBin'],
        #                                       print_result=False, unsequenced=True)
        #     st.session_state.agent.next_state(d['manufacturerBin'] + d['siteBin'] + d['typeBin'],
        #                                       print_result=False, unsequenced=True)
        
            # recs_bin = st.session_state.agent.story[ st.session_state.agent.state-1,  st.session_state.agent.arch.Z__flat]
            # recs_dec = binaryListToDecimal(recs_bin.astype(int))
            
            # try:
            #     st.session_state.test_devices_roles_PREDICTED[i] = roles_id_to_str[recs_dec]
            # except KeyError:
            #     st.session_state.mistakes_batch += 1
            #     st.session_state.test_devices_roles_PREDICTED[i] = 'NO GUESS'
    
            # i += 1

    st.button("Add this batch of new (test) devices", on_click= Batch_New_Devices_Callback)
    
    devices = np.zeros([len(test_devices), 6], dtype='O')
    print(devices)
    devices[:, 0] = np.array([d.__str__() for d in test_devices]) #should automatically convert this to the name string
    devices[:, 1] = np.array([manufacturers[d.device_type.manufacturer.id] for d in test_devices])
    devices[:, 2] = np.array([sites[d.site.id] for d in test_devices])
    devices[:, 3] = np.array([types[d.device_type.id] for d in test_devices])
    # devices[:, 4] = st.session_state.predicted_roles
    if 'predicted_roles' not in st.session_state:
        devices[:, 4] = np.array(['' for d in test_devices])
    else:
        devices[:, 4] = np.array([roles[r] for r in st.session_state.predicted_roles])
    devices[:, 5] = np.array([roles[d.device_role.id] for d in test_devices])
    print(devices)
    print(test_devices)
    # device_discovery = np.zeros([USER_num_test_devices, 6], dtype="O")
    # device_discovery[:, 0] = test_devices_info[:, 0]  # name
    # device_discovery[:, 1] = test_devices_info[:, 1]  # manufacturer
    # device_discovery[:, 2] = test_devices_info[:, 2]  # site 
    # device_discovery[:, 3] = test_devices_info[:, 3]  # type 
    # device_discovery[:, 4] = st.session_state.test_devices_roles_PREDICTED
    # device_discovery[:, 5] = test_devices_info[:, 4]  # role, actual

    devices_df = pd.DataFrame( devices, columns=['Name', 'Manufacturer', 'Site', 'Type', 'PREDICTED ROLE', 'EXPECTED ROLE'])
    
    st.table(devices_df)
    
    if 'correct_count' in st.session_state:
        correct_percentage = (st.session_state.correct_count/len(test_devices))*100
        missing_percentage = (st.session_state.missing_count/len(test_devices))*100

        st.write("Out of "+str(len(test_devices))+" devices added, the role was predicted correctly "+str(st.session_state.correct_count)+" times out of "+str(len(test_devices))+".")
        st.write("Or "+str(correct_percentage)+" %.")
        st.write("Also, there were no predictions "+str(st.session_state.missing_count)+" times, or "+str(missing_percentage)+" %.")   
    # correct_predicitons = sum(device_discovery[:, 4] == device_discovery[:, 5])
    # correct_percentage = (correct_predicitons/USER_num_test_devices) * 100
    # noguesses_percentage = (st.session_state.mistakes_batch/USER_num_test_devices) * 100

    # st.write("Out of "+str(USER_num_test_devices)+" devices added, the role was predicted correctly "+str(correct_predicitons)+" times out of "+str(USER_num_test_devices)+".")
    # st.write("Or "+str(correct_percentage)+" %.")
    # st.write("Also, there were no predictions "+str(st.session_state.mistakes_batch)+" times, or "+str(noguesses_percentage)+" %.")    
