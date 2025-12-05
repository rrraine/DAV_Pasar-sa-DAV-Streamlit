# streamlit run apps/main.py

import streamlit as st
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt 
# import plotly.express as px #pip install plotly if needed

import tab_overview
import tab_dataexploration
import tab_analysis
import tab_insights


# Page configuration
st.set_page_config(
    page_title="DPWH Flood Control Streamlit App",
    layout="wide",
)


st.title("DPWH Flood Control Projects - Data Analysis Dashboard")

def load_dataset():
    df = pd.read_csv("data/dpwhfloodcontrol.csv")
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    df = df.rename(columns={
        "FundingYear": "Year",
        "ApprovedBudgetForContract": "Budget"
    })
    # Ensure correct types
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    if "Budget" in df.columns:
        df["Budget"] = pd.to_numeric(df["Budget"], errors="coerce")
    return df



# Dataset | to reuse in all tabs

#st.sidebar.header("Upload Your Dataset")
#uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

#if uploaded_file:
#    df = pd.read_csv(uploaded_file)
# else:
#    df = None
#    st.sidebar.warning("Please upload a CSV file to continue.")

st.markdown("""
    <style>

    /* --------------------------------------------------
                    TAB NAVIGATION (CENTERING FIX)
    -------------------------------------------------- */
    
    /* FIX: Target the internal tab button list and center its contents */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center !important;
        gap: 5px; 
    }
    
    /* Ensure the main tabs container is a block element and doesn't interfere with the width of content below it */
    [data-testid="stTabs"] {
        display: block !important; 
        margin-bottom: 20px;
        width: 100%; /* Ensure it spans the full width of the main page */
    }


    /* Default tab style */
    .stTabs [data-baseweb="tab"] {
        font-size: 17px;
        color: #003366;                     /* Inactive tab text color (Blue) */
        background-color: #f0f0f0;          /* Inactive tab background */
        border-radius: 8px 8px 0 0;
        padding: 12px 20px;
        margin-right: 5px;
        transition: all 0.25s ease;
    }

    /* Active tab style */
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important;  /* Active background (Blue) */
        color: white !important;               /* Active text (White) */
        font-weight: bold;
        border-bottom: 2px solid #0A6E44; /* Green underline */
    }
    </style>
""", unsafe_allow_html=True)


tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Data Exploration", "Analysis", "Insights"])
with st.container(horizontal_alignment="center"):
    with st.container():
        with tab1:
            tab_overview.render()
        with tab2:
            tab_dataexploration.render()

        with tab3:
            tab_analysis.render()

        with tab4:
            tab_insights.render()
