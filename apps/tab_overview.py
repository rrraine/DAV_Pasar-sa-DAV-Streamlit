# tab_overview.py
import streamlit as st
import pandas as pd

def display_title_and_overview():
    # st.title("Overview and Dataset")
    st.subheader("Overview")

    st.write("""
        Flooding remains one of the most persistent challenges in the Philippines, severely affecting communities, infrastructure, and local economies. The issue has recently gained national attention due to controversies surrounding the country’s flood control budget—specifically cases of corruption, misuse of funds, and substandard project implementations. These concerns became more relevant after several typhoons devastated different regions, with Bagyong Tino in Cebu serving as a notable example. Understanding how flood control projects are distributed, implemented, and funded is crucial for evaluating whether government resources are being allocated efficiently and effectively.

    """)

# def display_gallery():
#     st.subheader("Typhone Aftermath - Photogallery")
    # add images with captions


def load_dataset():
    st.subheader("Dataset")
    
    file_path = "data/dpwhfloodcontrol.csv"
    df = pd.read_csv(file_path)
    return df

    # try:
    #     df = pd.read_csv(file_path)
    #     st.success("Dataset loaded successfully!")
    #     st.dataframe(df.head(), use_container_width=True)
    #     return df
    # except FileNotFoundError:
    #     st.error(f"File not found: {file_path}. Please ensure the dataset is in the correct path.")
    #     return None
    
def display_dataset_info(df):
    # st.subheader("Dataset Information")
    
    df_clean = df.loc[:, ~df.columns.str.startswith("Unnamed")]  # Remove unnamed columns

    st.write(f"**Rows:** {df_clean.shape[0]} | **Columns:** {df_clean.shape[1]}")

    with st.expander("Show Detailed Dataset Information", expanded=False):
        st.write("### 📌 Data Summary")
        st.write(df.describe(include="all"))

        st.write("### 🔢 Numeric Summary")
        st.write(df.describe())

        st.write("### ❗ Missing Values")
        st.write(df.isnull().sum())

    st.divider()

def display_filters(df):
    # Exclude unnamed columns
    df_clean = df.loc[:, ~df.columns.str.startswith("Unnamed")]

    st.write("""
    The dataset used in this project was sourced from [Kaggle’s DPWH Flood Control Projects](https://www.kaggle.com/datasets/bwandowando/dpwh-flood-control-projects) dataset. 
    It contains both quantitative and qualitative data on flood control projects implemented by the Department of Public Works and Highways (DPWH) across the Philippines, including information such as project location, contractor, type of work, budget, contract cost, and completion dates.
    """)

    numeric_cols = df_clean.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df_clean.select_dtypes(include=['object']).columns.tolist()

    selected_col = st.selectbox("Select column to filter:", df_clean.columns)

    if selected_col in numeric_cols:
        min_val = float(df_clean[selected_col].min())
        max_val = float(df_clean[selected_col].max())

        filter_range = st.slider(
            f"Filter `{selected_col}` by range:",
            min_val, max_val, (min_val, max_val)
        )

        df_filtered = df_clean[(df_clean[selected_col] >= filter_range[0]) &
                               (df_clean[selected_col] <= filter_range[1])]

    elif selected_col in cat_cols:
        unique_vals = df_clean[selected_col].dropna().unique().tolist()
        selected_vals = st.multiselect(
            f"Select values for `{selected_col}`:",
            unique_vals
        )

        df_filtered = df_clean[df_clean[selected_col].isin(selected_vals)] if selected_vals else df_clean

    else:
        st.info("Column type not supported for filtering.")
        df_filtered = df_clean

    st.dataframe(df_filtered, use_container_width=True)


def chosen_techniques():
    st.subheader("Chosen Data Analysis Techniques")

    st.write("""
    The analysis employs several techniques to extract meaningful insights from the DPWH Flood Control Projects dataset:

    - **Descriptive Analysis:** Used to summarize the dataset and provide an overview of trends, such as the number of projects per region and average budgets, giving a clear picture of overall patterns.  
    - **Correlation Analysis:** Applied to explore relationships between numerical variables, like budget versus contract cost, helping to detect anomalies or inefficiencies in spending.  
    - **Linear Regression:** Utilized to estimate how one variable affects another, such as predicting contract cost based on budget, which can highlight potential overspending or delays.  
    - **Clustering:** Selected to group similar projects or regions based on key attributes, revealing hidden patterns such as contractor performance clusters or regions with comparable flood control needs.
    """)

def objective():
     st.subheader("Objective of the Analysis")
     st.write("""
        The main objective of this analysis is to explore and visualize key insights from the DPWH Flood Control Projects dataset, particularly identifying the top contractors based on the number of projects—both overall and per region—and uncovering patterns in project implementation and resource distribution nationwide.

        **Expanded Objectives:**
        - Determine whether budget allocation aligns with regions most frequently affected by flooding.
        - Compare approved budgets versus contract costs to check for potential overpricing or underspending.
        - Identify contractors that consistently handle large-scale or high-cost projects.
        - Examine project completion timelines to find regions or contractors with delays.
        - Group regions or projects using clustering to uncover hidden patterns related to contractor performance or regional flood control needs.
        - Provide data-driven insights to improve transparency, efficiency, and planning for future flood control initiatives.
        """)


# # footer, no design pa
# def display_group_members():
#     st.subheader("Group: Pasar sa DAV (F1)")
#     st.write("**John Earl Echavez** – [@EarlJohnHub](https://github.com/EarlJohnHub) | **Lorraine Quezada** – [@rrraine](https://github.com/rrraine) | **Aliyah Khaet Regacho** – [@liya28](https://github.com/liya28) | **Harley Reyes** – [@muhadma](https://github.com/muhadma)  ")

# footer 2, with simple design
def display_group_members():
    footer_html = """
    <div style="
        background-color: #ffffff;
        padding: 10px 20px;
        border-top: 2px solid #003366;
        text-align: center;
        font-size: 14px;
        color: #003366;
    ">
        <strong>Group: Pasar sa DAV (F1)</strong><br>
        <strong>John Earl Echavez</strong> – <a href='https://github.com/EarlJohnHub' target='_blank'>@EarlJohnHub</a> | 
        <strong>Lorraine Quezada</strong> – <a href='https://github.com/rrraine' target='_blank'>@rrraine</a> | 
        <strong>Aliyah Khaet Regacho</strong> – <a href='https://github.com/liya28' target='_blank'>@liya28</a> | 
        <strong>Harley Reyes</strong> – <a href='https://github.com/muhadma' target='_blank'>@muhadma</a>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)



# call functions to render the tab
def render():
    display_title_and_overview()
    # display_gallery()

    df = load_dataset()

    if df is not None:
        display_filters(df)
        display_dataset_info(df)
        
    chosen_techniques()
    objective()
    display_group_members()
