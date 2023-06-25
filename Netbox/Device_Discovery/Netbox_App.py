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
st.session_state.api_key = api_key


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
    page_title="Netbox Demo App Powered by aolabs.ai",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "mailto:ali@aolabs.ai",
        'Report a bug': "mailto:ali@aolabs.ai",
        'About': "This is a demo of our AI features. Check out www.aolabs.ai and www.docs.aolabs.ai for more. Thank you!"
    }
)

# app front end
st.title('Netbox Demo - powered by aolabs.ai')
st.write("")
st.markdown("## Add Your Netbox Account")
st.markdown("Please enter the information below and then click the **Add Netbox Account** button to get started with this demo.")

# USER inputs
st.session_state.nb_USER_url = st.text_input('Enter your Netbox account URL:', "https://demo.netbox.dev/")    ## Note to Shane -- well done with the default text here! while looking up how you were using st.text_input, i see they also have a password option, see line below
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
    devices = list(nb.dcim.devices.all())[0: st.session_state.USER_num_total_devices ]

    #dictionary comprehensions that map ids to strings, for device name, mfg, type, site, and role
    st.session_state.device_ids    = {d.id : d.__str__() for d in devices}    #  to map device id to device name
    st.session_state.manufacturers = {d.device_type.manufacturer.id : d.device_type.manufacturer.__str__() for d in devices}
    st.session_state.device_types  = {d.device_type.id : d.device_type.__str__() for d in devices}
    st.session_state.sites         = {d.site.id : d.site.__str__() for d in devices}
    st.session_state.device_roles  = {d.device_role.id : d.device_role.__str__() for d in devices}
        
    # for demo performance snapshot, seperate into training and testing sets
    test_size = st.session_state.USER_num_test_devices
    np.random.shuffle(devices)
    test_devices_in = devices[:test_size]
    train_devices_in = devices[test_size:]
    st.session_state.test_devices_in = test_devices_in
    
    # call API in a loop for all TRAIN devices with labels 
    count = 0
    for d in train_devices_in:
        INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')
        LABEL = format(d.device_role.id, '010b')

        # call API
        response = agent_api_call(st.session_state.agent_id, INPUT, api_key, label=LABEL)

        print("trained on device {} with status code {}".format(count, response))
        count += 1
    
    # call API in loop for all TEST devices WITHOUT LABELS
    test_devices_out_roles = list(range(len(test_devices_in)))
    correct_count = 0
    noguess_count = 0
    for i in list(range(len(test_devices_in))):
        d = test_devices_in[i]
        INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')

        # call API
        response = agent_api_call(st.session_state.agent_id, INPUT, api_key)
        story = response.json()['story']

        expected = format(d.device_role.id, '010b')
        if expected == story:
            correct_count += 1
        # to convert binary output of Agent back to role ID and, via the role dict, the role name
        try: 
            test_devices_out_roles[i] = st.session_state.device_roles[int(story, 2)]
        except KeyError:  # if role ID guessed by Agent does not exist
            test_devices_out_roles[i] = "NO GUESS"
            noguess_count += 1    

    # save accuracy and other info in session to display to netbox visitor
    st.session_state.test_devices_out_roles = test_devices_out_roles
    st.session_state.correct_count = correct_count
    st.session_state.noguess_count = noguess_count

    st.markdown('# Training done')
    
    # Note to Shane -- couldn't get the 2 markdowns below to work, please double chjeck and complete design of this area
#    st.markdown('# predicted correctly for {count}/{total}'.format(count=correct_count, total=st.session_state.USER_num_test_devices))
#    st.markdown('# which is an accuracy of {}%'.format((correct_count/st.session_state.USER_num_test_devices)*100))
    #table of devices, correct labels, and guessed labels? -- Note to Shane -- yes, plus the device mfg, type, and site; see "device_discovery" object in page 2
     # so redesign all the below, all the front end elements       
    st.write("Data successfully loaded, agent is trained from "+st.session_state.nb_USER_url+" via API token: "+st.session_state.nb_USER_api_token)  
    st.write("There are "+str(count)+" devices; "+str(st.session_state.USER_num_test_devices)+" devices were withheld from the agent as test devices.")
    st.write("Please remember to re-click the button below if you change the NB account or number of test devices.")

    st.session_state.nb_account_added = True
    st.session_state.device_discovery = False   # so that device discovery results are refreshed on re-run

else:
    st.write("Add your info to run an Agent")