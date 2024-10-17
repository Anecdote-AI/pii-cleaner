import streamlit as st
import pandas as pd
from io import BytesIO
import base64
import os
from pii_removal import MaskPII

pii_mask = MaskPII()

def remove_pii(data, columns, deep_removal):
    # Ensure all selected columns are strings
    data[columns] = data[columns].astype(str)
    # Apply PII masking to each column
    for column in columns:
        data[column] = pii_mask.transform(data[column], deep=deep_removal)
    return data

# Set page configuration
st.set_page_config(page_title="PII Removal Tool", page_icon=":shield:")

# Add a logo (Replace 'logo.png' with your logo file path)
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=100)
else:
    st.warning("Logo file not found. Please make sure 'logo.png' is in the same directory.")

st.title("PII Removal Tool")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Read CSV
    data = pd.read_csv(uploaded_file)
    
    # Display CSV preview
    st.write("CSV Preview:")
    st.write(data.head())
    
    # Convert columns to list
    columns_list = data.columns.tolist()
    
    # Select columns for PII removal
    columns = st.multiselect("Select columns to remove PII", columns_list, default=columns_list)
    
    # Add the checkbox for deep removal
    deep_removal = st.checkbox("SLOW deep removal: includes names")
    
    if st.button("Apply PII Removal"):
        with st.spinner("Removing PII..."):
            # Apply PII removal with deep_removal parameter
            result_data = remove_pii(data, columns, deep_removal)
        
        # Convert result to CSV
        csv = result_data.to_csv(index=False).encode('utf-8')
        
        # Provide download button
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="pii_removed.csv",
            mime="text/csv",
        )
