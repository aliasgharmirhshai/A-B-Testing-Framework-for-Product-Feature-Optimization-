import pandas as pd
import scipy.stats as stats
import numpy as np

def compute_confidence_interval(conversions, total, confidence=0.95):
    """Returns lower and upper bound of the confidence interval"""
    if total == 0:
        return (0, 0)
    p = conversions / total
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    margin = z * np.sqrt(p * (1 - p) / total)
    return (p - margin, p + margin)


def calculate_metrics(df):
    groups = df.groupby('group').agg(
        total_users=('user_id', 'count'),
        total_converted=('converted', 'sum'),
        conversion_rate=('converted', 'mean'),
        avg_clicks=('clicks', 'mean'),
        avg_views=('views', 'mean')
    ).reset_index()

    lower_bounds = []
    upper_bounds = []

    for _, row in groups.iterrows():
        lower, upper = compute_confidence_interval(
            row['total_converted'], row['total_users']
        )
        lower_bounds.append(lower)
        upper_bounds.append(upper)

    groups['conversion_CI_lower'] = lower_bounds
    groups['conversion_CI_upper'] = upper_bounds

    return groups


def run_chi_squared_test(df):
    contingency = pd.crosstab(df['group'], df['converted'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    return {
        'test': 'Chi-Squared',
        'chi2_stat': chi2,
        'p_value': p,
        'is_significant': p < 0.05
    }


def run_chi_squared_test(df):
    # Create contingency table
    contingency = pd.crosstab(df['group'], df['converted'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    return {
        'test': 'Chi-Squared',
        'chi2_stat': chi2,
        'p_value': p,
        'is_significant': p < 0.05
    }


def run_t_test(df):
    control = df[df['group'] == 'control']['converted']
    test = df[df['group'] == 'test']['converted']
    t_stat, p = stats.ttest_ind(control, test, equal_var=False)
    return {
        'test': 'T-Test',
        't_stat': t_stat,
        'p_value': p,
        'is_significant': p < 0.05
    }


def calculate_effect_size(df):
    control = df[df['group'] == 'control']['converted']
    test = df[df['group'] == 'test']['converted']
    diff = test.mean() - control.mean()
    pooled_std = np.sqrt((control.var() + test.var()) / 2)
    cohen_d = diff / pooled_std if pooled_std > 0 else 0
    return {
        'effect_size': cohen_d,
        'interpretation': interpret_effect_size(cohen_d)
    }


def interpret_effect_size(d):
    if abs(d) < 0.2:
        return 'Small'
    elif abs(d) < 0.5:
        return 'Medium'
    else:
        return 'Large'


def summarize_results(df):
    metrics = calculate_metrics(df)
    t_test_result = run_t_test(df)
    chi2_result = run_chi_squared_test(df)
    effect = calculate_effect_size(df)

    return {
        'metrics': metrics,
        't_test': t_test_result,
        'chi_squared': chi2_result,
        'effect_size': effect
    }

