# tab_dataexploration.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_dataset

# def load_dataset():
#     df = pd.read_csv("data/dpwhfloodcontrol.csv")
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
#     return df


# Filter dataset (inside tab)
def filter_dataset(df):
    st.subheader("Budget Allocation")
    
    # Region filter
    regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
    selected_region = st.selectbox("Select Region:", regions)
    
    # Year range filter
    if "Year" in df.columns:
        min_year = int(df["Year"].min())
        max_year = int(df["Year"].max())
        year_range = st.slider("Select Funding Year Range:",
                               min_value=min_year,
                               max_value=max_year,
                               value=(min_year, max_year))
    else:
        year_range = (None, None)
    
    # Budget filter
    if "Budget" in df.columns:
        min_budget = float(df["Budget"].min())
        max_budget = float(df["Budget"].max())
        budget_range = st.slider("Select Budget Range:",
                                 min_value=min_budget,
                                 max_value=max_budget,
                                 value=(min_budget, max_budget))
    else:
        budget_range = (None, None)
    
    # Apply filters
    df_filtered = df.copy()
    if year_range[0] is not None:
        df_filtered = df_filtered[(df_filtered["Year"] >= year_range[0]) & (df_filtered["Year"] <= year_range[1])]
    if budget_range[0] is not None:
        df_filtered = df_filtered[(df_filtered["Budget"] >= budget_range[0]) & (df_filtered["Budget"] <= budget_range[1])]
    if selected_region != "All":
        df_filtered = df_filtered[df_filtered["Region"] == selected_region]
    
    return df_filtered


# Key Statistics
def display_key_statistics(df):
    st.subheader("Key Statistics")

    budget_col = "Budget" # ApprovedBudgetForContract
    cost_col = "ContractCost"

    # st.write("Columns detected:", df.columns.tolist())

    # Check if columns exist
    if budget_col not in df.columns or cost_col not in df.columns:
        st.error("Dataset must contain 'ApprovedBudgetForContract' and 'ContractCost' columns.")
        return

    #Convert to numeric (handles TypeError from strings) 
    df[budget_col] = pd.to_numeric(df[budget_col], errors="coerce")
    df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

    # Helper for peso formatting
    def peso(x):
        try:
            return f"₱{x:,.2f}"
        except:
            return "N/A"


    stats = {
        "Statistic": [
            "Mean (Average)",
            "Mode",
            "Standard Deviation (STD)",
            "Variance",
            "Minimum (Min)",
            "Maximum (Max)",
            "Range (Max - Min)",
            "25th Percentile (Q1)",
            "50th Percentile (Median)",
            "75th Percentile (Q3)"
        ],
        budget_col: [
            peso(df[budget_col].mean()),
            peso(df[budget_col].mode().iloc[0]),
            peso(df[budget_col].std()),
            f"{df[budget_col].var():.2e}",
            peso(df[budget_col].min()),
            peso(df[budget_col].max()),
            peso(df[budget_col].max() - df[budget_col].min()),
            peso(df[budget_col].quantile(0.25)),
            peso(df[budget_col].median()),
            peso(df[budget_col].quantile(0.75)),
        ],
        cost_col: [
            peso(df[cost_col].mean()),
            peso(df[cost_col].mode().iloc[0]),
            peso(df[cost_col].std()),
            f"{df[cost_col].var():.2e}",
            peso(df[cost_col].min()),
            peso(df[cost_col].max()),
            peso(df[cost_col].max() - df[cost_col].min()),
            peso(df[cost_col].quantile(0.25)),
            peso(df[cost_col].median()),
            peso(df[cost_col].quantile(0.75)),
        ],
        "Interpretation": [
            "On average, contract costs are slightly lower than the approved budgets, indicating cost savings.",
            "Both have the same most frequent value, suggesting a standard cost level.",
            "Variability in approved budgets and contract costs is nearly the same.",
            "Variances confirm similar dispersion.",
            "Smallest contract cost is slightly lower than the smallest approved budget.",
            "Maximum contract cost is lower than the maximum approved budget.",
            "Approved budgets have a wider range than contract costs.",
            "25% of projects have lower budgets and even lower contract costs.",
            "Median values are nearly identical, showing good budget alignment.",
            "Upper-end projects show contract costs slightly lower than budgets."
        ]
    }

    # Convert to DataFrame
    stats_df = pd.DataFrame(stats)

    # Display nicely
    st.dataframe(stats_df, use_container_width=True)




# Heatmap, Boxplot, Histogram

def heatmap_boxplot_histogram(df):
    st.subheader("Additional Visualizations")

    # Display the heatmap
    st.write("### Correlation Heatmap")

    col1, col2 = st.columns(2)
    with col1:
        st.write("""
                The heatmap shows correlations between key numeric variables, such as Approved Budget, Contract Cost, and Duration. Surprisingly, Approved Budget and Contract Cost are almost uncorrelated (r ≈ –0.01), suggesting inconsistencies due to rebudgeting, reporting differences, or project management gaps. Project cost and duration are also weakly related (r ≈ 0.03), and smaller projects tend to have slightly higher cost overruns (r ≈ –0.20). Overall, the heatmap reveals weak relationships among major variables, highlighting potential gaps in how budgets, timelines, and costs are managed across projects and regions.
                """)
    with col2:
        st.image("res/heatmap.png", use_container_width=True)

    # Display boxplot and histogram side by side
    st.write("### Boxplot and Histogram")
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Boxplot")
        st.write("""
                The box plot visualizes the spread and outliers in project budgets and costs. Most projects cluster between ₱25M and ₱85M, but there are several outliers representing unusually high or low project costs. These outliers may reflect large-scale national or regional projects or potential inefficiencies in budgeting. This confirms the pattern seen in the histogram: the majority of projects follow typical funding ranges, while a few disproportionately expensive ones have a significant impact on overall spending.
                """)
        st.image("res/boxplot.png", use_container_width=True)

    with col2:
        st.write("#### Histogram")
        
        st.write("""
            The histogram shows the distribution of Approved Budgets and Contract Costs for flood control projects. Both are right-skewed, meaning most projects fall within lower-to-mid budget ranges, while a few very expensive “mega-projects” pull the average upward. 
            The mean contract cost is ₱55.52M, slightly lower than the mean approved budget of ₱56.71M, and the mode for both is ₱49M, indicating a common standard project cost. Overall, this chart highlights that while most projects are within typical budgets, a small number of large projects dominate total spending.
            """)
        st.image("res/histogram.png", use_container_width=True)


# Visualizations
def plot_budget_per_region(df):
    if "Budget" in df.columns and "Region" in df.columns:
        st.subheader("Budget Allocation per Region")
        fig = px.bar(df.groupby("Region")["Budget"].sum().reset_index(),
                     x="Region", y="Budget",
                     title="Total Budget per Region",
                     text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

def plot_budget_per_year(df):
    if "Budget" in df.columns and "Year" in df.columns:
        st.subheader("Budget Allocation per Year")
        fig = px.bar(df.groupby("Year")["Budget"].sum().reset_index(),
                     x="Year", y="Budget",
                     title="Total Budget per Funding Year",
                     text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

def plot_projects_per_year(df):
    if "Year" in df.columns:
        st.subheader("Number of Projects per Year")
        fig = px.bar(df.groupby("Year").size().reset_index(name="Projects"),
                     x="Year", y="Projects",
                     title="Projects per Funding Year",
                     text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

def interactive_projects_per_region(df):
    if "Region" in df.columns and "Year" in df.columns:
        st.subheader("Projects per Region")
        regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
        selected_region = st.selectbox("Select Region for Detailed View:", regions)
        
        if selected_region != "All":
            df_region = df[df["Region"] == selected_region]
        else:
            df_region = df

        fig = px.bar(df_region.groupby("Year").size().reset_index(name="Projects"),
                     x="Year", y="Projects",
                     title=f"Projects in {selected_region}" if selected_region != "All" else "Projects by Year",
                     text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

# kulang pa ng overlapping projects per region per year visualization

def render():
    df = load_dataset()
    
    # Display stats and charts
    display_key_statistics(df)

    # Heatmap, Boxplot, Histogram
    heatmap_boxplot_histogram(df)

     # Filter inside the tab
    df_filtered = filter_dataset(df)
    plot_budget_per_region(df_filtered)
    plot_budget_per_year(df_filtered)
    plot_projects_per_year(df_filtered)
    interactive_projects_per_region(df_filtered)
