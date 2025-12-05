import streamlit as st
import pandas as pd

def load_dataset():
    df = pd.read_csv("data/dpwhfloodcontrol.csv")

    # Remove unnamed trailing commas
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

    # Strip whitespace from all string columns
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Replace empty strings with NaN
    df.replace("", pd.NA, inplace=True)

    # Rename columns
    df = df.rename(columns={
        "FundingYear": "Year",
        "ApprovedBudgetForContract": "Budget",
        "StartDate": "StartDate",
        "ActualCompletionDate": "EndDate",
    })

    # Convert types
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Budget"] = pd.to_numeric(df["Budget"], errors="coerce")
    df["ContractCost"] = pd.to_numeric(df["ContractCost"], errors="coerce")

    # Convert dates
    for col in ["StartDate", "EndDate"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Compute duration
    df["DurationDays"] = (df["EndDate"] - df["StartDate"]).dt.days

    return df



# def load_dataset():
#     df = pd.read_csv("data/dpwhfloodcontrol.csv")
#     df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
#     df = df.rename(columns={
#         "FundingYear": "Year",
#         "ApprovedBudgetForContract": "Budget",
#         "StartDate": "StartDate",
#         "ActualCompletionDate": "EndDate",
#     })
#     # Ensure correct types
#     if "Year" in df.columns:
#         df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
#     if "Budget" in df.columns:
#         df["Budget"] = pd.to_numeric(df["Budget"], errors="coerce")

#     #Converting ContractCost from a str into an int
#     cost_col = 'ContractCost'
#     df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

#     #Converting the date string into dates
#     date_cols = ['StartDate', 'EndDate']
#     for col in date_cols:
#         df[col] = pd.to_datetime(df[col], errors="coerce")

#     df['DurationDays'] = (df['EndDate'] - df['StartDate']).dt.days
#     #Should I drop rows that have a missing date
#     #df = df.dropna(subset=[cost_col, 'DurationDays'])

#     return df
