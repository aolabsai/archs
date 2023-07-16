# -*- coding: utf-8 -*-
"""
Main Page - Netbox Device Discovery

@author: Shane Polisar, aolabs.ai
"""

# 3rd Party Modules
import numpy as np
import streamlit as st
import requests
import pynetbox  # Netbox interface


# Returns json, result stored in json as Agent's 'story'
def agent_api_call(agent_id, input_data, label=None, deployment="Local"):

    if deployment == "API":
        url = "https://7svo9dnzu4.execute-api.us-east-2.amazonaws.com/v0dev/kennel/agent"
        payload = {
            "kennel_id": "v0dev/TEST-Netbox_DeviceDiscovery",
            "agent_id": agent_id,
            "INPUT": input_data,
            "control": {
                "US": True
            }
        }
        if label != None:
            payload["LABEL"] = label
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": st.secrets['aolabs_api_key']
        }
        response = requests.post(url, json=payload, headers=headers)
        response = response.json()['story']  # we can print the HTTP response here, too
        return response

    if deployment == "Local":
        if label == None:
            label = []
        if agent_id not in st.session_state['Local_Agents']:
            agent = st.session_state.Local_Core( st.session_state.Local_Arch )
            st.session_state["Local_Agents"][agent_id] = agent
        else:
            agent = st.session_state['Local_Agents'][agent_id]
        agent.reset_state()
        agent.next_state( list(input_data), list(label), unsequenced=True)
        response = agent.story[ agent.state-1, agent.arch.Z__flat ]
        response = "".join(list(response.astype(str)))
        return response

# to construct and store Local Agents as needed
if "Local_Agents" not in st.session_state:
    st.session_state.Local_Agents = {}

    # preparing Arch Netbox Device Discovery locally 
    from Arch import Arch
    arch = Arch([10, 10, 10], [10], [], "forward_full_conn", "Agent created locally!")
    st.session_state.Local_Arch = arch
    
    # retrieving Agent class locally from Core
    from github import Github, Auth    
    github_auth = Auth.Token(st.secrets["aolabs_github_auth"])
    github_client = Github(auth=github_auth)
    ao_core = github_client.get_repo("aolabsai/ao_core")
    content = ao_core.get_contents("ao_core/ao_core.py")
    exec(content.decoded_content, globals())
    st.session_state.Local_Core = Agent

#save {id: attribute} dicts of device and other info to session_state
def add_netbox():
    manufacturers = {}
    device_types = {}
    sites = {}
    roles = {}    

    nb = pynetbox.api(
        st.session_state.nb_USER_url,
        token= str(st.session_state.nb_USER_api_token),
        threading=True)
    try:
        devices = list(nb.dcim.devices.all())
        st.session_state.account_added = True
        st.session_state.valid_netbox_apikey = True
        st.session_state.num_devices = len(devices)
        st.session_state.devices = devices
        st.session_state.minimum_devices = len(devices) >= 2
        for d in devices:
            manufacturers[d.device_type.manufacturer.id] = d.device_type.manufacturer.__str__()
            device_types[d.device_type.id] = d.device_type.__str__()
            sites[d.site.id] = d.site.__str__()
            roles[d.device_role.id] = d.device_role.__str__()
    except pynetbox.RequestError as e:
        devices = []
        st.session_state.account_added = False
        st.session_state.valid_netbox_apikey = False
        st.session_state.num_devices = 2
        st.session_state.devices = devices        
        print(e)
   
    st.session_state.manufacturers = manufacturers
    st.session_state.device_types = device_types
    st.session_state.sites = sites
    st.session_state.roles = roles

if 'account_added' not in st.session_state:
    st.session_state.num_devices = 2
    st.session_state.account_added = False
    st.session_state.minimum_devices = False
    

# Trains an Agent on a Netbox instance, first shuffling the list of devices, and for this demo perparing subsets of devices for training and testing
def train_agents(deployment):
    devices = st.session_state.devices
    np.random.shuffle(devices)
    
    test_size = st.session_state.USER_num_test_devices
    batch = devices[0:st.session_state.USER_num_total_devices]
    test_devices_in = batch[0:test_size]
    train_devices_in = batch[test_size:]
    st.session_state.test_devices_in = test_devices_in
    st.session_state.train_size = len(train_devices_in)
    
    prog = 0
    prog_bar = st.progress(0, text="Training Progress")
    for d in train_devices_in:
        INPUT = format(d.device_type.manufacturer.id, '010b') + format(d.device_type.id, '010b') + format(d.site.id, '010b')
        LABEL = format(d.device_role.id, '010b')

        # call Agent via API
        response = agent_api_call(st.session_state.agent_id_field, INPUT, label=LABEL, deployment=deployment)
        # print("trained on device {} with status code {}".format(count, response))
        
        prog += 1
        prog_bar.progress(float(prog)/len(train_devices_in), text='Training Progress')
    # display training is DONE message
    prog_bar.progress(1.0, text='Training Complete')

    st.session_state.agent_id = st.session_state.agent_id_field
    st.session_state.trained = True
    st.session_state.tested = False
    st.session_state.recs = 0
    st.session_state.mistakes = 0
    
    Agent = {
        'deployment': deployment,
        'trained': str(st.session_state.trained)+" - "+str(len(train_devices_in)),
        'tested (bulk)': str(st.session_state.tested)+" - "+str(test_size),
        'accuracy (bulk)': "",
        'no guesses (bulk)': "",
        'recs (autocomplete)': str(0),
        'mistakes (autocomplete)': str(0),
        }
    st.session_state.Agents[ st.session_state.agent_id ] = Agent


# Streamlit-powered frontend
st.set_page_config(
    page_title="Local Device Discovery AI Agent - demo by aolabs.ai",
    page_icon="https://i.imgur.com/j3jalQE.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "mailto:ali@aolabs.ai",
        'Report a bug': "mailto:ali@aolabs.ai",
        'About': "This is a demo of our AI features. Check out www.aolabs.ai and docs.aolabs.ai for more. Thank you!"
    }
)
st.title('Local AI Agents for Netbox Device Discovery')
st.write("### *a demo by [aolabs.ai](https://www.aolabs.ai/)*")
st.write("")

# side bar content
st.session_state.side_bar_content = """
if "Agents" not in st.session_state:
    st.session_state["Agents"] = {}
if 'account_added' in st.session_state:
    if st.session_state.account_added is False: data_source = "**Data Source:** :red[*Connect a Netbox Account*]" 
    elif st.session_state.account_added: data_source = "**Data Source:** :green["+st.session_state.nb_USER_url+"]"    
if 'agent_id' not in st.session_state:
    active_agent = "**Current Agent:** :red[*No Agent(s) Yet*]"
    agent_deployment = ""
else:
    active_agent = "**Current Agent:** :violet["+st.session_state.agent_id+"]"
    agent_deployment = "Agent deployed :blue["+st.session_state.Agents[st.session_state.agent_id]['deployment']+"]"
with st.sidebar:    
    st.write(data_source)
    st.write(active_agent)
    st.write(agent_deployment)
st.sidebar.image("https://raw.githubusercontent.com/netbox-community/netbox/develop/docs/netbox_logo.svg", use_column_width=True)"""
exec(st.session_state.side_bar_content)
    
left_big, right_big = st.columns([0.7, 0.3])

with right_big:
    st.image("https://i.imgur.com/eZyVouO.png")
    st.markdown("*The Netbox Devices UI at [demo.netbox.dev/dcim/devices/](https://demo.netbox.dev/dcim/devices/)*", help="Login with username **admin** and password **admin**.")

with left_big:
    instruction_md = """### Welcome! How this works: \n
* Connect an unique Agent to a Netbox account (by entering a Netbox url and API token; you can use the [public Netbox demo](https://demo.netbox.dev/))\n
* Train your Agent on the account's local list of **Network Devices'** **:green[Manufacters]**, **:green[Types]**, and **:green[Sites]** to infer the ***:blue[Roles]*** of newly discovered devices and supplement manual role assignment\n
* Agents are not pre-trained on any other data and can live in state with your list of devices if used in your application; this demo presented a snapshot\n
* After entering the info below to train an Agent, view its predictions in the sidebar as a *bulk import service* or as a *context-aware auto-complete*"""
    st.markdown(instruction_md)
    st.write("---")
    
    # Capture USER inputs
    left, right = st.columns(2)
    
    ## Netbox account
    with left:
        st.session_state.nb_USER_url = st.text_input('Enter your Netbox account URL:', "https://demo.netbox.dev/")
        help_netbox_api = "If you don't have a Netbox account, you can a get temporary API token by logging in to the [Netbox public demo instance](https://demo.netbox.dev/user/api-tokens/) with username *admin* and password *admin*."
        st.session_state.nb_USER_api_token = st.text_input('Enter your Netbox account API token:',  type='password', help=help_netbox_api)
    
        left_filled = len(st.session_state.nb_USER_url) > 0 and len(st.session_state.nb_USER_api_token) > 0
        st.button("Connect Netbox Account", type="primary", on_click=add_netbox, disabled=not(left_filled))
           
        if 'account_added' in st.session_state:
            if st.session_state.account_added is True:
                st.write(":green[Netbox Account Successfully Connected]; there {} devices on this Netbox account available for training/testing.".format(st.session_state.num_devices))
            
        if 'valid_netbox_apikey' in st.session_state:
            if st.session_state.valid_netbox_apikey is False:
                st.write(":red[Invalid Netbox API Key--] *please try again*.")
    
    ## Training and test configuration
    with right:
        st.session_state.USER_num_total_devices = st.number_input("How many of the available devices in this Netbox account would you like to use for this demo?" , min_value=2, max_value=st.session_state.num_devices, disabled=not(st.session_state.account_added))
        x = st.session_state.USER_num_total_devices
        max_test_devices = x-1
        help_numtest = "The rest of the devices will be used for training the Agent."
        st.session_state.USER_num_test_devices = st.number_input("Of those ("+str(x)+") devices, how many should be withheld to TEST the Agent?" , min_value=1, max_value=max_test_devices, disabled=not(st.session_state.account_added), help=help_numtest)
        st.session_state.agent_id_field = st.text_input("Enter a unique name for this Agent", disabled=not(st.session_state.account_added))
    
        right_filled = len(st.session_state.agent_id_field) > 0
        st.button("Deploy & Train Your Agent [:violet[locally]]",type="primary", on_click=train_agents, disabled=not(st.session_state.account_added) or not(right_filled) or not(st.session_state.minimum_devices), args= ("Local",), help="The Agent will be running in the Streamlit browser session; Agents are by design lightweight enough to run on the edge")
        st.button("Deploy & Train Your Agent [:blue[via our API]]", type="primary", on_click=train_agents, disabled=not(st.session_state.account_added) or not(right_filled) or not(st.session_state.minimum_devices), args = ("API",), help="We'll host your Agent on our AWS via our API, so you can even invoke this Agent from anywhere else https://docs.aolabs.ai/reference/agentinvoke")


# Post training message
if 'trained' in st.session_state:
    st.write('***:violet[Agent Training Complete]***')
    st.write("From "+st.session_state.nb_USER_url+" via API token: ..."+st.session_state.nb_USER_api_token[-6:])  
    device_count = st.session_state.train_size + len(st.session_state.test_devices_in)
    st.write("")
    st.write("- {num_devices} devices were used\n- {num_train} for training the Agent\n- {num_test} for testing".format(num_devices=device_count, num_train=st.session_state.train_size, num_test=len(st.session_state.test_devices_in)))
    st.write("View the Agent's performance by clicking the pages in the sidebar.")