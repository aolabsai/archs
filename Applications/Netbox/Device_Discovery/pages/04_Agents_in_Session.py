# -*- coding: utf-8 -*-
"""
Page 5 of App - Netbox Device Discovery

Purpose: Display Agents connected to Session

"""

# 3rd Party Modules
import streamlit as st
import pandas as pd

# streamlit frontend
st.title('View All Your Agents')
if "side_bar_content" in st.session_state: exec(st.session_state.side_bar_content)
else:
    with st.sidebar:
        st.write("*Go to the Main Page to start*")
st.write("*View all of the Agents you've called during this browser session.*")

if "Agents" in st.session_state:
    if st.session_state.Agents == {}: st.text("You have not created any Agents yet.")
    st.dataframe( pd.DataFrame.from_dict( st.session_state.Agents ) )
else:
    st.text("You have not created any Agents yet.")


left_big, right_big = st.columns([0.5, 0.5])
with left_big:
    st.write("")
    st.image("https://i.imgur.com/n0KciAE.png")