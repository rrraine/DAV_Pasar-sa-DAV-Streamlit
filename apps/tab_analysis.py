import streamlit as st

def render():
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
        c1.metric("Slope", "0.974")
        c2.metric("Intercept", "610,409")
        c3.metric("R² Score", "0.977")

        st.markdown("""
### Interpretation
There is a near-perfect linear relationship between the Approved Budget and Contract Cost.  
Higher budgets result in proportionally higher costs, showing strong consistency in expenditure behavior.

### Key Notes
- Points align tightly with the regression line.  
- Very few projects deviate from the budget.  
- The high R² shows the model captures most cost variability.  

### Conclusion
Budget is the **strongest and most reliable predictor** of Contract Cost.  
""")

    # ==========================================================
    # TAB 2 — REGRESSION 2
    # ==========================================================
    with tab2:
        st.header("Regression 2: Project Duration → Contract Cost")
        st.image("res/Regression 2.png", use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Slope", "86,178")
        c2.metric("Intercept", "34,268,617")
        c3.metric("R² Score", "0.086")

        st.markdown("""
### Interpretation
Project Duration shows **very weak predictive power** for Contract Cost.  
Costs vary widely even for similar durations, indicating time is not the main driver of expenditure.

### Key Notes
- Scatter is highly dispersed.  
- Duration explains only 8.6% of cost variation.  
- Long durations do **not** reliably mean higher costs.

### Conclusion
Duration alone cannot explain or estimate Contract Costs effectively.
""")

    # ==========================================================
    # TAB 3 — REGRESSION 3
    # ==========================================================
    with tab3:
        st.header("Regression 3: Approved Budget → Project Duration")
        st.image("res/Regression 3.png", use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Slope", "1.001 × 10⁻⁶")
        c2.metric("Intercept", "190.02 days")
        c3.metric("R² Score", "0.089")

        st.markdown("""
### Interpretation
Approved Budget has **almost no influence** on Project Duration.  
Timelines vary drastically across all budget levels.

### Key Notes
- Scatter is extremely spread out.  
- Only 8.9% of timeline variability is explained by budget.  
- High-budget projects are not consistently faster or slower.

### Conclusion
Budget is **not** a predictor of how long a project will take.
""")

    # ==========================================================
    # TAB 4 — OVERALL SUMMARY
    # ==========================================================
    with tab_summary:
        st.header("Overall Summary")
        st.markdown("""
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
""")

