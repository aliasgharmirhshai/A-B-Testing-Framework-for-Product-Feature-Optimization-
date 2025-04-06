import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
n_users = 1000
conversion_rate_control = 0.12
conversion_rate_test = 0.16

# Simulate users
user_ids = np.arange(1, n_users + 1)
groups = np.random.choice(['control', 'test'], size=n_users)

# Assign conversions based on group
conversions = []
for group in groups:
    if group == 'control':
        converted = np.random.binomial(1, conversion_rate_control)
    else:
        converted = np.random.binomial(1, conversion_rate_test)
    conversions.append(converted)

# Create DataFrame
df = pd.DataFrame({
    'user_id': user_ids,
    'group': groups,
    'converted': conversions
})

# Optional: Add timestamps and other behavior metrics
df['timestamp'] = pd.date_range(start='2025-01-01', periods=n_users, freq='T')
df['clicks'] = np.random.poisson(lam=3 if df['group'][0] == 'control' else 4, size=n_users)
df['views'] = df['clicks'] + np.random.randint(0, 3, size=n_users)

# Export to CSV
df.to_csv('ab_test_fintech_data.csv', index=False)

print("✅ Dataset generated and saved as 'ab_test_fintech_data.csv'")
