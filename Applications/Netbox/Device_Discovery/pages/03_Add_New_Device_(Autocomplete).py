# -*- coding: utf-8 -*-
"""
Page 3 of App - Netbox Device Discovery

Purpose: to display the results of an Agent's deivce role prediction as an autofill recommender that can be live-trained

"""

# 3rd Party Modules
import numpy as np
import pandas as pd
import streamlit as st

from Main_Page import agent_api_call


def Recommendation_Callback():            
    # Run Agent API
    INPUT = format(manufacturer_id, '010b') + format(type_id, '010b') + format(site_id, '010b')
    label = None
    response = agent_api_call(st.session_state.agent_id, INPUT, label, deployment=st.session_state.Agents[ st.session_state.agent_id ]['deployment'])
    # print("RECOMMENDED - " + response)

    x = int(st.session_state.Agents[ st.session_state.agent_id ]['recs (autocomplete)']) 
    x += 1
    # st.session_state.recs += 1
    try:
        st.session_state.recommendation = roles[response]
        st.write("**Predicted** *Device Role*:  "+ st.session_state.recommendation)
    except KeyError:
        y = int(st.session_state.Agents[ st.session_state.agent_id ]['mistakes (autocomplete)'])
        y += 1
        st.write("Oops, no recommendation to offer; this happened "+str(y)+" out of "+str(x)+" recs so far") 
    st.session_state.Agents[ st.session_state.agent_id ]['recs (autocomplete)'] = str(x)
    st.session_state.Agents[ st.session_state.agent_id ]['mistakes (autocomplete)'] = str(y)


def Confirm_Recommendation_Callback():               
    # Run Agent API
    INPUT = format(manufacturer_id, '010b') + format(type_id, '010b') + format(site_id, '010b')
    LABEL = format(role_id, '010b')
    response = agent_api_call(st.session_state.agent_id, INPUT, label=LABEL, deployment=st.session_state.Agents[ st.session_state.agent_id ]['deployment'])
    # print("CONFIRMED - " + response)
    st.session_state.print_confirm = True


# Streamlit-powered frontend
st.title('Add a New Device -- with AI Agent Assistance')
if "side_bar_content" in st.session_state: exec(st.session_state.side_bar_content)
else:
    with st.sidebar:
        st.write("*Go to the Main Page to start*")

left_big, right_big = st.columns([0.7, 0.3])

with right_big:
    st.image("https://i.imgur.com/4ufNVr1.png")
    st.markdown("*Screenshot from demo.netbox.dev/dcim/devices/add/*")    
    # with st.expander("See Agent's Arch (Configuration)"):
    #     arch_visual_miro_html= """<iframe width="768" height="432" src="https://miro.com/app/live-embed/uXjVM_kESvI=/?moveToViewport=121907,-48157,16256,9923&embedId=323274877415" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>"""
    #     st.write(arch_visual_miro_html, unsafe_allow_html=True)

with left_big:
    st.write("*Conceived as an autocomplete solution for the [add a new device page on Netbox](https://demo.netbox.dev/dcim/devices/add/)*.")
    st.write("")
    st.write("")
    
    if 'trained' not in st.session_state:
        st.text("You have to connect your Netbox account and an Agent first.")
    else:    
        deployment = st.session_state.Agents[ st.session_state.agent_id ]['deployment']
        # generate table of devices to be added / recommended    
        if st.session_state.account_added is True:
            test_devices = st.session_state.test_devices_in
            test_devices_table = np.zeros([len(test_devices), 4], dtype='O')
            for i in range(len(test_devices)):
                d = test_devices[i]
                test_devices_table[i, 0] = d.__str__()
                test_devices_table[i, 1] = d.device_type.manufacturer.__str__()
                test_devices_table[i, 2] = d.site.__str__()
                test_devices_table[i, 3] = d.device_type.__str__()
            st.session_state.test_devices_table = pd.DataFrame( test_devices_table, columns=['Name', 'Manufacturer', 'Site', 'Type'])
            st.markdown("Imagine you're given a list of new device to add to your Netbox account.")
            st.markdown("Your Agent is ready to help by predicting what :blue[Role] new devices are likely to have given your current set up of devices.")
            st.markdown(":red[If your Agent makes a mistake], you can train it on the correct information when you properly add the device as Agents learn without a distinct gap between training and inference.")
            st.write(st.session_state.test_devices_table)
            st.write("")
    
        # load session data
        manufacturers = st.session_state.manufacturers
        roles = st.session_state.roles
        sites = st.session_state.sites
        types = st.session_state.device_types  
    
        # USER input fields    
        st.write("### Enter New Device Info:")
        manufacturer_selected = st.selectbox('Manufacturer', list(manufacturers.values()))
        site_selected = st.selectbox('Site', list(sites.values()))
        type_selected = st.selectbox("Type", list(types.values()))
        role_selected = st.selectbox('Device Role', list(roles.values()))
    
        #converting user input to IDs
        manufacturer_id = list(manufacturers.keys())[list(manufacturers.values()).index(manufacturer_selected)]
        site_id = list(sites.keys())[list(sites.values()).index(site_selected)]
        type_id = list(types.keys())[list(types.values()).index(type_selected)]
        role_id = list(roles.keys())[list(roles.values()).index(role_selected)]
        
        # recommend a device whenever any input changes on this page
        Recommendation_Callback()
    
        # offer USER ability to confirm recommendation and postively reinforce Agent    
        st.write("")
        st.button("Confirm Device & Add to Agent's Training", on_click= Confirm_Recommendation_Callback)
        if 'print_confirm' in st.session_state:
            if st.session_state.print_confirm is True: st.write(":blue[Device added] & :violent[Agent has been trained]")
        st.session_state.print_confirm = False