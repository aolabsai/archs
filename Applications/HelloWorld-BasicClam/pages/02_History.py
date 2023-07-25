# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 12:55:14 2022

@author: alebr
"""

# 3rd Party Modules
import numpy as np
import streamlit as st


# Returns json, result stored in json as Agent's 'story'
def agent_api_call_history_request(agent_id, request):

    url = "https://7svo9dnzu4.execute-api.us-east-2.amazonaws.com/v0dev/kennel/agent"

    payload = {
        "kennel_id": "v0dev/TEST-BedOfClams",
        "agent_id": agent_id,
        "request": request,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "buildBottomUpRealAGI" # st.secrets["aolabs_api_key"]
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)
    response = response.json()['story']  # we can print the HTTP response here, too
    return response


# streamlit frontend
st.title('View All Your Agents')
if "side_bar_content" in st.session_state: exec(st.session_state.side_bar_content)
else:
    with st.sidebar:
        st.write("*Go to the Main Page to start*")
st.write("*View all of the Agents you've called during this browser session.*")
st.write("")
st.write("")
if "Agents" in st.session_state:
    if st.session_state.Agents == {}: st.text("You have not created any Agents yet.")
    st.dataframe( pd.DataFrame.from_dict( st.session_state.Agents ) )
else:
    st.text("You have not created any Agents yet.")


Agent_keys = list( st.session_state.Agents.keys() )

Agent = st.selectbox("Select an Agent to View its History:", Agent_keys)



st.title('Clam History')

st.markdown("Sneak peak at an AI program you can classically condition for general behaviors. Guide and details coming soon.  :)")
st.markdown("For now, please visit [aolabs.ai](https://www.aolabs.ai/), [docs.aolabs.ai](https://docs.aolabs.ai/), or contact ali@aolabs.ai.")
# clam_header_image = Image.open(r'./Toy_Clam.png')
# st.image(clam_header_image, caption='Quick Visual')
st.text("")
st.text("")

if st.session_state.Agents[ Agent ]['deployment'] == "API":
    
    mem = 

    st.text("Please spin up a Agent Locally to view its history (We haven't expose Agent history in our API yet).")

else:
    Agent = st.session_state.Local_Agents[ st.session_state.agent_id ]


    if hasattr(Agent.neurons[3], 'tsets') is not True: st.write("The Clam is still untrained; try exposing it stimulus with LABELS or INSTINCTS activated. Then you'll be able to see the neuron-level histories, too.")
    else:
        with st.expander("Access memory of individual neurons here"):
    
            neuron_SEL= st.selectbox('Pick one', ['Q0', 'Q1', 'Q2', "Z0 (the output neuron)"])
            
            if 'Q0' in neuron_SEL: SEL = 3
            if 'Q1' in neuron_SEL: SEL = 4
            if 'Q2' in neuron_SEL: SEL = 5
            if 'Z0' in neuron_SEL: SEL = 6
                
            neuron_story = Agent.neurons[SEL].tsets.astype(int)
            neuron_outputs = Agent.neurons[SEL].outputs.astype(int)
            
            tcol1, tcol2 = st.columns(2)
            
            with tcol1:
                st.header("Inputs")
                st.write(neuron_story)
                
            with tcol2:
                st.header("Outputs")
                st.write(neuron_outputs)
    
    story = Agent.story[0: Agent.state+1, np.asarray([0, 1, 2, 3, 4, 5, 6, 7, 10])].astype(int)
    
    metastory = Agent.metastory[0: Agent.state+1, np.asarray([0, 1, 2, 3, 4, 5, 6, 7, 10])].astype(str)
     
    col1, col2 = st.columns([1.5, 3])


        # tab1, tab2 = st.tabs(["Story", "Metastory"])
        
    
    with col1:
        st.header("Story")
        st.write(story)
        
    with col2:
        st.header("Metastory")
        st.write(metastory)




left_big, right_big = st.columns([0.5, 0.5])
with left_big:
    st.write("")
    st.image("https://i.imgur.com/n0KciAE.png")

