# -*- coding: utf-8 -*-
"""
Page 5 of App - Netbox Device Discovery

Purpose: Display Agents connected to Session

"""

# 3rd Party Modules
import streamlit as st
import pandas as pd

# side bar content
if "Agents" not in st.session_state:
    st.session_state["Agents"] = {}
if st.session_state.account_added is False:
    data_source = "**Data Source:** :red[*Connect a Netbox Account*]" 
elif st.session_state.account_added:
    data_source = "**Data Source:** :green["+st.session_state.nb_USER_url+"]"    
if 'agent_id' not in st.session_state:
    active_agent = "**Active Agent:** :red[*No Agent Yet*]"
else:
    active_agent = "**Active Agent:** :violet["+st.session_state.agent_id+"]"
with st.sidebar:    
    st.write(data_source)
    st.write(active_agent)
st.sidebar.image("https://raw.githubusercontent.com/netbox-community/netbox/develop/docs/netbox_logo.svg", use_column_width=True)


if "Agents" in st.session_state:
    st.dataframe( pd.DataFrame.from_dict( st.session_state.Agents ) )
else:
    st.text("You have not created any Agents yet.")

st.write("")
st.image("https://i.imgur.com/n0KciAE.png")