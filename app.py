import streamlit as st
import pandas as pd
from model import llm_handler
import numpy as np
import json
from helper import (calibrate_risk_score,
                    show_risk_scale,
                    get_risk_cat, get_barchart,
                    get_barcharts, filter_high_extreme_risk,
                    create_matrix_from_csv)

# Page configuration
st.set_page_config(
    page_title="Risk Assessment Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
custom_css = """
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
        background-color: #f8fafc;
    }
    
    /* Header styling */
    .main-header {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        padding: 0px 24px;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        font-size: 16px;
        font-weight: 500;
        color: #4b5563;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1e40af;
        border-bottom: 2px solid #1e40af;
    }
    
    /* Risk color classes for future use */
    .risk-deep-green { background-color: #047857; }
    .risk-light-green { background-color: #10B981; }
    .risk-yellow { background-color: #F59E0B; }
    .risk-red { background-color: #EF4444; }
    .risk-wine { background-color: #991B1B; }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff;
    }
    
    /* File uploader styling */
    .stFileUploader {
        padding: 1rem;
        border-radius: 8px;
        border: 2px dashed #e2e8f0;
        background-color: #f8fafc;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        padding: 1rem;
        border-radius: 8px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Custom card styling */
    .custom-card {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Risk Score Color Scale */
    .risk-scale-container {
        padding: 1.5rem;
        background-color: white;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .risk-scale {
        width: 100%;
        height: 8px;
        background: linear-gradient(
            to right,
            #006400 0%,      /* Deep green - Lower Risk (1-5) */
            #90EE90 20%,     /* Light green - Low Risk (6-10) */
            #FFD700 40%,     /* Yellow - Medium Risk (11-15) */
            #FF0000 60%,     /* Red - High Risk (16-20) */
            #8B0000 80%      /* Wine - Extreme Risk (21-25) */
        );
        border-radius: 4px;
        margin: 1rem 0;
    }

    .risk-labels {
        display: flex;
        justify-content: space-between;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }

    .risk-label {
        font-weight: 500;
        text-align: center;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Application Header
st.markdown("""
    <div class="main-header">
        <h1 style='text-align: center; color: #1e40af; font-size: 2.5rem; font-weight: 600;'>
            Risk Assessment Dashboard
        </h1>
        <p style='text-align: center; color: #6b7280; margin-top: 0.5rem;'>
            Enterprise Risk Management System
        </p>
    </div>
""", unsafe_allow_html=True)

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
                required_columns = ['Risk ID', 'Type of Risk', 'Description', 'Indicator',
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
                updated_data['Likelihood Category'] = updated_data['Likelihood Score'].apply(
                    get_risk_cat)
                updated_data['Risk Score'] = updated_data['Likelihood Score'] * \
                    data['Impact Score']
                # Calculate Calibrated Risk Score (1-5 scale)

                updated_data['Calibrated Risk Score'] = updated_data['Risk Score'].apply(
                    calibrate_risk_score)
                updated_data['Risk Category'] = updated_data['Calibrated Risk Score'].apply(
                    get_risk_cat)
                st.dataframe(updated_data)
            else:
                st.error("Failed to process data with LLM.")

        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.info("Please upload a CSV or Excel file to begin.")


# In the Overview tab section
try:
    with tab1:
        # Create metrics row
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            # Total Risk Dashboard
            with st.container():
                st.markdown("""
                    <div class="custom-card">
                        <div class="metric-value">
                """, unsafe_allow_html=True)
                if 'Calibrated Risk Score' in updated_data.columns:
                    current_total_risk = updated_data['Calibrated Risk Score'].sum(
                    )
                    # In practice, you would fetch this from a database
                    previous_total_risk = 0  # Placeholder for previous risk

                    risk_change = ((current_total_risk - previous_total_risk) / previous_total_risk * 100
                                   if previous_total_risk != 0 else 0)
                    st.metric(
                        "Total Risk Score",
                        f"{current_total_risk}",
                        f"{risk_change:+.1f}%" if previous_total_risk != 0 else "First Assessment"
                    )

        with col2:
            # High Risks Dashboard
            with st.container():
                st.markdown("""
                    <div class="custom-card">
                        <div class="metric-value">
                """, unsafe_allow_html=True)

                if 'Calibrated Risk Score' in updated_data.columns:
                    current_high_risks = len(
                        updated_data[updated_data['Calibrated Risk Score'] == 4])
                    previous_high_risks = 0  # Placeholder for previous count
                    high_risk_change = ((current_high_risks - previous_high_risks)
                                        if previous_high_risks != 0 else current_high_risks)

                    st.metric(
                        "High Risks",
                        current_high_risks,
                        f"{high_risk_change:+d}" if previous_high_risks != 0 else "New"
                    )

        with col3:
            # Critical Risks Dashboard
            with st.container():
                st.markdown("""
                    <div class="custom-card">
                        <div class="metric-value">
                """, unsafe_allow_html=True)

                if 'Calibrated Risk Score' in updated_data.columns:
                    current_high_risks = len(
                        updated_data[updated_data['Calibrated Risk Score'] == 5])
                    previous_high_risks = 0  # Placeholder for previous count
                    high_risk_change = ((current_high_risks - previous_high_risks)
                                        if previous_high_risks != 0 else current_high_risks)

                    st.metric(
                        "Extreme High Risks",
                        current_high_risks,
                        f"{high_risk_change:+d}" if previous_high_risks != 0 else "New"
                    )

        with col4:
            # average Risk Dashboard
            with st.container():
                st.markdown("""
                    <div class="custom-card">
                        <div class="metric-value">
                """, unsafe_allow_html=True)

                if 'Calibrated Risk Score' in updated_data.columns:
                    current_total_risk = updated_data['Calibrated Risk Score'].mean(
                    )
                    # In practice, you would fetch this from a database
                    previous_total_risk = 0  # Placeholder for previous risk

                    risk_change = ((current_total_risk - previous_total_risk) / previous_total_risk * 100
                                   if previous_total_risk != 0 else 0)

                    st.metric(
                        "Average Risk Score",
                        f"{current_total_risk:.2f}",
                        f"{risk_change:+.1f}%" if previous_total_risk != 0 else "New"
                    )
        with col5:
            # Residual Risk Dashboard
            with st.container():
                st.markdown("""
                    <div class="metric-card">
                        <div class="metric-value">
                """, unsafe_allow_html=True)

                if 'Calibrated Risk Score' in updated_data.columns:
                    # Calculate residual risk (current - previous)
                    current_risk = updated_data['Calibrated Risk Score'].sum()
                    previous_risk = 0  # Placeholder for previous risk
                    residual_risk = current_risk - previous_risk if previous_risk != 0 else 0

                    st.metric(
                        "Residual Risk",
                        f"{residual_risk:.2f}",
                        "First Assessment" if previous_risk == 0 else None
                    )

        # Show the risk scale
        show_risk_scale()
        st.plotly_chart(create_matrix_from_csv(updated_data))
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(get_barchart(updated_data),
                            use_container_width=True)
        with col2:
            st.plotly_chart(get_barcharts(updated_data),
                            use_container_width=True)

        # show high risk table
        st.write("High and Extreme Risks")
        st.dataframe(filter_high_extreme_risk(updated_data))
except:
    st.info("Please upload a CSV or Excel file to begin.")
# Add a footer
st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 2rem; margin-top: 2rem; border-top: 1px solid #e5e7eb;'>
        Risk Assessment Dashboard © 2025
    </div>
""", unsafe_allow_html=True)
