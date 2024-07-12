import requests
import numpy as np
import streamlit as st
import pandas as pd



# API URL and payload

def API_response(agent_id):
    url = "https://7svo9dnzu4.execute-api.us-east-2.amazonaws.com/v0dev/kennel/agent"

    payload = {
    "kennel_id": "v0.1.2dev/TEST-Netbox_DeviceDiscovery",
    "agent_id": agent_id, 
    "request": "story"
    }

    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-API-KEY": "weBuildBottomUpAGIsForAll"
    }   

    # Send POST request to the API
    response = requests.post(url, json=payload, headers=headers)
    
    return response.text




# Optimized function to convert a binary string into a lookup table
def string2lookup(bi_text):
    # Remove the first 25 characters and the last 2 characters from the binary string
    bi_text = bi_text[25:-2]
    
    # Convert the string into a list of characters
    lis = list(bi_text)
    
    # Convert the list of characters to a NumPy array of integers
    lis = np.asarray(lis, dtype=int)
    
    # Calculate the number of rows in the lookup table
    rows = int(len(lis) / 73)
    
    # Reshape the array into a 2D array with 73 columns
    look_up = np.reshape(lis, [rows, 73])
    
    return look_up





# Streamlit-powered frontend
st.title('Agent history page')
if "side_bar_content" in st.session_state: exec(st.session_state.side_bar_content)
else:
    with st.sidebar:
        st.write("*Go to the Main Page to start*")

left_big, right_big = st.columns([0.7, 0.3])


if 'trained' not in st.session_state:
    st.text("You have to connect your Netbox account and an Agent first.")

else:

    with left_big:
        
        st.write("")
        st.write("")
        
        deployment = st.session_state.Agents[st.session_state.agent_id]['deployment']
        
        # Generate table of devices to be added/recommended    
        if st.session_state.account_added:
            train_devices = st.session_state.train_devices_in
            train_devices_table = np.zeros([len(train_devices), 4], dtype='O')
            for i in range(len(train_devices)):
                d = train_devices[i]
                train_devices_table[i, 0] = d.__str__()
                train_devices_table[i, 1] = d.device_type.manufacturer.__str__()
                train_devices_table[i, 2] = d.site.__str__()
                train_devices_table[i, 3] = d.device_type.__str__()
            st.session_state.train_devices_table = pd.DataFrame(train_devices_table, columns=['Name', 'Manufacturer', 'Site', 'Type'])
            
            st.markdown("Given below is the label history table.")
            
            st.write(st.session_state.train_devices_table)
            st.write("")
        
        # Load session data
        manufacturers = st.session_state.manufacturers
        roles = st.session_state.roles
        sites = st.session_state.sites
        types = st.session_state.device_types

    with right_big:
        agent_id = st.session_state.agent_id
        
        # Get the lookup table and the array of strings from the binary text
        bi_text = API_response(agent_id=agent_id)  # Assuming you have a function to get the binary text response
        table = string2lookup(bi_text)

        # Create a DataFrame from the lookup table
        df = pd.DataFrame(table)

        # Define the column names according to the specified format
        column_names = []

        # First 10 columns
        column_names.extend([f'I1_{i}' for i in range(1, 11)])

        # Next 10 columns
        column_names.extend([f'I2_{i}' for i in range(1, 11)])

        # Next 10 columns
        column_names.extend([f'I3_{i}' for i in range(1, 11)])

        # Next 30 columns
        column_names.extend([f'Q{i}_{j}' for i in range(1, 4) for j in range(1, 11)])

        # Next 10 columns
        column_names.extend([f'Z{i}' for i in range(1, 11)])

        # Last 4 columns
        column_names.extend([f'C{i}' for i in range(1, 5)])

        # Update the DataFrame with new column names
        df.columns = column_names[:df.shape[1]]

        # Add sliders to control the number of rows and columns displayed
        num_rows = st.slider("Number of rows to display", min_value=1, max_value=df.shape[0], value=7)
        num_cols = st.slider("Number of columns to display", min_value=1, max_value=df.shape[1], value=5)

        st.write(f"Displaying first {num_rows} rows and first {num_cols} columns of the lookup table:")
        st.table(df.iloc[:num_rows, :num_cols])
