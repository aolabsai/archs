import requests
import numpy as np
import streamlit as st
import pandas as pd

# API URL and payload
url = "https://7svo9dnzu4.execute-api.us-east-2.amazonaws.com/v0dev/kennel/agent"

payload = {
    "kennel_id": "v0.1.2dev/TEST-Netbox_DeviceDiscovery",
    "agent_id": "72-50-kushagra",
    "request": "story"
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-API-KEY": "weBuildBottomUpAGIsForAll"
}

# Send POST request to the API
response = requests.post(url, json=payload, headers=headers)

# Save response text into a variable
bi_text = response.text

# Print the length of the response text
print(len(bi_text))

# Function to split a string into chunks of specified size
def chunk_string(s, chunk_size):
    return [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]

# Optimized function to convert a binary string into a lookup table
def string2lookup(bi_text):
    # Removing unnecessary initial and final characters from the string
    bi_text = bi_text[25:-2]
    # Split the string into chunks of size 74
    chunks = chunk_string(bi_text, 74)
    # Convert chunks to a NumPy array
    arr = np.array(chunks)
    # Convert the array of strings to a 2D array of integers
    look_up = np.array([[int(char) for char in string] for string in arr])
    return look_up, arr

# Get the lookup table and the array of strings from the binary text
table, array_of_strings = string2lookup(bi_text)
print(table)

# # Create a DataFrame from the lookup table
# df = pd.DataFrame(table)

# # Define the column names according to the specified format
# column_names = []

# # First 10 columns
# column_names.extend([f'I1_{i}' for i in range(1, 11)])

# # Next 10 columns
# column_names.extend([f'I2_{i}' for i in range(1, 11)])

# # Next 10 columns
# column_names.extend([f'I3_{i}' for i in range(1, 11)])

# # Next 30 columns
# column_names.extend([f'Q{i}_{j}' for i in range(1, 4) for j in range(1, 11)])

# # Next 10 columns
# column_names.extend([f'Z{i}' for i in range(1, 11)])

# # Last 4 columns
# column_names.extend([f'C{i}' for i in range(1, 5)])

# # Update the DataFrame with new column names
# df.columns = column_names[:df.shape[1]]


# Streamlit app
st.title("History page for NetBox app")

st.write("Look up table:")
st.write(table)
