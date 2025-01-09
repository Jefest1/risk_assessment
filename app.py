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
    background-color: #f9fafb;
}

h1 {
    @apply text-4xl font-bold text-center text-blue-600;
}

.stButton>button {
    @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
}

.stDataFrame {
    @apply shadow-lg rounded-lg;
}
</style>
"""

# Apply the custom CSS
st.markdown(tailwind_css, unsafe_allow_html=True)

# Streamlit App
st.title("Risk Assessment Dashboard")

# Clear cache button
if st.button("Clear Cache"):
    st.cache_data.clear()

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
            # Add a new column for impact score with random values between 1 and 5
            data['Impact Score'] = np.random.randint(1, 6, size=len(data))
        # Display uploaded data
        st.write("### Uploaded Data")
        st.dataframe(data.head())

        # Process data with LLM
        with st.spinner("Processing data with LLM..."):
            updated_data = llm_handler.process_data(data)

        if updated_data is not None:
            st.success("Data processed successfully!")
            st.write("### Updated Data with Likelihood and risk score")
            updated_data = pd.DataFrame(json.loads(
                updated_data.strip('```json').strip('```')))
            updated_data['Risk Score'] = updated_data['Likelihood Score'] * \
                data['Impact Score']
            st.dataframe(updated_data)
        else:
            st.error("Failed to process data with LLM.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
# else:
#     st.info("Please upload a CSV or Excel file to begin.")
