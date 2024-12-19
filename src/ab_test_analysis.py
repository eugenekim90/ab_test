import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.power import TTestPower
from statsmodels.stats.proportion import proportions_ztest

class ABTestAnalyzer:
    def __init__(self):
        self.control_data = None
        self.treatment_data = None
        self.alpha = 0.05  # Default significance level
        
    def load_data(self, control_data, treatment_data):
        """Load control and treatment data."""
        self.control_data = control_data
        self.treatment_data = treatment_data
        
    def calculate_conversion_rates(self):
        """Calculate conversion rates for both groups."""
        control_conversion = np.mean(self.control_data)
        treatment_conversion = np.mean(self.treatment_data)
        return control_conversion, treatment_conversion
    
    def perform_chi_square_test(self):
        """Perform chi-square test for proportions."""
        control_conversions = np.sum(self.control_data)
        treatment_conversions = np.sum(self.treatment_data)
        control_total = len(self.control_data)
        treatment_total = len(self.treatment_data)
        
        # Create contingency table
        contingency = np.array([
            [control_conversions, control_total - control_conversions],
            [treatment_conversions, treatment_total - treatment_conversions]
        ])
        
        chi2, p_value = stats.chi2_contingency(contingency)[:2]
        return chi2, p_value
    
    def perform_z_test(self):
        """Perform z-test for proportions."""
        control_conversions = np.sum(self.control_data)
        treatment_conversions = np.sum(self.treatment_data)
        control_total = len(self.control_data)
        treatment_total = len(self.treatment_data)
        
        z_stat, p_value = proportions_ztest(
            [control_conversions, treatment_conversions],
            [control_total, treatment_total]
        )
        return z_stat, p_value
    
    def calculate_effect_size(self):
        """Calculate Cohen's h for proportions."""
        control_conversion = np.mean(self.control_data)
        treatment_conversion = np.mean(self.treatment_data)
        
        # Convert proportions to angles
        control_angle = 2 * np.arcsin(np.sqrt(control_conversion))
        treatment_angle = 2 * np.arcsin(np.sqrt(treatment_conversion))
        
        # Calculate Cohen's h
        cohens_h = treatment_angle - control_angle
        return cohens_h
    
    def calculate_power(self):
        """Calculate statistical power."""
        effect_size = self.calculate_effect_size()
        sample_size = min(len(self.control_data), len(self.treatment_data))
        
        power_analysis = TTestPower()
        power = power_analysis.power(
            effect_size=effect_size,
            nobs=sample_size,
            alpha=self.alpha
        )
        return power
    
    def plot_conversion_rates(self):
        """Plot conversion rates for both groups."""
        control_conversion, treatment_conversion = self.calculate_conversion_rates()
        
        plt.figure(figsize=(10, 6))
        sns.barplot(
            x=['Control', 'Treatment'],
            y=[control_conversion, treatment_conversion]
        )
        plt.title('Conversion Rates by Group')
        plt.ylabel('Conversion Rate')
        plt.ylim(0, max(control_conversion, treatment_conversion) * 1.2)
        
        # Add percentage labels
        for i, v in enumerate([control_conversion, treatment_conversion]):
            plt.text(i, v, f'{v:.1%}', ha='center', va='bottom')
        
        return plt.gcf()
    
    def plot_distribution(self):
        """Plot distribution of conversions."""
        plt.figure(figsize=(10, 6))
        sns.kdeplot(data=self.control_data, label='Control', fill=True)
        sns.kdeplot(data=self.treatment_data, label='Treatment', fill=True)
        plt.title('Distribution of Conversions')
        plt.xlabel('Conversion')
        plt.ylabel('Density')
        plt.legend()
        return plt.gcf()
    
    def generate_report(self):
        """Generate a comprehensive report of the A/B test results."""
        control_conversion, treatment_conversion = self.calculate_conversion_rates()
        chi2, chi2_p_value = self.perform_chi_square_test()
        z_stat, z_p_value = self.perform_z_test()
        effect_size = self.calculate_effect_size()
        power = self.calculate_power()
        
        report = {
            'Control Conversion Rate': f'{control_conversion:.1%}',
            'Treatment Conversion Rate': f'{treatment_conversion:.1%}',
            'Relative Improvement': f'{(treatment_conversion - control_conversion) / control_conversion:.1%}',
            'Chi-square Test p-value': f'{chi2_p_value:.4f}',
            'Z-test p-value': f'{z_p_value:.4f}',
            'Effect Size (Cohen\'s h)': f'{effect_size:.3f}',
            'Statistical Power': f'{power:.1%}',
            'Sample Size (Control)': len(self.control_data),
            'Sample Size (Treatment)': len(self.treatment_data)
        }
        
        return report 