# -*- coding: utf-8 -*-
"""
Page 4 of App - Netbox Device Discovery

Purpose: Helpful links and about

"""

# 3rd Party Modules
import streamlit as st

# Streamlit-powered frontend
st.title('More Details -- thanks for taking a look!')
st.sidebar.image("https://raw.githubusercontent.com/netbox-community/netbox/develop/docs/netbox_logo.svg", use_column_width=True) 
st.write("*We're an AI research venture out of UC Berkeley, very excited to be building for Netbox*.")
st.write("")
st.write("")
st.write("[**Application Code**](https://github.com/aolabsai/archs/blob/main/Netbox/Device_Discovery/Netbox_App.py) -- what's powering this app, open sourced.")
st.write("[**Agent Arch Code**](https://github.com/aolabsai/archs/blob/main/netbox-device_discovery.py) -- a configuration that defines the 40-neuron Agents behind this app.")
st.write("[**Arch visual representaton**](https://miro.com/app/board/uXjVM_kESvI=/?share_link_id=346355827918) -- a miro board that visualizes the Agent's Arch.")
st.write("[**Agent-as-a-Service API reference**](https://docs.aolabs.ai/reference/agentinvoke) -- Agents are primarly designed to be run locally; get in touch if you'd like that.")
st.write("Visit ([aolabs.ai](https://www.aolabs.ai/)) and ([docs.aolabs.ai](https://docs.aolabs.ai/)) for more and [say hi on discord](https://discord.gg/Zg9bHPYss5).")
