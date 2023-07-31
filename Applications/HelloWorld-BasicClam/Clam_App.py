# -*- coding: utf-8 -*-
"""
Main Page - Basic Clam Test Bed

@author: aolabs.ai
"""

# 3rd Party Modules
import numpy as np
import streamlit as st
import requests



def agent_api_call(agent_id, input_data, label=None, deployment="Local"):

    if deployment == "API":
        url = "https://7svo9dnzu4.execute-api.us-east-2.amazonaws.com/v0dev/kennel/agent"
    
        payload = {
            "kennel_id": "v0dev/TEST-BedOfClams",
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
            "X-API-KEY": "buildBottomUpRealAGI" # st.secrets["aolabs_api_key"]
        }
    
        response = requests.post(url, json=payload, headers=headers)
        print(response)    
        response = response.json()['story']  # we can print the HTTP response here, too
        return response

    if deployment == "Local":
        if label == None:
            label = []
        agent = st.session_state.Local_Agents[agent_id]
        agent.reset_state()
        agent.next_state( list(input_data), [label], unsequenced=True)
        response = agent.story[ agent.state-1, agent.arch.Z__flat ]
        response = "".join(list(response.astype(str)))
        print("from api call func" + response)
        return response

if "Local_Agents" not in st.session_state:
    # to construct and store Local Agents as needed
    st.session_state.Local_Agents = {}

    # preparing Arch Netbox Device Discovery locally 
    from Arch import Arch
    arch = Arch([1, 1, 1], [1], [], "full_conn", "Clam Agent created locally!")
    st.session_state.Local_Arch = arch
    
    # retrieving Agent class locally from Core
    from github import Github, Auth    
    github_auth = Auth.Token(st.secrets["aolabs_github_auth"])
    github_client = Github(auth=github_auth)
    ao_core = github_client.get_repo("aolabsai/ao_core")
    content = ao_core.get_contents("ao_core/ao_core.py")
    exec(content.decoded_content, globals())
    st.session_state.Local_Core = Agent
    # import ao_core as ao
    # st.session_state.Local_Core = ao.Agent

st.set_page_config(
    page_title="AO Labs Demo App",
    page_icon="https://i.imgur.com/j3jalQE.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "mailto:ali@aolabs.ai",
        'Report a bug': "mailto:ali@aolabs.ai",
        'About': "This is a demo of our AI features. Check out www.aolabs.ai and www.docs.aolabs.ai for more. Thank you!"
    }
)

# App Front End
st.title('Hello, World! A Clam-Level General Intelligence')
st.write("### *a demo by [aolabs.ai](https://www.aolabs.ai/)*")

# side bar content
st.session_state.side_bar_content = """
if "Agents" not in st.session_state:
    st.session_state["Agents"] = {}
if 'agent_id' not in st.session_state:
    active_agent = "**Current Agent:** :red[*No Agent(s) Yet*]"
    agent_deployment = ""
    agent_state = ""
else:
    active_agent = "**Current Agent:** :violet["+st.session_state.agent_id+"]"
    agent_deployment = "**Agent Deployment:** :blue["+st.session_state.Agents[st.session_state.agent_id]['deployment']+"]"
    agent_state = "**Agent State:** :green["+st.session_state.Agents[st.session_state.agent_id]['state']+"]"
with st.sidebar:    
    st.write(active_agent)
    st.write(agent_deployment)
    # st.write(agent_state)
st.sidebar.image("https://i.imgur.com/n0KciAE.png", use_column_width=True)"""
exec(st.session_state.side_bar_content)


with st.expander("About & Context", expanded=True):
    
    left_big_top, right_big_top = st.columns([0.5, 0.5])
    
    with left_big_top:
        st.image("https://i.imgur.com/EiFhojY.png", caption="Clams are smarter than we think!")
    
    with right_big_top:
        st.markdown("""
        ### Did you know that :blue[clams] can be trained like dogs and other animals? \n
        They can learn to associate outputs, opening or closing, to different input patterns. For instance, clams in captivity can learn to remain open around shadows [[source](https://dantheclamman.blog/2019/06/02/thoughts-of-a-clam/#:~:text=When%20a%20certain,do%20my%20work.)].\n
        This intuitive type of cognition, so obvious in animals but so far neglected in AI, has 3 main advantages that deep learning lacks: \n
        * Continous learning:  no gap between training and inference \n
        * Fully transparency: learned behavior can be traced back to training history or how its been conditioned\n
        * Self-grounding: learned behavior can never be out-of-distribution from training history \n
        """)
    
    st.write("")
    st.write("")
    st.write("")
        
    st.markdown("""
    This is a demo of the simplest form of this function, a thought experiment of a 3-input and single-output clam. The 3 inputs the Clam can sense are Chemical-A and Chemical-B, which start of as neutral inputs, and Food, which in the clam is configured to trigger positive association between input and output. The output is opening or closing. \n
    Can you bend the Clam Agent to your will? Can you grok the potential here?\n
    Can you imagine training in this way an even more capable Agent, one with a greater number of input-outputs to learn to associate?  \n
    We're building more complex Agents and at the same time making them useful in applications; a scaled up version of the 4-neuron Clam Agent demonstated here is solving for [network device discovery](https://aolabs-netbox.streamlit.app/).  \n
    """)
    

st.title("Clam Test Bed - v0.1.1")

left_big_bottom, right_big_bottom = st.columns([0.6, 0.4])

with right_big_bottom:

    st.image("https://i.imgur.com/FaKTGkG.png")
    st.markdown("""            
    ### Notes:            
    * A fresh, untrained Agent will Open and Close randomly to any input pattern. \n
    * Agents can be trained by expliciting passing through input and output pairs--- this is the **Labels On** mode \n
    * Agents can be trained more automatically by pairing Food with particular input patters - this is the **Instincts On** mode \n
    """)
#    If the Clam Agent has its mouth Open in the presence of Food, it'll learn, eg. try pairing Food with Chemical-A with Instincts On and the Agent will learn to associate Chemical-A with Food and therefore with Opening, i.e. going forward the Agent will respond to Chemical-A even in the absence of Food while still ignoring Chemical-B. \n


with left_big_bottom:    

    st.write("### First, name your Clam Agent")
#    st.write(" Agents maintain persistant state and are auto-provisioned through our API (or you can also try a version of this demo with the Agent loaded in the browser session.")
    def New_Agent(deployment):
        st.session_state.agent_trials = 0
        st.session_state.agent_id = st.session_state.agent_id_field
        st.session_state.agent_results = np.zeros( (100,  5), dtype='O')
    
        Agent = {
            'deployment': deployment,
            'trials': str(0),
            'last_trial': "",
            'state' : str(0),
            '%_closed' : str(0),
            # 'tested (bulk)': str(st.session_state.tested)+" - "+str(test_size),
            # 'accuracy (bulk)': "",
            # 'no guesses (bulk)': "",
            # 'recs (autocomplete)': str(0),
            # 'mistakes (autocomplete)': str(0),
            }
        st.session_state.Agents[ st.session_state.agent_id ] = Agent       
        if deployment == "Local":
            agent = st.session_state.Local_Core( st.session_state.Local_Arch )
            st.session_state.Local_Agents[st.session_state.agent_id] = agent            
    
    st.session_state.agent_id_field = st.text_input("Name your Agent", value="1st of Clams",  label_visibility="hidden")
    
    st.button("Create Agent Locally", on_click=New_Agent, args=("Local",), type="primary")
    st.button("Or Create Agent via API", on_click=New_Agent, args=("API",))

    if "agent_id" not in st.session_state: pass #st.write("Load up an Agent!")
    else: st.write("Current Agent:  " + st.session_state.agent_id)
    st.write("---")
    st.write("### Step 0) Activate learning:")
    instincts_ONOFF = st.checkbox('Instincts On')
    labels_ONOFF = st.checkbox('Labels On')
    if labels_ONOFF & instincts_ONOFF is True: st.write('Note: the presence of labels overrides any instinctual learning.')
    LABEL = None
    if labels_ONOFF is True:
        labels_CHOICE = st.radio('Pick one', ['OPEN the Clam', 'CLOSE the Clam'])
        if labels_CHOICE == 'OPEN the Clam': LABEL = 1
        if labels_CHOICE == 'CLOSE the Clam': LABEL = 0
    
    st.write("")
    
    st.write("### Step 1) Set an input pattern:")
    placeholder = "Choose any combination of Food, A-Chem, B-Chem, or none of them"
    user_INPUT = st.multiselect(label="Set an input pattern:", options=['FOOD', 'A-CHEMICAL', 'B-CHEMICAL'], label_visibility="hidden", help= placeholder)
    user_STATES = st.slider('To be repeated this many times:', 1, 10)
    st.write("")
    st.write("")


    # Run the Agent Trial
    def run_agent():
        Agent = st.session_state.Agents[ st.session_state.agent_id ]
        
        # INPUTS
        INPUT = [0, 0, 0]
        if 'FOOD'       in user_INPUT: INPUT[0] = 1
        if 'A-CHEMICAL' in user_INPUT: INPUT[1] = 1
        if 'B-CHEMICAL' in user_INPUT: INPUT[2] = 1
        
        responses = []
        for x in np.arange(user_STATES):
            response= agent_api_call(st.session_state.agent_id, INPUT, label=LABEL, deployment=Agent['deployment'])        
            print(response)
            responses += [int(response)]
    
        # save trial results for dispplaying to enduser    
        final_totals = sum(responses) / user_STATES * 100
        if labels_ONOFF == True: Label_Insti = "LABEL"
        elif instincts_ONOFF == True: Label_Insti = "INSTI"
        else: Label_Insti ="NONE"
        
        st.session_state.agent_results[st.session_state.agent_trials, :] = ["Trial #"+str(st.session_state.agent_trials), INPUT, user_STATES, Label_Insti, str(final_totals)+"%"]
        st.session_state.agent_trials += 1
        Agent['trials'] = str(st.session_state.agent_trials)
        Agent['last_trial'] = "Trial #"+str(st.session_state.agent_trials)+"with input"+str(INPUT)+" repeated "+str(user_STATES)+" with learning:"+Label_Insti+" for "+ str(final_totals)+"% opening"

    
    if "agent_id" not in st.session_state: pass
    else: 
        st.write("### Step 2) Run Trial #"+str(st.session_state.agent_trials))
        if user_STATES == 1: button_text= 'Expose Clam ONCE'
        if user_STATES > 1: button_text= 'Expose Clam '+str(user_STATES)+' times'
        st.button(button_text, on_click=run_agent, type="primary")
    
st.write("---")

# Display Trial Log Results

if "agent_id" not in st.session_state: st.write("*You have to create an Agent first*")
else:
    st.write("### Trial #"+str(st.session_state.agent_trials)+" Result:")
    display_trial = st.session_state.agent_trials-1
    if display_trial == -1: pass
    else:
        st.write("**Trial #"+str(display_trial)+" Results Summary**: You exposed the Clam Agent to "+str(st.session_state.agent_results[display_trial, 1])+' as input for '+str(st.session_state.agent_results[display_trial, 2])+'   times with learning mode '+str(st.session_state.agent_results[display_trial, 3])+'.')
        if (st.session_state.agent_results[display_trial, -1]) == "0%":
            if LABEL == 0: st.write("As you commanded, the Clam remained CLOSED, and learned to do so for the input you set.")
            else: st.write("The Clam didn't open at all. :(  Give it some food with this chemical and see how its behavior changes.")
        else:
            if LABEL == 1: st.write("As you ordered, the Clam was OPEN, and learned to do so for the input you set.")
            else: st.write('The Clam OPENED  '+st.session_state.agent_results[display_trial, -1]+' of the time.')
    st.write("")
    st.write("---")
    st.write('### All Trials')
    st.text(str(st.session_state.agent_results[0:st.session_state.agent_trials, :]))  