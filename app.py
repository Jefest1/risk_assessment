import streamlit as st
import pandas as pd
from model import llm_handler
from config import settings

# Streamlit App
st.title("Risk Assessment Dashboard")


# File Upload
uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]

    try:
        if file_type == 'csv':
            data = pd.read_csv(uploaded_file)
            required_columns = ['Risk ID', 'Description', 'Indicator',
                                'Lower Limit', 'Upper Limit', 'Response Level']
            missing_columns = [
                col for col in required_columns if col not in data.columns]
            data = data[required_columns]
        elif file_type == 'xlsx':
            data = pd.read_excel(uploaded_file)
            required_columns = ['Risk ID', 'Description', 'Indicator',
                                'Lower Limit', 'Upper Limit', 'Response Level']
            missing_columns = [
                col for col in required_columns if col not in data.columns]
            data = data[required_columns]
        # Display uploaded data
        st.write("### Uploaded Data")
        st.dataframe(data.head())

        # Process data with LLM
        with st.spinner("Processing data with LLM..."):
            updated_data = llm_handler.process_data(data)

        if updated_data is not None:
            st.success("Data processed successfully!")
            st.write("### Updated Data with Likelihood and Reasons")
            st.write(updated_data)
        else:
            st.error("Failed to process data with LLM.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
# else:
#     st.info("Please upload a CSV or Excel file to begin.")
