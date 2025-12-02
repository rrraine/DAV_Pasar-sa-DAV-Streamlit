import streamlit as st
import pandas as pd

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
