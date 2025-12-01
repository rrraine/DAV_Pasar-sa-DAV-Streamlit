import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
from utils import load_dataset


# @st.cache_data
# def load_dataset():
#     BASE_DIR = Path(__file__).resolve().parent
#     FILE_PATH = BASE_DIR.parent / 'data' / 'dpwhfloodcontrol.csv'

#     df = pd.read_csv(FILE_PATH)
#     df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
#     df = df.rename(columns={
#         "FundingYear": "Year",
#         "ApprovedBudgetForContract": "Budget"
#     })
#     # Ensure correct types
#     if "Year" in df.columns:
#         df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
#     if "Budget" in df.columns:
#         df["Budget"] = pd.to_numeric(df["Budget"], errors="coerce")

#     #Data Cleaning
#     #Converting 'ContractCost' to numeric
#     cost_col = 'ContractCost'
#     df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

#     return df

# Helper Functions
#region
def format_peso_billions(value):
    try:
       return f"₱{value / 1_000_000_000:,.2f} B"
    except:
        return "N/A"
#endregion


def key_insights(df):
    st.header("Key Findings and Summary")

    # Data Preparation and Metrics
    total_cost = df['ContractCost'].sum()
    total_project = len(df)

    if "Year" in df.columns and "Budget" in df.columns:
        budget_year = df.groupby("Year")["Budget"].sum().reset_index()
        peak_budget = budget_year["Budget"].max()
        peak_year = budget_year.loc[budget_year["Budget"].idxmax(), "Year"]
    else:
        peak_budget = 0
        peak_year = "N/A"
    col_total_cost, col_peak_budget, col_total_projects = st.columns(3)
    
    with col_total_cost:
        with st.container(border=True, horizontal_alignment="center"):
            st.subheader("Total Cost")
            st.metric(
                label = "Total Budget For Flood Control Projects",
                value = format_peso_billions(total_cost)
            )
            st.caption("Sum of all Contract Cost in the dataset.")
    with (col_peak_budget):
        with st.container(border=True, horizontal_alignment="center"):
            st.subheader("Peak Budget")
            st.metric(
                label = f"Budget in {peak_year}",
                value = format_peso_billions(peak_budget)
            )
            st.caption("Highest financial budget in the dataset")
    with col_total_projects:
        with st.container(border=True, horizontal_alignment="center"):
            st.subheader("Total Projects")
            st.metric(
                label="Total Project Awarded",
                value = f"{total_project:,}"
            )
            st.caption("Volume demonstates overall project scale")
    st.divider()
    st.subheader("Cost Distribution: Mega-Project Domination")

    col_hist, col_text = st.columns([2,1])
    with col_hist:
        with st.container(border=True, horizontal_alignment="center"):
            fig_hist = px.histogram(
                df[df['ContractCost'].notna()],
                x="ContractCost",
                nbins=50,
                title="Project Contract Cost Distribution",
                log_y=True,
                labels={'ContractCost': 'Contract Cost (Log Scale)'}
            )
            st.plotly_chart(fig_hist)
    with col_text:
        with st.container(border=True, horizontal_alignment="center"):
            st.markdown("""
                The distribution of project costs is **heavily right-skewed**, visually confirming a critical imbalance:
                
                - The **vast majority** of projects are small to mid-sized.
                - The **total budget** is disproportionately consumed by a **small number of extremely expensive mega-projects** (the long tail).
                - This pattern raises questions about cost standardization.
                """
            )
    st.divider()
    # Should I Add A Concentration of Contracts???
    st.subheader("Concentration of Contracts // Should I add this?")

def pattern_trends(df):
    if df.empty:
        st.warning("No data found")
        return
    st.subheader("Trends")

    col_chart, col_text = st.columns([2,1])

    with col_chart:
        with st.container(border=True, horizontal_alignment="center"):
            df_regional_budget = df.groupby(['Year', 'Region'])['Budget'].sum().reset_index()

            fig_trend = px.bar(
                df_regional_budget,
                x='Year',
                y='Budget',
                title="Approved Budget vs Contract Cost (Tight Alignment)",
                log_x=True,
                log_y=True,
                template="plotly_dark"
            )
            st.plotly_chart(fig_trend, use_container_width=True)
    with col_text:
        with st.container(border=True, horizontal_alignment="center"):
            st.markdown("""
                Analysis of funding over time reveals a significant **shift in national priority**:
            
                - **Early Recipients (2021):** Funding was lower and more evenly distributed across all regions.
                - **Surge Years (2022-2024):** The budget surge was overwhelmingly driven by **Region III (Central Luzon)** and **Region IV-A (CALABARZON)**.
                - **Insight:** This trend indicates a focused, massive effort to enhance infrastructure in these key Luzon economic and population centers, potentially at the expense of consistent investment in other regions.
            """)
    st.divider()

    st.subheader("Tight Budget Cost Alignment")

    col_text, col_chart = st.columns([2,1])
    with col_text:
        with st.container(border=True, horizontal_alignment="center"):
            st.text("What is happening na ahahahhaha")
    with col_chart:
        with st.container(border=True, horizontal_alignment="center"):
            fig_cost_align = px.scatter(
                df,
                x='Budget',
                y='ContractCost',
                title="Approved Budget vs Contract Cost (Tight Alignment)",
                log_x=True,
                log_y=True,
                template="plotly_dark"
            )
            st.plotly_chart(fig_cost_align, use_container_width=True)


def render():
    st.title("Insights")
    st.divider()
    df = load_dataset()
    key_insights(df)
    pattern_trends(df)