# Risk Assessment Dashboard

## Overview
The Risk Assessment Dashboard is a web application built using Streamlit to provide a comprehensive risk management system. It allows users to upload risk-related data, analyze it using AI/ML models, and visualize risk metrics in an intuitive dashboard. This project is designed to help organizations monitor and mitigate risks effectively.

## Features
- **File Upload**: Upload risk data files in CSV or Excel formats.
- **AI-Powered Analysis**: Use a language model (Claude AI) to analyze risk data and calculate likelihood scores.
- **Risk Visualization**: Generate key risk metrics such as Total Risk Score, High Risks, Critical Risks, Average Risk Score, and Residual Risk.
- **Interactive Tabs**: Navigate between data overview, risk analysis, and raw data views.
- **Custom Styling**: Professional, clean UI with custom CSS for enhanced user experience.

---

## Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python, Claude AI (via Anthropics API)
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy

---

## Installation
1. **Clone the Repository**:
```bash
$ git clone https://github.com/your-repo/risk-assessment-dashboard.git
$ cd risk-assessment-dashboard
```

2. **Install Dependencies**:
```bash
$ pip install -r requirements.txt
```

3. **Set Up Environment Variables**:
Create a `.env` file and add the following:
```env
CLAUDE_API_KEY=<your_api_key>
CLAUDE=<model_name>
```

---

## Running the Application
1. **Start the Application**:
```bash
$ streamlit run app.py
```

2. **Access the Dashboard**:
Open your browser and go to: `http://localhost:8501`

---

## Usage

### 1. Upload File
- Upload a CSV or Excel file containing risk data.
- Required columns: `Risk ID`, `Description`, `Indicator`, `Lower Limit`, `Upper Limit`, `Response Level`.

### 2. View Risk Analysis
- Navigate to the "Overview" tab to see key risk metrics.
- Use interactive charts for better insights.

### 3. Check Raw Data
- Go to the "Data" tab to view processed data, including calculated likelihood scores, calibrated risk scores, and risk categories.

---

## Folder Structure
- **app.py**: Main application script for the Streamlit dashboard.
- **models.py**: Contains the LLMHandler class for AI-based data analysis.
- **helper.py**: Utility functions for risk calibration, visualization, and filtering.
- **config.py**: Configuration settings for the project.
- **static/**: Folder containing any static files, e.g., CSS, images.
- **templates/**: Folder for template HTML files (if any).

---

## Key Components

### 1. **Custom CSS Styling**
The dashboard uses custom CSS to provide a professional look and feel. Styling includes:
- Custom tab design.
- Risk color scales.
- Styled data tables and charts.

### 2. **Risk Metrics**
The dashboard computes the following:
- **Total Risk Score**: Sum of calibrated risk scores.
- **High Risks**: Number of risks categorized as "High".
- **Critical Risks**: Number of risks categorized as "Extreme High".
- **Average Risk Score**: Mean calibrated risk score.
- **Residual Risk**: Difference between current and previous total risks.

### 3. **AI Integration**
The dashboard uses an AI model (Claude) to:
- Analyze risk indicators.
- Generate likelihood scores (1-5 scale).
- Enhance data insights.

---

## Dependencies
- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Plotly
- Anthropics API
- OpenAI (optional for future extensions)

---

## Future Enhancements
- Add support for additional AI models (e.g., OpenAI, Hugging Face).
- Implement user authentication for secure access.
- Integrate a database for storing historical risk data.
- Add more visualization options, such as heatmaps and line charts.
- Enable exporting processed data and charts.

---

## Troubleshooting
- **File Upload Issues**: Ensure the uploaded file has all required columns.
- **AI Processing Errors**: Check if the API key and model configuration in `.env` are correct.
- **CSS Not Loading**: Verify that the custom CSS block is correctly added to `app.py`.

---

