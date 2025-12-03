# tab_analysis_3d.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
import plotly.express as px
from streamlit import container

from style_manager import inject_global_css


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def safe_to_numeric(series):
    return pd.to_numeric(series, errors="coerce")

def parse_dates_safe(df, col):
    if col not in df.columns:
        return pd.NaT
    return pd.to_datetime(df[col], errors="coerce")

# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------
@st.cache_data
def load_dataset(path="data/dpwhfloodcontrol.csv"):
    df = pd.read_csv(path)

    # Remove unnamed index-like columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Rename key columns for consistency
    rename_map = {
        "FundingYear": "Year",
        "ApprovedBudgetForContract": "Budget",
        "ContractCost": "ContractCost"
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Convert basic numeric fields
    for col in ["Year", "Budget", "ContractCost"]:
        if col in df.columns:
            df[col] = safe_to_numeric(df[col])

    # Identify date columns
    start_candidates = [
        "StartDate", "Start Date", "CommencementDate", "DateStarted"
    ]
    end_candidates = [
        "ActualCompletionDate", "CompletionDate",
        "CompletedDate", "EndDate"
    ]

    start_col = next((c for c in start_candidates if c in df.columns), None)
    end_col   = next((c for c in end_candidates if c in df.columns), None)

    df["_parsed_start"] = parse_dates_safe(df, start_col)
    df["_parsed_end"]   = parse_dates_safe(df, end_col)

    # Duration in days
    df["DurationDays"] = (df["_parsed_end"] - df["_parsed_start"]).dt.days

    # Budget metrics
    if "Budget" in df.columns and "ContractCost" in df.columns:
        df["CostDifference"] = df["Budget"] - df["ContractCost"]
        df["PercentSavings"] = np.where(
            (df["Budget"].notna()) & (df["Budget"] != 0),
            (df["CostDifference"] / df["Budget"]) * 100,
            np.nan
        )
    else:
        df["CostDifference"] = np.nan
        df["PercentSavings"] = np.nan

    return df

# ---------------------------------------------------------
# Main render
# ---------------------------------------------------------
def render():
    inject_global_css()
    st.title("K-Means Clustering with PCA Visualization")

    df = load_dataset()

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if len(numeric_cols) < 2:
        st.error("Dataset does not contain enough numeric features to run K-Means.")
        return

    st.write("### Dataset Preview")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("⚙️ K-Means Settings")

    col1, col2 = st.columns([1, 1])

    with col1:
        n_clusters = st.slider("Number of Clusters (k):", 2, 10, 3)
        scale_data = st.checkbox("Standardize Data", value=True)

    with col2:
        selected_features = st.multiselect(
            "Select Numeric Columns for Clustering:",
            numeric_cols,
            default=numeric_cols
        )

    if len(selected_features) < 2:
        st.warning("Please select at least TWO numeric features.")
        return

    st.markdown("---")

    # ---------------------------
    # Data Preparation
    # ---------------------------
    df_num = df[selected_features].copy()

    # Handle NaN
    imputer = SimpleImputer(strategy="mean")
    df_num_imputed = pd.DataFrame(imputer.fit_transform(df_num), columns=selected_features)

    # Scale
    if scale_data:
        scaler = StandardScaler()
        X = scaler.fit_transform(df_num_imputed)
    else:
        X = df_num_imputed.values

    # ---------------------------
    # K-Means
    # ---------------------------
    kmeans = KMeans(n_clusters=n_clusters, n_init=20, random_state=42)
    df["Cluster"] = kmeans.fit_predict(X)

    # ---------------------------
    # PCA for visualization
    # ---------------------------
    pca = PCA(n_components=2)
    pca_coords = pca.fit_transform(X)

    df_plot = df.copy()
    df_plot["PC1"] = pca_coords[:, 0]
    df_plot["PC2"] = pca_coords[:, 1]

    # ---------------------------
    # Output
    # ---------------------------
    st.write("### Clustered Dataset")
    st.dataframe(df_plot, use_container_width=True)

    st.write("### 📊 PCA Visualization of Clusters")

    fig = px.scatter(
        df_plot,
        x="PC1",
        y="PC2",
        color=df_plot["Cluster"].astype(str),
        hover_data=selected_features,
        title=f"PCA Projection of K-Means Clusters (k = {n_clusters})",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("### 🎯 Cluster Centroids (Scaled Feature Space)")
    centroids = pd.DataFrame(kmeans.cluster_centers_, columns=selected_features)
    st.dataframe(centroids, use_container_width=True)

    st.title("Analysis Dashboard")
    st.write(
        "This section presents the regression analyses examining how "
        "Approved Budget, Project Duration, and Contract Cost interact across DPWH Flood Control Projects."
    )

    st.divider()

    # ------------------------------
    # TABS FOR EACH REGRESSION
    # ------------------------------
    tab1, tab2, tab3, tab_summary = st.tabs(
        ["Regression 1: Budget → Cost",
         "Regression 2: Duration → Cost",
         "Regression 3: Budget → Duration",
         "Overall Summary"]
    )

    # ==========================================================
    # TAB 1 — REGRESSION 1
    # ==========================================================
    with tab1:
        st.header("Regression 1: Approved Budget → Contract Cost")
        st.image("res/Regression 1.png", use_container_width=True)

        # Metrics row
        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True, horizontal_alignment="center"):
                st.caption("Slope")
                st.header("0.974")
                #c1.metric("Slope", "0.974")
        with c2:
            with st.container(border=True, horizontal_alignment="center"):
                st.caption("Intercept")
                st.header("610,409")
                #c2.metric("Intercept", "610,409")
        with c3:
            with st.container(border=True, horizontal_alignment="center"):
                st.caption("R² Score")
                st.header("0.977")
                #c3.metric("R² Score", "0.977")

        st.markdown("""
        <div class='glass-container'>
    ### Interpretation
    There is a near-perfect linear relationship between the Approved Budget and Contract Cost.  
    Higher budgets result in proportionally higher costs, showing strong consistency in expenditure behavior.

    ### Key Notes
    - Points align tightly with the regression line.  
    - Very few projects deviate from the budget.  
    - The high R² shows the model captures most cost variability.  

    ### Conclusion
    Budget is the **strongest and most reliable predictor** of Contract Cost.  
        </div>
    """,unsafe_allow_html=True)

    # ==========================================================
    # TAB 2 — REGRESSION 2
    # ==========================================================
    with tab2:
        st.header("Regression 2: Project Duration → Contract Cost")
        st.image("res/Regression 2.png", use_container_width=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True, horizontal_alignment="center"):
                st.caption("Slope")
                st.header("86,178")
            # c1.metric("Slope", "86,178")
        with c2:
            with st.container(border=True, horizontal_alignment="center"):
                st.caption("Intercept")
                st.header("34,268,617")
                #c2.metric("Intercept", "34,268,617")
        with c3:
            with st.container(border=True, horizontal_alignment="center"):
                st.caption("R² Score")
                st.header("0.086")

                #c3.metric("R² Score", "0.086")

        st.markdown("""
        <div class='glass-card'>
    ### Interpretation
    Project Duration shows **very weak predictive power** for Contract Cost.  
    Costs vary widely even for similar durations, indicating time is not the main driver of expenditure.

    ### Key Notes
    - Scatter is highly dispersed.  
    - Duration explains only 8.6% of cost variation.  
    - Long durations do **not** reliably mean higher costs.

    ### Conclusion
    Duration alone cannot explain or estimate Contract Costs effectively.
        </div>
    """,unsafe_allow_html=True)

    # ==========================================================
    # TAB 3 — REGRESSION 3
    # ==========================================================
    with tab3:
        st.header("Regression 3: Approved Budget → Project Duration")
        st.image("res/Regression 3.png", use_container_width=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            with st.container(border=True, horizontal_alignment="center"):
                st.caption("Slope")
                st.header("1.001 × 10⁻⁶")
                #c1.metric("Slope", "1.001 × 10⁻⁶")
        with c2:
            with st.container(border=True, horizontal_alignment="center"):
                st.caption("Intercept")
                st.header("190.02 days")
                #c2.metric("Intercept", "190.02 days")
        with c3:
            with st.container(border=True, horizontal_alignment="center"):
                st.caption("R² Score")
                st.header("0.089")
                #c3.metric("R² Score", "0.089")

        st.markdown("""
        <div class='glass-card'>
    ### Interpretation
    Approved Budget has **almost no influence** on Project Duration.  
    Timelines vary drastically across all budget levels.

    ### Key Notes
    - Scatter is extremely spread out.  
    - Only 8.9% of timeline variability is explained by budget.  
    - High-budget projects are not consistently faster or slower.

    ### Conclusion
    Budget is **not** a predictor of how long a project will take.
        </div>
    """,unsafe_allow_html=True)

    # ==========================================================
    # TAB 4 — OVERALL SUMMARY
    # ==========================================================
    with tab_summary:
        st.header("Overall Summary")
        st.markdown("""
        
        <div class='glass-card'>
    ### Synthesis of Findings
    Across the three regressions, one pattern is crystal clear:

    **Contract Cost is tightly tied to the Approved Budget, while Project Duration is largely independent of both.**

    ---

    ### Comparison Table

    | Regression | R² Score | Interpretation |
    |-----------|----------|----------------|
    | **Budget → Cost** | **0.977** | Extremely strong relationship; budget predicts cost almost perfectly. |
    | **Duration → Cost** | 0.086 | Very weak; time spent does not dictate cost. |
    | **Budget → Duration** | 0.089 | Very weak; budget does not determine timeline. |

    ---

    ### Final Interpretation
    - Costs follow budgets **very closely**.  
    - Timelines are unpredictable and affected by factors outside these variables.  
    - The contrast between strong financial correlation and weak time-based correlations highlights the need to **scrutinize efficiency, delays, and project execution practices**.
    
    </div>
    """,unsafe_allow_html=True)

