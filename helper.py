import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def calibrate_risk_score(score):
    if 1 <= score <= 5:
        return 1  # lower risk
    elif 6 <= score <= 10:
        return 2  # low risk
    elif 11 <= score <= 15:
        return 3  # medium risk
    elif 16 <= score <= 20:
        return 4  # high risk
    else:  # 21-25
        return 5  # extreme risk


def get_risk_cat(risk):
    if risk <= 1:
        return 'lower'
    elif risk == 2:
        return 'low'
    elif risk == 3:
        return 'medium'
    elif risk == 4:
        return 'high'
    elif risk == 5:
        return 'extreme'
    else:
        return 'risk levels cannot be greater than 5'


# Add a color scale visualization
def show_risk_scale():
    st.markdown("""
        <div class='risk-scale-container'>
            <h4>Risk Score Scale</h4>
            <div class='risk-scale'></div>
            <div class='risk-labels'>
                <span class='risk-label' style='color: #006400;'>Lower<br/>(1-5)</span>
                <span class='risk-label' style='color: #90EE90;'>Low<br/>(6-10)</span>
                <span class='risk-label' style='color: #FFD700;'>Medium<br/>(11-15)</span>
                <span class='risk-label' style='color: #FF0000;'>High<br/>(16-20)</span>
                <span class='risk-label' style='color: #8B0000;'>Extreme<br/>(21-25)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


def get_barchart(data):
    # Filter for high and extreme likelihood levels
    high_extreme_likelihood = data[data['Likelihood Category'].isin(
        ['high', 'extreme'])]
    likelihood_counts = high_extreme_likelihood.groupby(
        'Likelihood Category')['Risk ID'].count().reset_index()
    likelihood_counts.rename(columns={'Risk ID': 'Count'}, inplace=True)

    # Create High and Extreme Likelihood Levels bar chart
    fig_likelihood = px.bar(
        likelihood_counts,
        x='Likelihood Category',
        y='Count',
        title='High and Extreme Likelihood Levels',
        labels={'Count': 'Count', 'Likelihood Category': 'Likelihood Level'},
        barmode='group',
        color='Likelihood Category',
        color_discrete_sequence=['#722F37', 'red']
    )
    # Hide the legend
    fig_likelihood.update_layout(showlegend=False)

    return fig_likelihood


def get_barcharts(data):
    # Filter for high and extreme likelihood levels
    high_extreme_risk = data[data['Risk Category'].isin(['high', 'extreme'])]
    risk_counts = high_extreme_risk.groupby(
        'Risk Category')['Risk ID'].count().reset_index()
    risk_counts.rename(columns={'Risk ID': 'Count'}, inplace=True)

    # Create High and Extreme Likelihood Levels bar chart
    fig_likelihood = px.bar(
        risk_counts,
        x='Risk Category',
        y='Count',
        title='High and Extreme Risk Levels',
        labels={'Count': 'Count', 'Risk Category': 'Risk Level'},
        barmode='group',
        color='Risk Category',
        color_discrete_sequence=['#722F37', 'red']
    )
    # Hide the legend
    fig_likelihood.update_layout(showlegend=False)

    return fig_likelihood


def filter_high_extreme_risk(data):
    # Filter the rows with high and extreme likelihood categories
    filtered_data = data[data['Likelihood Category'].isin(['high', 'extreme'])]

    # Select only the relevant columns
    selected_columns = filtered_data[[
        'Risk ID', 'Type of Risk', 'Indicator', 'Likelihood Score', 'Calibrated Risk Score']]

    return selected_columns


def create_matrix_from_csv(data):
    """
    Create a risk matrix visualization from the dataset using Likelihood Score and Impact Score.

    Parameters:
        data (pd.DataFrame): Preprocessed risk dataset.

    Returns:
        fig (plotly.graph_objects.Figure): Risk matrix heatmap.
    """
    # Extract unique Impact and Likelihood Scores
    impact_scores = sorted(data['Impact Score'].unique())
    likelihood_scores = sorted(data['Likelihood Score'].unique(), reverse=True)

    # Create a pivot table for the heatmap
    risk_matrix = data.pivot_table(
        values="Calibrated Risk Score",
        index="Likelihood Score",
        columns="Impact Score",
        aggfunc="mean",
        fill_value=0
    )

    # Define the color scale
    colorscale = [
        [0.0, "#006400"],   # Deep green - Lower Risk
        [0.2, "#90EE90"],   # Light green - Low Risk
        [0.4, "#FFD700"],   # Yellow - Medium Risk
        [0.6, "#FF0000"],   # Red - High Risk
        [1.0, "#8B0000"]    # Wine - Extreme Risk
    ]

    # Add white spaces between colors for differentiation
    colorscale_with_spaces = []
    for i in range(len(colorscale) - 1):
        colorscale_with_spaces.append(colorscale[i])
        mid_point = (colorscale[i][0] + colorscale[i + 1][0]) / 2
        colorscale_with_spaces.append([mid_point, "#FFFFFF"])  # White space
    colorscale_with_spaces.append(colorscale[-1])

    # Create the heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=risk_matrix.values,
            x=[f"{i}" for i in impact_scores],
            y=[f"{i}" for i in likelihood_scores],
            colorscale=colorscale_with_spaces,
            colorbar=dict(title="Calibrated Risk Score"),
            hovertemplate="Impact: %{x}<br>Likelihood: %{y}<br>Score: %{z}<extra></extra>"
        )
    )

    # Set axis titles and layout
    fig.update_layout(
        title="Risk Matrix",
        xaxis=dict(title="Impact Scores"),
        yaxis=dict(title="Likelihood Scores"),
        template="plotly_white"
    )

    return fig
