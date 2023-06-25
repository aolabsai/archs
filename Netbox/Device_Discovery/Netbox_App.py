# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 00:37:29 2022

@author: alebr
"""

# AO Labs Modules
# modified import to import ao_core 
import sys
sys.path.append('/home/shane/Development/Animo-Omnis')
import ao_core as ao

# 3rd Party Modules
import numpy as np
import streamlit as st

#api requests
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


# Application-Specific Modules
# import pynetbox as pynb

# nb = pynb.api(
#     'https://demo.netbox.dev',
#     token='18001f2de10ec5bae0d1d2e2614e6f98d427a434',
#     threading=True,
# )

from netbox_ai_app.main_netbox import deviceToIO

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

st.title('Netbox Demo - powered by aolabs.ai')
st.write("")
st.markdown("## Add Your Netbox Account")
st.markdown("Please enter the information below and then click the **Add Netbox Account** button to get started with this demo.")

# st.session_state.nb_USER_url = st.text_input('Enter your Netbox account URL:')
st.session_state.nb_USER_url = st.text_input('Enter your Netbox account URL:', "https://demo.netbox.dev/")
st.session_state.nb_USER_api_token = st.text_input('Enter your Netbox account API token:')
st.session_state.USER_num_test_devices = st.number_input('How many of the devices in this Netbox account would you like to use to test this new Device Discovery Augmentation service?' , 0, 30)
st.session_state.agent_id = st.text_input('enter the id of your agent')


def New_NB_ACCOUNT_Callback():

# if 'nbd' not in st.session_state:
    import pynetbox
    nb = pynetbox.api(
        st.session_state.nb_USER_url,
        token=st.session_state.nb_USER_api_token,
        threading=True,
    )
    devices = list(nb.dcim.devices.all())

    #dictionary comprehensions that map ids to strings
    # dict_manufacturer = {d.device_type.manufacturer.id:d.device_type.manufacturer for d in devices}
    # dict_device_type = {d.device_type.id:d.device_type for d in devices}
    # dict_sites = {d.sites.id:d.site for d in devices}
    manufacturers = {}
    device_types = {}
    sites = {}
    roles = {}
    
    
    for d in devices:
    # for i in range(len(devices)):
    #     d = devices[i]
        manufacturers[d.device_type.manufacturer.id] = d.device_type.manufacturer.__str__()
        device_types[d.device_type.id] = d.device_type.__str__()
        sites[d.site.id] = d.site.__str__()
        roles[d.device_role.id] = d.device_role.__str__()
    
    #save dictionaries to session_state
    st.session_state.manufacturers = manufacturers
    st.session_state.device_types = device_types
    st.session_state.sites = sites
    st.session_state.roles = roles

    
    
    
    # test_devices_in = np.random.choice(len(devices), st.session_state.USER_num_test_devices, replace=False)
    # test_devices_in = np.random.choice(devices, st.session_state.USER_num_test_devices, replace=False)
    # train_devices_in = np.delete( np.arange(len(devices)), test_devices_in)
    # train_devices_in = np.setdiff1d(devices, test_devices_in)
    # choices = np.random.choice(len(devices), st.session_state.USER_num_test_devices, replace=False)
    # print(choices)
    # test_devices_in = np.copy(devices[choices])
    # train_devices_in = np.delete(devices, choices)
    test_size = st.session_state.USER_num_test_devices
    np.random.shuffle(devices)
    test_devices_in = devices[:test_size]
    train_devices_in = devices[test_size:]

    st.session_state.test_devices_in = test_devices_in
    

    # print(devices[0])
    # call API in a loop for all TRAIN devices with labels
    count = 0
    prog_bar = st.progress(0, text="Training Progress")
    for d in train_devices_in:
        INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')
        # TypeError: unsupported format string passed to DeviceTypes.__format__
        LABEL = format(d.device_role.id, '010b')

        # call API
        response = agent_api_call(st.session_state.agent_id, INPUT, api_key, label=LABEL)

        print("trained on device {} with status code {}".format(count, response))
        count += 1
        prog_bar.progress(float(count)/len(train_devices_in), text='Training Progress')

    # display training is DONE message
    st.write('Training done')
    # prompt click from user to move along (to next page or a button appears on for loop completion appears)

    # call API in loop for all TEST devices WITHOUT LABELS
        # similar to above
        
    # test_devices_out = np.arange(len(train_devices_in))
    # correct_count = 0
    # for i in range(len(test_devices_in)):
    #     d = test_devices_in[i]
    # for d in test_devices_in:
        # INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')
        # response = agent_api_call(st.session_state.agent_id, INPUT, api_key)
        # story = response.json()['story']
        # np.append(test_devices_out, story)

        # expected = format(d.device_role.id, '010b')
        # if expected == story:
        #     correct_count += 1

    # save accuracy and other info in session to display to netbox visitor
    # st.session_state.correct_count = correct_count
    
    # make it all look pretty and explainable
    # st.markdown('# predicted correctly for {count}/{total}'.format(count=correct_count, total=st.session_state.USER_num_test_devices))
    # st.markdown('# which is an accuracy of {}%'.format((correct_count/st.session_state.USER_num_test_devices)*100))
    #table of devices, correct labels, and guessed labels?

    # prompt visitor to clone this app and associated agent
    
    ## next up
    # add history vibility
        # raw and per neuron, see how it's displayed in basic clam demo app
    
    ## bonus
    # add new devices, on click of button, re-trains agent

#%%
def deviceToIO(d):
    info = {
        'id': d.id,
        'idBin': format(d.id, '010b'),
        'type': d.device_type.id,
        'typeBin': format(d.device_type, '010b'),
        'manufacturer': d.device_type.manufacturer.id,
        'manufacturerBin': format(d.device_type.manufacturer.id, '010b'),
        'site': d.site.id,
        'siteBin': format(d.site.id, '010b'),
        'role': d.device_role.id,
        'roleBin': format(d.device_role.id, '010b'),
    }
    return info

#%%
        
    
    arraySize = 10
    
    # map binary strings to ids
    roles = {}
    manufacturers = {}
    sites = {}
    types = {}
    roles_id_to_str = {}
    
    devices_array_IO = np.zeros(4000, dtype='O')
    devices_info = np.zeros([4000, 5], dtype='O')
        
    inc = 0
    #populate devices array
    for device in devices:

        devices_array_IO[inc] = deviceToIO(device, arraySize)
        
        devices_info[inc, 0] = str(device)
        devices_info[inc, 1] = str(device.device_type.manufacturer)
        devices_info[inc, 2] = str(device.site)
        devices_info[inc, 3] = str(device.device_type)
        devices_info[inc, 4] = str(device.device_role)
   
        #add device data to sets so they can be options in text boxes
        roles[str(device.device_role)] = device.device_role.id
        manufacturers[str(device.device_type.manufacturer)] = device.device_type.manufacturer.id
        sites[str(device.site)] = device.site.id
        types[str(device.device_type)] = device.device_type.id
    
        roles_id_to_str[device.device_role.id] = str(device.device_role)    
    
        # count number of devices
        inc += 1

    devices_array_IO = devices_array_IO[0:inc]
    devices_info = devices_info[0:inc, :]

    test_devices_in = np.random.choice(inc, st.session_state.USER_num_test_devices, replace=False)    
    train_devices_array_IO = np.delete(devices_array_IO, test_devices_in)
    test_devices_array_IO = np.copy(devices_array_IO[test_devices_in])    
    test_devices_info = np.copy(devices_info[test_devices_in, :])
               
    nbd = {
        "roles": roles,
        "manufacturers" : manufacturers,
        "sites" : sites,
        "types" : types,
        "roles_id_to_str" : roles_id_to_str,
        "inc" : inc,
        "train_devices_array_IO" : train_devices_array_IO,
        "test_devices_array_IO" : test_devices_array_IO,
        "test_devices_info" : test_devices_info,
        }

# if 'agent' not in st.session_state:
    # configure architecture
    from netbox_ai_app import arch_netbox
    arch = arch_netbox.arch

    # create agent
    arch.full_conn()
    agent = ao.Agent(arch)

    #train agent
    for d in train_devices_array_IO:
        agent.next_state(d['manufacturerBin'] + d['siteBin'] + d['typeBin'],
                    d['roleBin'], print_result=False, unsequenced=True)
        agent.reset_state()

    #save data to session

    st.session_state.nbd = nbd

    st.session_state.agent = agent    

    st.session_state.mistakes = 0
    st.session_state.mistakes_batch = 0
    st.session_state.recs = 0
    st.session_state.test_devices_roles_PREDICTED = 0


st.write("")
st.button("Add Netbox Account", on_click= New_NB_ACCOUNT_Callback)


if 'nbd' not in st.session_state:
    pass
else:
    st.write("Data successfully loaded, agent is trained from "+st.session_state.nb_USER_url+" via API token: "+st.session_state.nb_USER_api_token)  
    st.write("There are "+str(st.session_state.nbd['inc'])+" devices; "+str(st.session_state.USER_num_test_devices)+" devices were withheld from the agent as test devices.")
    st.write("Please remember to re-click the button below if you change the NB account or number of test devices.")