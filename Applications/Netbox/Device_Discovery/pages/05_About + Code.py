# -*- coding: utf-8 -*-
"""
Page 4 of App - Netbox Device Discovery

Purpose: Helpful links and about

"""

# 3rd Party Modules
import streamlit as st


# app front end
st.title('More Details -- thanks for taking a look!')
st.write("*We're an AI research venture out of UC Berkeley building a new class of AI; thanks for stopping by and please share your feedback!*.")
if "side_bar_content" in st.session_state: exec(st.session_state.side_bar_content)
else:
    with st.sidebar:
        st.write("*Go to the *Main Page* to start*")
st.write("")
st.write("")

left_big, right_big = st.columns([0.7, 0.3])

with left_big:

    # Streamlit-powered frontend
    st.write("[**Application code (Github)**](https://github.com/aolabsai/archs/tree/application/Netbox_devicediscovery/Applications/Netbox/Device_Discovery) -- what's powering this app, open sourced.")
    st.write("[**Agent Arch code (Github)**](https://github.com/aolabsai/archs/blob/main/Architectures/netbox-device_discovery.py) -- a configuration that defines the 40-neuron Agents behind this app.")
    st.write("[**Arch visual representaton (Miro)**](https://miro.com/app/board/uXjVM_kESvI=/?share_link_id=346355827918) -- a miro board that visualizes the Agent's Arch.")
    st.write("[**Agent-as-a-Service API reference**](https://docs.aolabs.ai/reference/agentinvoke) -- Agents are primarly designed to be run locally; get in touch if you'd like that.")
    st.write("")
    st.write("Visit ([aolabs.ai](https://www.aolabs.ai/)) and ([docs.aolabs.ai](https://docs.aolabs.ai/)) for more and [say hi on discord](https://discord.gg/Zg9bHPYss5).")
    st.write("")
    st.image("https://i.imgur.com/n0KciAE.png")