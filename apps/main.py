# streamlit run apps/main.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px #pip install plotly if needed


import tab_overview
import tab_dataexploration
import tab_analysis
import tab_insights


# Page configuration
st.set_page_config(
    page_title="DPWH Flood Control Streamlit App",
    layout="wide",
)

st.title("DPWH Flood Control Projects - Data Analysis Dashbaord")


# Dataset | to reuse in all tabs

# st.sidebar.header("Upload Your Dataset")
# uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
# else:
#     df = None
#   st.sidebar.warning("Please upload a CSV file to continue.")

st.markdown("""
    <style>
    /* Default tab style */
    .stTabs [data-baseweb="tab"] {
        font-size: 17px;
        color: #003366;                     /* Inactive tab text color */
        background-color: #f0f0f0;          /* Inactive tab background */
        border-radius: 8px 8px 0 0;
        padding: 12px 20px;
        margin-right: 5px;
    }

    /* Active tab style */
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important;  /* Active background */
        color: white !important;               /* Active text */
        font-weight: bold;
        border-bottom: 2px solid #001f4d;
    }
    </style>
""", unsafe_allow_html=True)


tab1, tab2, tab3, tab4 = st.tabs(["Overview and Dataset", "Data Exploration", "Analysis", "Insights"])

with tab1:
    tab_overview.render()

with tab2:
    tab_dataexploration.render()

with tab3:
    tab_analysis.render()

with tab4:
    tab_insights.render()


