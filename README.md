# A/B Testing Analysis Platform

A simple and efficient platform for analyzing A/B test results, featuring an interactive dashboard for real-time analysis and visualization.

## Project Structure

```
ab_test_analysis/
├── src/
│   ├── ab_test_analysis.py  # Core analysis functionality
│   ├── dashboard.py         # Streamlit dashboard
│   └── generate_data.py     # Data generation utility
└── requirements.txt         # Project dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Dashboard

Launch the Streamlit dashboard:
```bash
streamlit run src/dashboard.py
```

The dashboard provides:
- Test parameter configuration
- Real-time analysis
- Statistical testing
- Visualizations
- Sample size calculator

### Key Metrics

1. **Conversion Rates**
   - Control and treatment group rates
   - Relative improvement

2. **Statistical Analysis**
   - Chi-square and Z-test p-values
   - Effect size (Cohen's h)
   - Statistical power

3. **Sample Size Calculator**
   - Calculate required sample size
   - Adjust effect size and power

## Dependencies

- numpy==1.24.3
- pandas==2.0.3
- scipy==1.10.1
- matplotlib==3.7.2
- seaborn==0.12.2
- statsmodels==0.14.0
- streamlit==1.32.0

## License

MIT License 