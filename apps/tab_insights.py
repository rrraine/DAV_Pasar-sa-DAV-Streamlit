import streamlit as st
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
    st.subheader("Concentration of Contracts")

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


def anomalies(df):
    if df.empty:
        st.warning("No data found")
        return
    st.header("Anomalies")
    st.subheader("Tight Budget Cost Alignment")

    col_text, col_chart = st.columns([1, 2])
    with col_text:
        with st.container(border=True, horizontal_alignment="center"):
            st.markdown("""
                Comparison of Approved Budget vs Contract Cost

                The scatter diagram for Approved Budget and Contract Cost reveals a near-perfect linear relationsship
                ,confirming the the DPWH is successful at **cost control** and reliably stays within the budget. 
                - The high correlation (typically **R = 0.95**) confirms that the planned budget is an excellent predictor
                    of the final cost.
                - However, this tight alignment suggest a structural issue: **Weak Competition**. Since contractors rarely
                    bid significantly below the maximum approved budget, the process consistently minimizes risk for the agency but
                    **fails to maximize public savings** through competitive price reduction.
            """)
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
    st.divider()
    st.subheader("Financial Disconnect: The Oversight Paradox")

    col_plot, col_text = st.columns([2, 1])
    with col_plot:
        with st.container(border=True, horizontal_alignment="center"):
            fig_scatter = px.scatter(
                df[df['ContractCost'] < df['ContractCost'].quantile(0.95)],
                y='ContractCost',
                x='DurationDays',
                log_y=True,
                title="Cost vs Duration: Weak Correlation (r = 0.22)",
                labels={
                    'DurationDays': 'Project Duration(Days)',
                    'ContractCost': 'Contract Cost (Log Scale)',
                }
            )
            fig_scatter.update_layout(template="plotly_dark", height=450)
            st.plotly_chart(fig_scatter, use_container_width=True)
    with col_text:
        with st.container(border=True, horizontal_alignment="center"):
            st.markdown("""
                The data reveals a significant financial disconnect where project duration
                is a very poor predictor of contract cost (r = 0.22)
                
                This suggest that project cost are primarily driven by factors other than time, such as:
                - **Initial Scope and Complexity**
                - **Risk Premium**
                - **Resource Intensity**
            """)
    st.divider()


def recommendation(df):
    st.subheader("Recommendations to the DPWH")

def render():
    st.title("Insights")
    st.divider()
    df = load_dataset()
    key_insights(df)
    pattern_trends(df)
    anomalies(df)