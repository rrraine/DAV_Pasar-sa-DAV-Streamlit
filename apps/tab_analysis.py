# tab_analysis_3d.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
import plotly.express as px

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

# Run
if __name__ == "__main__":
    render()