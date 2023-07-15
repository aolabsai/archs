# -*- coding: utf-8 -*-
"""
Page 2 of App - Netbox Device Discovery

Purpose: to display the results of an Agent's deivce role predictions

"""

# 3rd Party Modules
import numpy as np
import pandas as pd
import streamlit as st

from Main_Page import agent_api_call

#show results button from first page?
def Batch_New_Devices_Callback():
    #run agent on test data
    i=0
    
    st.session_state.predicted_roles = []
    st.session_state.predicted_roles_str = []
    correct_count = 0
    missing_count = 0
    prog_bar = st.progress(0, text="Testing Progress")
    for i in range(len(test_devices)):
        d = test_devices[i]
        
        # Run Agent API
        INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')
        response = agent_api_call(st.session_state.agent_id, INPUT)
        print(response)
        
        # Calculate results
        story = response.json()['story']
        st.session_state.predicted_roles += [int(story, 2)]
        expected = d.device_role.id
        if expected == int(story, 2):
            correct_count += 1
        elif st.session_state.predicted_roles[i] not in roles:
            missing_count += 1

        # Display results        
        try: # the predicted role from the list of roles
            st.session_state.predicted_roles_str += [roles[st.session_state.predicted_roles[i]]]
        except KeyError: # What would otherwise be called a hallucination. :) But we can filter it out because we're working within a fixed encoding/decoding Agent with fixed input/outputs.
            st.session_state.predicted_roles_str += ["NO GUESS"]
                
        prog_bar.progress(float(i)/len(test_devices), text='Testing Progress')
    prog_bar.progress(100, text='Testing Done')
    
    st.session_state.correct_count = correct_count
    st.session_state.missing_count = missing_count
    
    st.session_state.tested = True


# app front end
st.title('Bulk Import New Devices -- with AI Agent Assistance')
if "side_bar_content" in st.session_state: exec(st.session_state.side_bar_content)
else:
    with st.sidebar:
        st.write("*Go to the Main Page to start*")

left_big, right_big = st.columns([0.7, 0.3])

with right_big:
    st.image("https://i.imgur.com/m2Aws1v.png")
    st.markdown("*Screenshot from demo.netbox.dev/dcim/devices/import/*")    
    # with st.expander("See Agent's Arch (Configuration)"):
    #     arch_visual_miro_html= """<iframe width="768" height="432" src="https://miro.com/app/live-embed/uXjVM_kESvI=/?moveToViewport=121907,-48157,16256,9923&embedId=323274877415" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>"""
    #     st.write(arch_visual_miro_html, unsafe_allow_html=True)

with left_big:

    st.write("*Conceived as an API solution for the [bulk import new devices page on Netbox](https://demo.netbox.dev/dcim/devices/import/).*")
    st.write("")
    st.write("")
    st.write("Click the button below to batch-predict the **:red[Roles]** for these new devices.")
    st.write("")
    
    if 'trained' not in st.session_state: st.text("You have to connect your Netbox account and an Agent first.")
    else:
        # load session data
        manufacturers = st.session_state.manufacturers
        roles = st.session_state.roles
        sites = st.session_state.sites
        types = st.session_state.device_types
        
        test_devices = st.session_state.test_devices_in
        agent_id = st.session_state.agent_id
    
        st.button("Predict **Roles** for this batch of new (test) devices", on_click= Batch_New_Devices_Callback, type="primary")
        
        devices = np.zeros([len(test_devices), 6], dtype='O')
        for i in range(len(test_devices)):
            d = test_devices[i]
            devices[i, 0] = d.__str__()
            devices[i, 1] = d.device_type.manufacturer.__str__()
            devices[i, 2] = d.site.__str__()
            devices[i, 3] = d.device_type.__str__()
            
            if 'predicted_roles' in st.session_state and st.session_state.tested is True:
                devices[i, 4] = st.session_state.predicted_roles_str[i]
            else: # the prediction hasn't been run yet, no results to display
                devices[i, 4] = ""
            devices[i, 5] = roles[d.device_role.id]
        
        devices_df = pd.DataFrame( devices, columns=['Name', 'Manufacturer', 'Site', 'Type', 'PREDICTED ROLE', 'EXPECTED ROLE'])

    if 'trained' in st.session_state:
        
        st.dataframe(devices_df)
        
        if st.session_state.tested is True:
            correct_percentage = (st.session_state.correct_count/len(test_devices))*100
            missing_percentage = (st.session_state.missing_count/len(test_devices))*100
            
            st.session_state.Agents[ st.session_state.agent_id ][ 'accuracy (bulk)' ] = str(correct_percentage)
            st.session_state.Agents[ st.session_state.agent_id ][ 'no guesses (bulk)' ] = str(missing_percentage)
            
        
            st.write("Out of "+str(len(test_devices))+" devices added, the role was predicted correctly "+str(st.session_state.correct_count)+" times out of "+str(len(test_devices))+".")
            st.write("Or "+str(correct_percentage)+" %.")
            st.write("Also, there were no predictions "+str(st.session_state.missing_count)+" times, or "+str(missing_percentage)+" %.")   