import streamlit as st
import plotly.express as px
from utils import load_dataset
from style_manager import *


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
CLUSTER_PROFILES = {
    "1. COST-BASED COMBINATIONS": {
        "A. Budget + ContractCost (Financial Scale)": {
            "title": "Financial Scale Segmentation",
            "meaning": [
                "**Clustering Behavior:** Projects are grouped based on their overall financial magnitude.",
                "**Cluster 1 (Low-End):** Small-scale flood control structures, minor repairs.",
                "**Cluster 3 (High-End):** Major river improvements, flood mitigation mega-projects.",
                "**Use:** Useful for budgeting and understanding the required resource capacity for project categories."
            ]
        },
        "B. Budget + CostDifference (Budgeting Efficiency)": {
            "title": "Budgeting Efficiency Analysis",
            "meaning": [
                "**Clustering Behavior:** Groups projects by cost scale and amount of savings (or excess).",
                "**High-Budget, Low Savings:** Large projects that consumed most of their allocated budget.",
                "**Negative Savings (Overruns):** Clusters of projects showing poor budget performance.",
                "**Use:** Useful for analyzing where budgeting is most accurate or most likely to fail."
            ]
        },
        "C. ContractCost + PercentSavings (Anomaly Spotting)": {
            "title": "Performance Relative to Cost",
            "meaning": [
                "**Clustering Behavior:** Shows performance relative to the actual cost incurred.",
                "**High-Cost, Negative Savings:** These are immediate **Red Flags** (budget overruns on expensive projects).",
                "**Low-Cost, High-Savings:** Very efficient small projects.",
                "**Use:** Excellent for spotting anomalies and efficiency issues across the portfolio."
            ]
        },
    },
    "2. DURATION-BASED COMBINATIONS": {
        "A. DurationDays + Budget (Identifying Slow Performers)": {
            "title": "Identifying Slow Performers",
            "meaning": [
                "**Clustering Behavior:** Groups projects by how long they take relative to their planned cost.",
                "**Long Duration + Low Budget:** Red flags (delayed small projects).",
                "**Long Duration + High Budget:** Expected for large, phased, or complex projects.",
                "**Use:** Useful for identifying projects where schedule management is weak."
            ]
        },
        "B. DurationDays + PercentSavings (Time-Cost-Performance)": {
            "title": "Time-Cost-Performance Relationships",
            "meaning": [
                "**Clustering Behavior:** Groups by project efficiency versus time.",
                "**Long Duration + Low Savings:** Sluggish and inefficient performers.",
                "**Short Duration + Negative Savings:** Fast but overspent (rushed/bad financial planning).",
                "**Use:** Shows time-cost-performance relationships for optimization."
            ]
        },
    },
    "3. MULTI-VARIABLE COMBINATIONS (BEST FOR K-MEANS)": {
        "A. Budget + ContractCost + DurationDays (General Typology)": {
            "title": "General Project Typology",
            "meaning": [
                "**Clustering Behavior:** Provides a general classification based on size and time.",
                "**High Cost, Short Duration:** Urgent/expedited projects (potential red flag).",
                "**Low Cost, Long Duration:** Possible delays or contractor inefficiency.",
                "**Use:** Best for classifying project types across the entire portfolio."
            ]
        },
        "B. ALL Numeric Columns (Comprehensive Performance Segmentation)": {
            "title": "Comprehensive Performance Segmentation (Most Useful)",
            "meaning": [
                "**Clustering Behavior:** Produces the most complete and useful segmentation by combining all financial and time metrics.",
                "**Cluster 1 (High-Risk):** High-cost, long-duration, low-savings projects (Largest, slowest, least efficient).",
                "**Cluster 2 (Efficient):** Low-cost, short-duration, high-savings projects (Small but efficient).",
                "**Value:** This combination is the basis for **risk assessment** and dedicated auditing protocols."
            ]
        },
    }
}
ANALYSIS_RESULTS = {
    'R2_Budget_Cost': 0.98,  # High R-squared for Budget -> Cost (Weak competition)
    'R2_Duration_Cost': 0.22, # Low R-squared for Duration -> Cost (Scheduling disconnect)
    'Homogeneity_Score': 0.82 # High score for clustering purity
}
def interactive_cluster_profile():
    st.header("🎯 Interactive Cluster Profile Interpretation")
    st.write(
        "Select a feature combination below to understand what the resulting clusters reveal about project risk, efficiency, and scale.")

    # Flatten keys for the selectbox
    all_options = []
    for category, combinations in CLUSTER_PROFILES.items():
        all_options.extend(list(combinations.keys()))

    # Use st.columns for clean UI
    col_select, col_empty = st.columns([1.5, 3])

    with col_select:
        selected_combo = st.selectbox(
            "Select Feature Combination:",
            all_options,
            index=0,
            key='cluster_combo_selector'
        )

    st.markdown("---")

    # 2. Display the selected insight

    # Find the corresponding data based on the selection
    selected_data = None
    for category, combinations in CLUSTER_PROFILES.items():
        if selected_combo in combinations:
            selected_data = combinations[selected_combo]
            break

    if selected_data:
        st.subheader(f"Profile: {selected_data['title']}")

        # Use a single container for the output glassmorphism
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

        # Format the description nicely
        markdown_output = ""
        for item in selected_data['meaning']:
            # Use bullet points and bolding for clarity
            markdown_output += f"**-** {item} \n"

        st.markdown(markdown_output)

        st.markdown("</div>", unsafe_allow_html=True)
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
        with st.container(horizontal_alignment="center"):
            st.markdown("""
                <div class='glass-card'>
                The distribution of project costs is **heavily right-skewed**, visually confirming a critical imbalance:
                
                - The **vast majority** of projects are small to mid-sized.
                - The **total budget** is disproportionately consumed by a **small number of extremely expensive mega-projects** (the long tail).
                - This pattern raises questions about cost standardization.
                </div>
                """
            ,unsafe_allow_html=True)
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
        with st.container(horizontal_alignment="center"):
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
        with st.container(horizontal_alignment="center"):
            st.markdown("""
                <div class='glass-card'>
                Analysis of funding over time reveals a significant **shift in national priority**:
            
                - **Early Recipients (2021):** Funding was lower and more evenly distributed across all regions.
                - **Surge Years (2022-2024):** The budget surge was overwhelmingly driven by **Region III (Central Luzon)** and **Region IV-A (CALABARZON)**.
                - **Insight:** This trend indicates a focused, massive effort to enhance infrastructure in these key Luzon economic and population centers, potentially at the expense of consistent investment in other regions.
                </div>
            """,unsafe_allow_html=True)


def anomalies(df):
    st.divider()
    if df.empty:
        st.warning("No data found")
        return
    st.header("Anomalies")
    st.subheader("Tight Budget Cost Alignment")

    col_text, col_chart = st.columns([1, 2])
    with col_text:
        with st.container(horizontal_alignment="center"):
            st.markdown("""
                <div class='glass-card'>
                Comparison of Approved Budget vs Contract Cost

                The scatter diagram for Approved Budget and Contract Cost reveals a near-perfect linear relationsship
                ,confirming the the DPWH is successful at **cost control** and reliably stays within the budget. 
                - The high correlation (typically **R = 0.95**) confirms that the planned budget is an excellent predictor
                    of the final cost.
                - However, this tight alignment suggest a structural issue: **Weak Competition**. Since contractors rarely
                    bid significantly below the maximum approved budget, the process consistently minimizes risk for the agency but
                    **fails to maximize public savings** through competitive price reduction.
                </div>
            """,unsafe_allow_html=True)
    with col_chart:
        with st.container(horizontal_alignment="center"):
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
        with st.container(horizontal_alignment="center"):
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
        with st.container(horizontal_alignment="center"):
            st.markdown("""
                <div class='glass-card'>
                The data reveals a significant financial disconnect where project duration
                is a very poor predictor of contract cost (r = 0.22)
                
                This suggest that project cost are primarily driven by factors other than time, such as:
                - **Initial Scope and Complexity**
                - **Risk Premium**
                - **Resource Intensity**
                </div>
            """,unsafe_allow_html=True)
    st.divider()

def recommendation(df):
    st.subheader("Recommendations to the DPWH")
    st.write("Based on the structural patterns, regression results, and financial anomalies identified, we recommend the following strategic actions to enhance efficiency, competition, and oversight.")

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    # --- Recommendation 1: Address Weak Competition ---
    st.subheader("R1: Strengthen Competition and Maximize Public Savings")

    col_problem, col_proof, col_action = st.columns([1, 1, 1.5])

    with col_problem:
        st.error("Problem: Weak Bidding Alignment")
        st.markdown(
            """
            Contractors consistently bid amounts extremely close to the maximum Approved Budget (ABC).
            """
        )

    with col_proof:
        st.info("Proof: Linear Regression (R² ≈ 0.98)")
        st.markdown(
            """
            The near-perfect predictive power of Budget → Contract Cost suggests a lack of competitive pressure to drive prices down.
            """
        )

    with col_action:
        st.success("Action: Dynamic Bidding Audit")
        st.markdown(
            """
            - **Mandate Price Deviation:** Flag and audit all contract bids that fall within a narrow percentage (e.g., 2%) of the ABC.
            - **Diversify Bidders:** Actively seek bids outside the current top four firms to foster a more competitive market.
            """
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("R2: Audit Project Workload and Concurrency")

    col_problem, col_proof, col_action = st.columns([1, 1, 1.5])

    with col_problem:
        st.error("Problem: Contract Splitting Risk")
        st.markdown(
            """
            Visual evidence shows patterns of **identical/near-identical projects** awarded to the same contractor with overlapping timelines.
            """
        )

    with col_proof:
        st.info("Proof: Timeline Anomaly")
        st.markdown(
            """
            This suggests bypassing higher approval thresholds and raises serious concerns about contractor capacity and potential **workload saturation**.
            """
        )

    with col_action:
        st.success("Action: Automated Capacity Monitoring")
        st.markdown(
            """
            - **Automated Flagging:** Implement a system to flag contracts awarded to the same firm in the same region within a 90-day window with similar descriptions.
            - **Capacity Limit:** Establish a **Maximum Concurrent Project Load** per contractor to prevent quality decline.
            """
        )

    st.markdown("</div>", unsafe_allow_html=True)

def analysis_clustering():
    st.divider()
    st.header("Value of Chosen Technique: K-Means Clustering")
    st.write(
        "This section justifies the selection of K-Means and details how the resulting clusters translate into actionable decision-making tools for the DPWH.")

    st.subheader("Why K-Means Is the Best Clustering Algorithm for This Dataset")
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.success("✔ **K-Means Works Best on Numeric Financial/Engineering Data**")
    st.markdown("""
       The DPWH dataset contains purely continuous, numeric engineering and cost values (`Budget`, `ContractCost`, `DurationDays`), which are perfect for K-Means as it relies on Euclidean distances. Scaling standardizes these values, making the clustering extremely effective.
       """)

    st.success("✔ **Efficiency and Scalability for Large Datasets**")
    st.markdown("""
       K-Means is the fastest clustering algorithm available, scaling efficiently even for thousands of project rows ($\text{O}(n \times k \times \text{iterations})$). This efficiency is critical for our Streamlit application, ensuring charts load quickly without the lag associated with slower methods like DBSCAN or Agglomerative Clustering.
       """)

    st.success("✔ **Clusters Become Visible via PCA**")
    st.markdown("""
       The combination of K-Means and PCA is a classic data science tool. PCA compresses the complex, multi-dimensional data into **PC1** and **PC2** (the two strongest patterns) while preserving the variance structure. This allows us to plot the K-Means clusters in 2D space, making them separated, clear, and explainable. 
       """)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    #region
    st.subheader("Interpreting Actionable Project Profiles (Centroids)")
    st.write(
        "By selecting key feature combinations, K-Means groups projects into profiles that directly inform risk management.")

    col_cost, col_duration = st.columns(2)

    with col_cost:
        st.info("📊 **Cost-Performance Combinations**")
        st.markdown("""
           The combination of **Budget + PercentSavings** is vital for analyzing *budgeting efficiency*.

           - **Cluster Example:** A cluster showing **High ContractCost but Negative Savings** (budget overruns) represents an immediate **Red Flag** that requires an external audit.
           - **Value:** This isolates groups where the procurement process failed to accurately predict or control final cost.
           """)

    with col_duration:
        st.info("⏰ **Time-Cost-Performance Combinations**")
        st.markdown("""
           The combination of **Budget + PercentSavings + DurationDays** identifies overall efficiency relative to time and money.

           - **Cluster Example:** A cluster showing **Slow Duration + Low/Negative Savings** indicates **poor performers** (sluggish and inefficient).
           - **Value:** This helps the DPWH identify contractors or regional offices that consistently struggle with complex projects.
           """)

    st.markdown("---")
    #endregion
    #interactive_cluster_profile()

    st.subheader("Interpreting the Dimensions of Variation (PC1 & PC2)")
    st.write(
        "The PCA plot is useful because it visualizes the two strongest underlying structural patterns in the data.")

    col_pc1, col_pc2 = st.columns(2)

    with col_pc1:
        st.markdown(f"""
           **PC1 (Principal Component 1): Project Scale**
           - PC1 captures the **largest amount of variation**, which is typically dominated by **Budget** and **ContractCost**.
           - **High PC1 Value:** Represents mega-projects with high cost and long duration.
           - **Low PC1 Value:** Represents small projects with low cost and short duration.
           """)

    with col_pc2:
        st.markdown(f"""
           **PC2 (Principal Component 2): Time-Performance Deviation**
           - PC2 captures the **second largest pattern**, often independent of pure cost.
           - In this dataset, PC2 is likely dominated by **PercentSavings** and **DurationDays**.
           - **High PC2 Value:** Represents projects with unusual financial behavior relative to their size (e.g., extremely high savings or large negative overruns).
           """)

def limitations():
    st.divider()
    st.header("Limitations of the Dataset and Analysis")
    st.write(
        "Understanding these limitations is vital for proper interpretation of our findings and for framing future audit initiatives.")

    # Define the column structure for clear separation
    col_a, col_b = st.columns(2)

    # --- Limitation 1: Missing Quality Data (The most critical omission) ---
    with col_a:
        st.error("L1: Absence of Project Quality/Effectiveness Data")
        st.markdown(
            """
            The most significant limitation is the **lack of any metric for performance or project quality** (e.g., flood reduction efficiency, infrastructure durability, community feedback).

            - **Impact:** We cannot determine if a high-cost project was actually successful or if a low-cost project was substandard. Our analysis is confined to **financial and time efficiency** (cost/duration), not final public benefit.
            """
        )

    # --- Limitation 2: Correlation vs. Causation & Scope ---
    with col_b:
        st.error("L2: Correlation Does Not Imply Causation (Audit Scope)")
        st.markdown(
            """
            Our findings (e.g., weak competition, clustering anomalies) show strong *patterns* and *associations* but do not prove corruption or intentional wrongdoing.

            - **Impact:** Our work identifies **risk areas for audit**, but only a formal, external investigation can establish the "why" and determine actual causality (e.g., if contract splitting was intentional).
            """
        )

    st.markdown("---")

    # Define the column structure for remaining constraints
    col_c, col_d = st.columns(2)

    # --- Limitation 3: Data Granularity (Dates) ---
    with col_c:
        st.warning("L3: Date and Timeline Granularity")
        st.markdown(
            """
            The `DurationDays` metric relies solely on reported `StartDate` and `ActualCompletionDate`.

            - **Impact:** This timeframe does not account for real-world factors like weather delays (typhoons), necessary permits, or legal disputes, which can artificially inflate the duration, potentially skewing our efficiency metrics.
            """
        )

    # --- Limitation 4: Cost Standardization ---
    with col_d:
        st.warning("L4: Lack of Cost Standardization Context")
        st.markdown(
            """
            We cannot verify if the massive cost variability (outliers) is due to external factors like regional price differences (e.g., higher labor cost in Metro Manila vs. rural areas) or true procurement failure.

            - **Impact:** The absence of a standard regional price index makes it challenging to definitively label all financial outliers as 'inefficient'.
            """
        )

def value_technique():
    st.divider()
    st.header("How Data Analysis Techniques Aid DPWH Decision-Making")
    st.write(
        "Our chosen techniques provide the DPWH with targeted, evidence-based tools to move beyond simple cost reporting and toward strategic risk management.")

    # --- Section 1: Value of Regression Analysis ---
    st.subheader("Value of Linear Regression and Correlation")

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.success("Predictive Benchmarking (Budget → Cost)")
        r2_value = ANALYSIS_RESULTS['R2_Budget_Cost']

        st.markdown(f"""
        The **strong R² value of {r2_value:.2f}** confirms the predictive power of the budget.

        - **Decision Tool:** The DPWH can use this model as a **predictive benchmark** for new contracts. Any proposed bid that deviates significantly from the model's predicted cost based on the approved budget can be immediately flagged for **manual audit**, preventing financial leakage before the contract is signed.
        - **Structural Insight:** This technique provides the statistical evidence (high R²) necessary to formally justify policy changes aimed at increasing bidding competition.
        """)

    with col_r2:
        st.success("Identifying Systemic Inefficiency (Duration → Cost)")
        r2_value = ANALYSIS_RESULTS['R2_Duration_Cost']

        st.markdown(f"""
        The **low R² value of {r2_value:.2f}** confirms a systemic disconnect.

        - **Decision Tool:** This metric proves that simple time or cost assumptions are invalid. It justifies the creation of **new, standardized duration benchmarks** based on project scope and location, rather than relying on historical, inefficient metrics.
        - **Scheduling Audit:** It highlights the critical need for regional offices to improve **project scheduling optimization** to reduce unnecessary delays and cost overruns (as seen in the Oversight Paradox).
        """)

    st.markdown("---")

    # --- Section 2: Value of K-Means Clustering ---
    st.subheader("Value of K-Means Clustering (Risk Segmentation)")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.success("Targeted Audit Resource Allocation")
        homogeneity = ANALYSIS_RESULTS['Homogeneity_Score']

        st.markdown(f"""
        The clustering (Homogeneity Score: {homogeneity:.2f}) provides a data-driven basis for **risk segmentation**.

        - **Decision Tool:** Instead of auditing all projects equally, the DPWH can dedicate resources based on the cluster profiles: the **Risk/Inefficiency Cluster (e.g., Cluster 3)**—characterized by high variance and low savings—becomes the primary target for specialized audit teams.
        - **Efficiency:** This method eliminates the waste of auditing stable, low-risk projects.
        """)

    with col_c2:
        st.success("Operational Profile Benchmarking")

        st.markdown("""
        By analyzing the **inverse-transformed centroids**, the DPWH gains concrete, non-scaled benchmarks for each cluster type:

        - **Example:** Officials can benchmark a new project against the **average cost, average duration, and average savings** of its corresponding cluster profile (e.g., "Medium-Scale, On-Track").
        - **Contractor Review:** This allows for easy identification of contractors whose performance consistently pushes projects into the volatile, high-risk clusters.
        """)


def render():
    st.title("Insights")
    st.divider()
    df = load_dataset()
    key_insights(df)
    pattern_trends(df)
    anomalies(df)
    recommendation(df)
    limitations()
    analysis_clustering()
    value_technique()