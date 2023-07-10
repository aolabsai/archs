# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 00:37:29 2022

@author: alebr
"""


# 3rd Party Modules
import numpy as np
import streamlit as st

from PIL import Image
from urllib.request import urlopen


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




url2 = "https://i.imgur.com/j3jalQE.png"
favicon = Image.open(urlopen(url2))

st.set_page_config(
    page_title="AO Labs Demo App",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "mailto:ali@aolabs.ai",
        'Report a bug': "mailto:ali@aolabs.ai",
        'About': "This is a demo of our AI features. Check out www.aolabs.ai and www.docs.aolabs.ai for more. Thank you!"
    }
)



#%% # Constructing a Clam agent

if 'agent' not in st.session_state:
            
    # training Agent on I = 000 <> Z = 0 -- being closed for 0 inputs
    INPUT = '000'
    LABEL = '0'
    response = agent_api_call(agent_id, INPUT, api_key, label=LABEL)

    agent_results = np.zeros( (200,  6), dtype='O')
    st.session_state.agent_results = agent_results
    
    # Creating an agent
    bc = ao.Agent( arch, "basic clam, 11 neurons (3-I, 3-Q, 1-Z, 4-C)")

    bc.trials = 1
    
    st.session_state.agent = bc

if 'agent_results' not in st.session_state:
    agent_results = np.zeros( (200,  6), dtype='O')

    # agent_results[0, :] = ["Trial #0", [0, 0, 0], 3, "LABEL", "0%", "All 0s"]

    st.session_state.agent_results = agent_results

# #%% # Running on agent


final_totals = ""




# App Front End
st.title('AO Labs v0.1.0 Clam Demo')

url = "https://i.imgur.com/cTHLQYL.png"
img = Image.open(urlopen(url))
st.image(img)

st.markdown("*Note: This app is not yet a standalone experience; please visit [this guide for more context](https://docs.google.com/document/d/1cUmTXsf7bCIMGKm3RHn001Qya-tZcFTvgCPj4Ynu2_M/edit).*")
st.write("")
st.write("")
st.write("")

st.write("STEP 0) Activate learning:")
instincts_ONOFF = st.checkbox('Instincts On')
labels_ONOFF = st.checkbox('Labels On')

if labels_ONOFF & instincts_ONOFF is True:
    st.write('Note: the presence of labels overrides any instinctual learning.')

LABEL = None
if labels_ONOFF is True:
    labels_CHOICE = st.radio('Pick one', ['OPEN the Clam', 'CLOSE the Clam'])
    if labels_CHOICE == 'OPEN the Clam': LABEL = 1
    if labels_CHOICE == 'CLOSE the Clam': LABEL = 0

st.write("")
user_INPUT = st.multiselect("STEP 1) Show the Clam this input:", ['FOOD', 'A-CHEMICAL', 'C-CHEMICAL'])

user_STATES = st.slider('This many times', 1, 100)

clam_INPUT = np.zeros( st.session_state.agent.arch.I__flat.shape ) 


def run_agent():
        
    if 'FOOD'       in user_INPUT: clam_INPUT[0] = 1
    if 'A-CHEMICAL' in user_INPUT: clam_INPUT[1] = 1
    if 'C-CHEMICAL' in user_INPUT: clam_INPUT[2] = 1
            
    start_state = st.session_state.agent.state
    
    for x in np.arange(user_STATES):
        
        st.session_state.agent.next_state( clam_INPUT, LABEL, DD=False, INSTINCTS=instincts_ONOFF, unsequenced=True)      # compare response of {0 1 0}
                                                                # to response of {0 0 1} 
        st.session_state.agent.reset_state()
     
    end_state = st.session_state.agent.state
    
    sel = np.arange( start_state, end_state, 2)
    raw_results = st.session_state.agent.story[np.ix_(sel, st.session_state.agent.arch.Z__flat)]
    
    aresults_totals = np.sum(raw_results, 1)
    
    final_totals = np.asarray(np.unique(aresults_totals, return_counts=True))
    final_totals[1] = final_totals[1]/user_STATES*100


    if labels_ONOFF == True: Label_Insti = "LABEL"
    elif instincts_ONOFF == True: Label_Insti = "INSTI"
    else: Label_Insti ="NONE"



    st.session_state.agent_results[st.session_state.agent.trials, :] = ["Trial #"+str(st.session_state.agent.trials), clam_INPUT, user_STATES, Label_Insti, str(final_totals[1, -1])+"%", final_totals]
    
    st.session_state.agent.trials += 1


ttrial = st.session_state.agent.trials-1

st.write("")
st.write("")
st.write("STEP 2) Run Trial: "+str(st.session_state.agent.trials)+"  ___ at Clam state: "+str(st.session_state.agent.state))
# st.write('Trial #: '+str(st.session_state.agent.trials))
# st.write('Clam state #: '+str(st.session_state.agent.state))


if user_STATES == 1: button_text= 'Expose Clam ONCE'
if user_STATES > 1: button_text= 'Expose Clam '+str(user_STATES)+' times'

st.button(button_text, on_click=run_agent)


# if st.session_state.agent.trials == 1 or st.session_state.agent.trials : pass
if st.session_state.agent.trials == 1: pass
elif ttrial == 0 & ttrial < 0: pass
else:
    st.write(str(st.session_state.agent_results[st.session_state.agent.trials-1, 0])+" RESULTS: You exposed the clam to "+str(st.session_state.agent_results[st.session_state.agent.trials-1, 1])+' as input for '+str(st.session_state.agent_results[st.session_state.agent.trials-1, 2])+'   times with learning mode '+str(st.session_state.agent_results[st.session_state.agent.trials-1, 3])+'.')
    if (st.session_state.agent_results[ttrial, -1][0, -1]) == 0:
        st.session_state.agent_results[ttrial, -2] = "0%"
        if LABEL == 0: st.write("As you commanded, the Clam remained CLOSED, and learned to do so for the input you set.")
        else: st.write("The Clam didn't open at all. :(  Give it some food with this chemical and see how its behavior changes.")
    else:
        if LABEL == 1: st.write("As you ordered, the Clam was OPEN, and learned to do so for the input you set.")
        else: st.write('The Clam OPENED  '+str(st.session_state.agent_results[ttrial, -2]+' of the time.'))


st.write('')
st.write('## Trial Results')

st.text(str(st.session_state.agent_results[0:st.session_state.agent.trials, 0:-1]))  

