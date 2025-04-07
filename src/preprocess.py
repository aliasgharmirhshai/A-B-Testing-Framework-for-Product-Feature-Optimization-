import pandas as pd

def prepare_conversion_metrics(metrics):
    """
    Prepares metrics DataFrame for conversion rate plotting by scaling percentages.
    
    Args:
        metrics (pd.DataFrame): DataFrame with 'conversion_rate', 'conversion_CI_lower', 
                                and 'conversion_CI_upper' columns.
    Returns:
        pd.DataFrame: Preprocessed DataFrame with scaled values.
    """
    metrics = metrics.copy()
    metrics['conversion_rate'] *= 100
    metrics['conversion_CI_lower'] *= 100
    metrics['conversion_CI_upper'] *= 100
    return metrics

def prepare_daily_conversion(df):
    """
    Prepares DataFrame for daily conversion plotting by extracting dates and calculating rates.
    
    Args:
        df (pd.DataFrame): DataFrame with 'timestamp', 'group', and 'converted' columns.
    Returns:
        pd.DataFrame: Preprocessed DataFrame with daily conversion rates.
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_conversion = df.groupby(['date', 'group'])['converted'].mean().reset_index()
    daily_conversion['converted'] *= 100
    return daily_conversion

def prepare_cumulative_conversion(df):
    """
    Prepares DataFrame for cumulative conversion plotting by calculating cumulative rates.
    
    Args:
        df (pd.DataFrame): DataFrame with 'timestamp', 'group', and 'converted' columns.
    Returns:
        pd.DataFrame: Preprocessed DataFrame with cumulative conversion rates.
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
    Prepares DataFrame for user funnel plotting by aggregating and reshaping data.
    
    Args:
        df (pd.DataFrame): DataFrame with 'group', 'views', 'clicks', and 'converted' columns.
    Returns:
        pd.DataFrame: Preprocessed DataFrame in long format for funnel visualization.
    """
    funnel = df.groupby('group')[['views', 'clicks', 'converted']].sum().reset_index()
    funnel_data = funnel.melt(id_vars='group', var_name='Stage', value_name='Count')
    return funnel_data