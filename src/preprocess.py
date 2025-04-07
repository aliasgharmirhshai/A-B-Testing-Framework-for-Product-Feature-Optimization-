import pandas as pd
import numpy as np

def compute_conversion_metrics(df):
    """
    Computes conversion rates and 95% confidence intervals for each group.
    
    Args:
        df (pd.DataFrame): DataFrame with 'group' and 'converted' columns.
    Returns:
        pd.DataFrame: DataFrame with 'group', 'conversion_rate', 'conversion_CI_lower', 'conversion_CI_upper'.
    """
    metrics = df.groupby('group')['converted'].agg(['mean', 'count']).reset_index()
    metrics.rename(columns={'mean': 'conversion_rate', 'count': 'total'}, inplace=True)
    # Calculate standard error
    metrics['se'] = np.sqrt(metrics['conversion_rate'] * (1 - metrics['conversion_rate']) / metrics['total'])
    # Calculate 95% CI
    metrics['conversion_CI_lower'] = metrics['conversion_rate'] - 1.96 * metrics['se']
    metrics['conversion_CI_upper'] = metrics['conversion_rate'] + 1.96 * metrics['se']
    # Ensure CI bounds are within [0,1]
    metrics['conversion_CI_lower'] = metrics['conversion_CI_lower'].clip(lower=0)
    metrics['conversion_CI_upper'] = metrics['conversion_CI_upper'].clip(upper=1)
    return metrics[['group', 'conversion_rate', 'conversion_CI_lower', 'conversion_CI_upper']]

def prepare_conversion_metrics(metrics):
    """
    Prepares metrics for plotting by scaling to percentages.
    
    Args:
        metrics (pd.DataFrame): DataFrame with conversion metrics.
    Returns:
        pd.DataFrame: Scaled metrics.
    """
    metrics = metrics.copy()
    metrics['conversion_rate'] *= 100
    metrics['conversion_CI_lower'] *= 100
    metrics['conversion_CI_upper'] *= 100
    return metrics

def prepare_daily_conversion(df):
    """
    Prepares data for daily conversion plotting.
    
    Args:
        df (pd.DataFrame): DataFrame with 'timestamp', 'group', and 'converted' columns.
    Returns:
        pd.DataFrame: Daily conversion rates.
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_conversion = df.groupby(['date', 'group'])['converted'].mean().reset_index()
    daily_conversion['converted'] *= 100
    return daily_conversion

def prepare_cumulative_conversion(df):
    """
    Prepares data for cumulative conversion plotting.
    
    Args:
        df (pd.DataFrame): DataFrame with 'timestamp', 'group', and 'converted' columns.
    Returns:
        pd.DataFrame: Cumulative conversion rates.
    """
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_sorted = df.sort_values('timestamp')
    df_sorted['cumulative_converted'] = df_sorted.groupby('group')['converted'].cumsum()
    df_sorted['cumulative_total'] = df_sorted.groupby('group').cumcount() + 1
    df_sorted['cumulative_rate'] = (df_sorted['cumulative_converted'] / df_sorted['cumulative_total']) * 100
    return df_sorted

def prepare_funnel_data(df):
    """
    Prepares data for funnel plotting.
    
    Args:
        df (pd.DataFrame): DataFrame with 'group', 'views', 'clicks', and 'converted' columns.
    Returns:
        pd.DataFrame: Funnel data in long format.
    """
    funnel = df.groupby('group')[['views', 'clicks', 'converted']].sum().reset_index()
    funnel_data = funnel.melt(id_vars='group', var_name='Stage', value_name='Count')
    return funnel_data