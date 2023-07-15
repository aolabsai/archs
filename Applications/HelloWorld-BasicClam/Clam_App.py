# -*- coding: utf-8 -*-
"""
Main Page - Basic Clam Test Bed

@author: aolabs.ai
"""

# 3rd Party Modules
import numpy as np
import streamlit as st
import requests
from PIL import Image
from urllib.request import urlopen


# Returns json, result stored in json as Agent's 'story'
def agent_api_call(agent_id, input_dat, label=None):
    url = "https://7svo9dnzu4.execute-api.us-east-2.amazonaws.com/v0dev/kennel/agent"

    payload = {
        "kennel_id": "v0dev/TEST-BedOfClams",
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
        "X-API-KEY": st.secrets["aolabs_api_key"]
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


# App Front End
st.title('AO Labs v0.1.0 Clam Demo')
url = "https://i.imgur.com/cTHLQYL.png"
img = Image.open(urlopen(url))
st.image(img)
st.markdown("*Note: This app is not yet a standalone experience; please visit [this guide for more context](https://docs.google.com/document/d/1cUmTXsf7bCIMGKm3RHn001Qya-tZcFTvgCPj4Ynu2_M/edit).*")
st.write("")
st.write("")
st.write("")

st.write("First, name your Clam Agent.")
st.write(" Agents maintain persistant state and are auto-provisioned through our API (or you can also try a version of this demo with the Agent loaded in the browser session.")
def New_Agent():
    st.session_state.agent_id = agent
    st.session_state.agent_results = np.zeros( (100,  5), dtype='O')
    st.session_state.agent_trials = 0
agent = st.text_input('Agent Name', value='1st of Clams', on_change=New_Agent)
if agent == '1st of Clams' and 'agent_id' not in st.session_state: New_Agent()    
st.write("The current Agent is::::", agent)
st.write("")
st.markdown('#')
st.markdown('##')

st.write("STEP 0) Activate learning:")
instincts_ONOFF = st.checkbox('Instincts On')
labels_ONOFF = st.checkbox('Labels On')
if labels_ONOFF & instincts_ONOFF is True: st.write('Note: the presence of labels overrides any instinctual learning.')
LABEL = None
if labels_ONOFF is True:
    labels_CHOICE = st.radio('Pick one', ['OPEN the Clam', 'CLOSE the Clam'])
    if labels_CHOICE == 'OPEN the Clam': LABEL = 1
    if labels_CHOICE == 'CLOSE the Clam': LABEL = 0
st.write("")

user_INPUT = st.multiselect("STEP 1) Show the Clam this input:", ['FOOD', 'A-CHEMICAL', 'C-CHEMICAL'])
user_STATES = st.slider('This many times', 1, 10)
st.write("")
st.write("")

st.write("STEP 2) Run Trial: "+str(st.session_state.agent_trials))
if user_STATES == 1:button_text= 'Expose Clam ONCE'
if user_STATES > 1: button_text= 'Expose Clam '+str(user_STATES)+' times'

# Run the Agent Trial
def run_agent():

    # INPUTS
    INPUT = [0, 0, 0]
    if 'FOOD'       in user_INPUT: INPUT[0] = 1
    if 'A-CHEMICAL' in user_INPUT: INPUT[1] = 1
    if 'C-CHEMICAL' in user_INPUT: INPUT[2] = 1
    
    responses = []
    for x in np.arange(user_STATES):
        response= agent_api_call(st.session_state.agent_id, INPUT, label=LABEL)        
        print(response)
        print([int(response.json()['story'])])
        responses += [int(response.json()['story'])]

    # save trial results for dispplaying to enduser    
    final_totals = sum(responses) / user_STATES * 100
    if labels_ONOFF == True: Label_Insti = "LABEL"
    elif instincts_ONOFF == True: Label_Insti = "INSTI"
    else: Label_Insti ="NONE"
    st.session_state.agent_results[st.session_state.agent_trials, :] = ["Trial #"+str(st.session_state.agent_trials), INPUT, user_STATES, Label_Insti, str(final_totals)+"%"]    
    
    st.session_state.agent_trials += 1

if user_STATES == 1: button_text= 'Expose Clam ONCE'
if user_STATES > 1: button_text= 'Expose Clam '+str(user_STATES)+' times'
st.button(button_text, on_click=run_agent)

# Display Trial Log Results
display_trial = st.session_state.agent_trials-1
print(display_trial)
if display_trial == -1: pass
else:
    st.write("**Trial #"+str(display_trial)+" Results Summary**: You exposed the Clam Agent to "+str(st.session_state.agent_results[display_trial, 1])+' as input for '+str(st.session_state.agent_results[display_trial, 2])+'   times with learning mode '+str(st.session_state.agent_results[display_trial, 3])+'.')
    if (st.session_state.agent_results[display_trial, -1]) == "0%":
        if LABEL == 0: st.write("As you commanded, the Clam remained CLOSED, and learned to do so for the input you set.")
        else: st.write("The Clam didn't open at all. :(  Give it some food with this chemical and see how its behavior changes.")
    else:
        if LABEL == 1: st.write("As you ordered, the Clam was OPEN, and learned to do so for the input you set.")
        else: st.write('The Clam OPENED  '+st.session_state.agent_results[display_trial, -2]+' of the time.')
st.write("")
st.write('## Trial Results')
st.text(str(st.session_state.agent_results[0:st.session_state.agent_trials, :]))  