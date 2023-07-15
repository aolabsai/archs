# -*- coding: utf-8 -*-
"""
Page 4 of App - Netbox Device Discovery

Purpose: Helpful links and about

"""

# 3rd Party Modules
import streamlit as st



left_big, right_big = st.columns([0.7, 0.3])

with right_big:
    st.image("https://i.imgur.com/n0KciAE.png")
    # with st.expander("See Agent's Arch (Configuration)"):
    #     arch_visual_miro_html= """<iframe width="768" height="432" src="https://miro.com/app/live-embed/uXjVM_kESvI=/?moveToViewport=121907,-48157,16256,9923&embedId=323274877415" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>"""
    #     st.write(arch_visual_miro_html, unsafe_allow_html=True)

with left_big:

    # Streamlit-powered frontend
    st.title('More Details -- thanks for taking a look!')
    st.sidebar.image("https://raw.githubusercontent.com/netbox-community/netbox/develop/docs/netbox_logo.svg", use_column_width=True) 
    st.write("*We're an AI research venture out of UC Berkeley, very excited to be building for Netbox*.")
    st.write("")
    st.write("")
    st.write("[**Application code (Github)**](https://github.com/aolabsai/archs/blob/main/Netbox/Device_Discovery/Netbox_App.py) -- what's powering this app, open sourced.")
    st.write("[**Agent Arch code (Github)**](https://github.com/aolabsai/archs/blob/main/netbox-device_discovery.py) -- a configuration that defines the 40-neuron Agents behind this app.")
    st.write("[**Arch visual representaton (Miro)**](https://miro.com/app/board/uXjVM_kESvI=/?share_link_id=346355827918) -- a miro board that visualizes the Agent's Arch.")
    st.write("[**Agent-as-a-Service API reference**](https://docs.aolabs.ai/reference/agentinvoke) -- Agents are primarly designed to be run locally; get in touch if you'd like that.")
    st.write("")
    st.write("*Running Agents Locally vs via the API:* Agents are designed to be deployed locally; they're super lightweight (the Agents in this app are only 40 neurons/parameters).The API is provided as a quick test bed and we are happy to accomdate local / on-prem needs; please reach out..")
    st.write("Visit ([aolabs.ai](https://www.aolabs.ai/)) and ([docs.aolabs.ai](https://docs.aolabs.ai/)) for more and [say hi on discord](https://discord.gg/Zg9bHPYss5).")
 