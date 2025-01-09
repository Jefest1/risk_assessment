import streamlit as st
import pandas as pd
from model import llm_handler
from config import settings
import numpy as np
import json

# Custom CSS for Tailwind
tailwind_css = """
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css');

body {
    background-color: #e7f5ff; /* Light blue background */
    font-family: 'Arial', sans-serif; /* Use a clean sans-serif font */
}

h1 {
    @apply text-4xl font-bold text-center text-indigo-600; /* Stylish indigo color */
}


.stDataFrame {
    border: 1px solid #d1d5db; /* Gray border */
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
"""

# Apply the custom CSS
st.markdown(tailwind_css, unsafe_allow_html=True)

# Streamlit App
st.title("Risk Assessment Dashboard")


# File Upload
with st.sidebar:
    uploaded_file = st.file_uploader(
        "Upload your CSV or Excel file", type=["csv", "xlsx"])

# Create tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Analysis", "Data"])

# Tab 3: Data
with tab3:
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
                data['Impact Score'] = np.random.randint(1, 6, size=len(data))

            elif file_type == 'xlsx':
                data = pd.read_excel(uploaded_file)
                required_columns = ['Risk ID', 'Description', 'Indicator',
                                    'Lower Limit', 'Upper Limit', 'Response Level']
                missing_columns = [
                    col for col in required_columns if col not in data.columns]
                data = data[required_columns]
                # Add a new column for impact score with random values between 1 and 5
                data['Impact Score'] = np.random.randint(1, 6, size=len(data))

            # Process data with LLM
            with st.spinner("Processing data with LLM..."):
                updated_data = llm_handler.process_data(data)

            if updated_data is not None:
                st.write("### Updated Data with Likelihood and risk score")
                updated_data = pd.DataFrame(json.loads(
                    updated_data.strip('```json').strip('```')))
                updated_data['Risk Score'] = updated_data['Likelihood Score'] * \
                    data['Impact Score']
                st.dataframe(updated_data.style.applymap(
                    lambda x: 'background-color: #d1fae5' if x <= 5 else 'background-color: #fef3c7' if x <= 10 else 'background-color: #facc15' if x <= 15 else 'background-color: #f87171' if x <= 20 else 'background-color: #991b1b',
                    subset=['Risk Score']))
            else:
                st.error("Failed to process data with LLM.")

        except Exception as e:
            st.error(f"Error processing file: {e}")
# else:
#     st.info("Please upload a CSV or Excel file to begin.")
