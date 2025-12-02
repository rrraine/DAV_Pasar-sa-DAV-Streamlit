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


tab1, tab2, tab3, tab4 = st.tabs(["   Overview   ", "   Data Exploration   ", "   Analysis   ", "   Insights   "])

with tab1:
    tab_overview.render()

with tab2:
    tab_dataexploration.render()

with tab3:
    tab_analysis.render()

with tab4:
    tab_insights.render()


# Option 2: Using a selectbox in the sidebar

# Page config
# st.set_page_config(
#     page_title="DPWH Flood Control Streamlit App",
#     layout="wide"
# )

# st.title("DPWH Flood Control Projects - Data Analysis Dashboard")

# st.markdown("""
# <style>
# /* Make radio look like vertical buttons */
# div[role="radiogroup"] > label {
#     background: #f0f0f0;
#     padding: 12px 16px;
#     border-radius: 8px;
#     margin-bottom: 6px;
#     width: 100%;
#     display: block;
#     border: 1px solid #d0d0d0;
#     cursor: pointer;
#     color: #003366;
#     font-size: 16px;
# }

# /* Selected state */
# div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
#     background: #003366 !important;
#     color: white !important;
#     font-weight: bold;
# }
# </style>
# """, unsafe_allow_html=True)


# # ---------------------------------------
# # Sidebar-like vertical tabs using radio
# # ---------------------------------------

# # Define available views
# pages = {
#     "Overview and Dataset": "overview",
#     "Data Exploration": "exploration",
#     "Analysis": "analysis",
#     "Insights": "insights"
# }

# # ---- Layout: 2 columns (sidebar + content)
# col_sidebar, col_content = st.columns([1, 4])

# with col_sidebar:
#     st.markdown("### 📁 Sections")

#     # Radio button selection (vertical tabs)
#     selected_page = st.radio(
#         "",
#         list(pages.keys()),
#         label_visibility="collapsed",
#     )

# # ---------------------------------------
# # CONTENT AREA (right column)
# # ---------------------------------------
# with col_content:
#     if selected_page == "Overview and Dataset":
#         tab_overview.render()

#     elif selected_page == "Data Exploration":
#         tab_dataexploration.render()

#     elif selected_page == "Analysis":
#         tab_analysis.render()

#     elif selected_page == "Insights":
#         tab_insights.render()


