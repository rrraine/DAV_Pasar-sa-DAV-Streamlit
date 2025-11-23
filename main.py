# streamlit run main.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px #pip install plotly if needed

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


tab1, tab2, tab3, tab4 = st.tabs(["Overview and Dataset", "Data Exploration", "Analysis", "Insights"])

# --- Tab 1: Overview and Dataset ---
with tab1:
  st.header("📄 Overview")





# --- Tab 2: Data Exploration ---
with tab2:
  st.header("🔍 Data Exploration")





# --- Tab 3: Analysis ---
with tab3:
    st.header("📊 Analysis")





# --- Tab 4: Insights ---
with tab4:
    st.header("💡 Insights")


