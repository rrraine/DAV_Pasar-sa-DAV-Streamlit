import streamlit as st
from pathlib import Path

def load_dataset():
    BASE_DIR = Path(__file__).resolve().parent
    FILE_PATH = BASE_DIR.parent / 'data' / 'dpwhfloodcontrol.csv'

    df = pd.read_csv(FILE_PATH)
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

def key_insights(df):
    st.title("Key Findings and Summary")

    # Data Preparion and Metrics
    total_cost = df['ContractCost'].sum()
    total_project = len(df)

    col_total_cost, col_peak_budget, col_total_projects = st.columns(3)
    
    with col_total_cost:
        with st.container(border=True, horizontal_alignment="center"):
            st.header("Total Cost of Flood Control Projects:")
    with col_peak_budget:
        with st.container(border=True, horizontal_alignment="center"):
            st.header("Peak Budget for a Flood Control Project")
    with col_total_projects:
        with st.container(border=True, horizontal_alignment="center"):
            st.header("Total Flood Control Projects")



def render():
    df = load_dataset()
    key_insights(df)
    st.title("Insights")
