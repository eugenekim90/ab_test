import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_ab_test_data(
    n_users=1000,
    control_conversion_rate=0.1,
    treatment_conversion_rate=0.12,
    days=30,
    seed=42
):
    """Generate synthetic A/B test data."""
    np.random.seed(seed)
    
    # Generate user IDs and assign groups
    user_ids = np.arange(n_users * 2)
    groups = np.array(['control'] * n_users + ['treatment'] * n_users)
    
    # Generate timestamps
    start_date = datetime.now() - timedelta(days=days)
    timestamps = [
        start_date + timedelta(
            days=np.random.randint(0, days),
            hours=np.random.randint(0, 24),
            minutes=np.random.randint(0, 60)
        )
        for _ in range(n_users * 2)
    ]
    
    # Generate conversions
    conversions = [
        np.random.binomial(1, control_conversion_rate) if group == 'control'
        else np.random.binomial(1, treatment_conversion_rate)
        for group in groups
    ]
    
    # Create DataFrame
    data = pd.DataFrame({
        'user_id': user_ids,
        'group': groups,
        'timestamp': timestamps,
        'conversion': conversions
    })
    
    return data

def save_data(data, filename='ab_test_data.csv'):
    """Save the generated data to a CSV file."""
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == '__main__':
    # Generate and save sample data
    data = generate_ab_test_data()
    save_data(data)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("-----------------")
    print(f"Total users: {len(data)}")
    print(f"Control group size: {len(data[data['group'] == 'control'])}")
    print(f"Treatment group size: {len(data[data['group'] == 'treatment'])}")
    print("\nConversion rates:")
    print(data.groupby('group')['conversion'].mean()) 