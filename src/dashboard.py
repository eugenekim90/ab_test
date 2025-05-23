import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ab_test_analysis import ABTestAnalyzer
from statsmodels.stats.power import TTestPower

# Set page config
st.set_page_config(
    page_title="A/B Test Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("A/B Test Analysis Dashboard")
    st.write("Configure your A/B test parameters and analyze the results.")
    
    # Sidebar for test configuration
    st.sidebar.header("Test Configuration")
    
    # Test parameters
    control_rate = st.sidebar.slider(
        "Control Conversion Rate",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.01,
        help="Expected conversion rate for the control group"
    )
    
    treatment_rate = st.sidebar.slider(
        "Treatment Conversion Rate",
        min_value=0.0,
        max_value=1.0,
        value=0.12,
        step=0.01,
        help="Expected conversion rate for the treatment group"
    )
    
    sample_size = st.sidebar.slider(
        "Sample Size per Group",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100,
        help="Number of users in each group"
    )
    
    # Generate data
    np.random.seed(42)
    control_data = np.random.binomial(1, control_rate, sample_size)
    treatment_data = np.random.binomial(1, treatment_rate, sample_size)
    
    # Initialize analyzer
    analyzer = ABTestAnalyzer()
    analyzer.load_data(control_data, treatment_data)
    
    # Display results
    st.header("Test Results")
    report = analyzer.generate_report()
    
    # Create two columns for metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Control Conversion Rate",
            report["Control Conversion Rate"],
            delta=None
        )
        st.metric(
            "Treatment Conversion Rate",
            report["Treatment Conversion Rate"],
            delta=report["Relative Improvement"]
        )
        st.metric(
            "Sample Size (Control)",
            report["Sample Size (Control)"]
        )
        st.metric(
            "Sample Size (Treatment)",
            report["Sample Size (Treatment)"]
        )
    
    with col2:
        st.metric(
            "Chi-square Test p-value",
            report["Chi-square Test p-value"]
        )
        st.metric(
            "Z-test p-value",
            report["Z-test p-value"]
        )
        st.metric(
            "Effect Size (Cohen's h)",
            report["Effect Size (Cohen's h)"]
        )
        st.metric(
            "Statistical Power",
            report["Statistical Power"]
        )
    
    # Display visualizations
    st.header("Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Conversion Rates")
        st.pyplot(analyzer.plot_conversion_rates())
    
    with col2:
        st.subheader("Distribution of Conversions")
        st.pyplot(analyzer.plot_distribution())
    
    # Display interpretation
    st.header("Interpretation")
    
    if float(report["Z-test p-value"]) < 0.05:
        st.success("The test results are statistically significant!")
        if float(report["Relative Improvement"].strip("%")) > 0:
            st.write(
                f"The treatment group shows a {report['Relative Improvement']} "
                "improvement over the control group."
            )
        else:
            st.write(
                f"The treatment group shows a {report['Relative Improvement']} "
                "decrease compared to the control group."
            )
    else:
        st.warning("The test results are not statistically significant.")
        st.write(
            "We cannot conclude that there is a meaningful difference between "
            "the control and treatment groups."
        )
    
    # Sample size calculator
    st.header("Sample Size Calculator")
    st.write(
        "Calculate the required sample size for your desired effect size and power."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        desired_effect = st.slider(
            "Desired Effect Size (Cohen's h)",
            min_value=0.1,
            max_value=1.0,
            value=0.2,
            step=0.1
        )
    
    with col2:
        desired_power = st.slider(
            "Desired Statistical Power",
            min_value=0.5,
            max_value=0.99,
            value=0.8,
            step=0.05
        )
    
    # Calculate required sample size
    power_analysis = TTestPower()
    required_sample_size = power_analysis.solve_power(
        effect_size=desired_effect,
        power=desired_power,
        alpha=0.05
    )
    
    st.metric(
        "Required Sample Size per Group",
        f"{int(required_sample_size):,}"
    )

if __name__ == "__main__":
    main() 