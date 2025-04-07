import matplotlib.pyplot as plt
import seaborn as sns
import os
from preprocess import (
    compute_conversion_metrics,
    prepare_conversion_metrics,
    prepare_daily_conversion,
    prepare_cumulative_conversion,
    prepare_funnel_data
)

def plot_conversion_rate(metrics, output_folder):
    """Plots conversion rates with confidence intervals."""
    metrics_prepared = prepare_conversion_metrics(metrics)
    groups = metrics_prepared['group']
    rates = metrics_prepared['conversion_rate']
    errors = [
        rates - metrics_prepared['conversion_CI_lower'],
        metrics_prepared['conversion_CI_upper'] - rates
    ]
    plt.figure(figsize=(6, 5))
    bars = plt.bar(groups, rates, yerr=errors, capsize=10, color=["#66c2a5", "#fc8d62"])
    plt.ylabel("Conversion Rate (%)")
    plt.title("Conversion Rate with 95% Confidence Intervals")
    plt.ylim(0, max(metrics_prepared['conversion_CI_upper']) + 5)
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1, f"{rate:.1f}%", ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'conversion_rate.png'))
    plt.close()

def plot_daily_conversion(df, output_folder):
    """Plots daily conversion rates over time."""
    daily_conversion = prepare_daily_conversion(df)
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=daily_conversion, x='date', y='converted', hue='group', marker='o')
    plt.ylabel("Daily Conversion Rate (%)")
    plt.title("Conversion Rate Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'daily_conversion.png'))
    plt.close()

def plot_cumulative_conversion(df, output_folder):
    """Plots cumulative conversion rates over time."""
    df_sorted = prepare_cumulative_conversion(df)
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df_sorted, x='timestamp', y='cumulative_rate', hue='group')
    plt.title("Cumulative Conversion Rate Over Time")
    plt.ylabel("Cumulative Conversion Rate (%)")
    plt.xlabel("Time")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'cumulative_conversion.png'))
    plt.close()

def plot_user_funnel(df, output_folder):
    """Plots user funnel from views to conversions."""
    funnel_data = prepare_funnel_data(df)
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Stage', y='Count', hue='group', data=funnel_data)
    plt.title("User Funnel: Views → Clicks → Conversions")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'user_funnel.png'))
    plt.close()

def plot_distributions(df, output_folder):
    """Plots distributions of clicks and views."""
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    sns.boxplot(x='group', y='clicks', data=df)
    plt.title("Click Distribution")
    plt.subplot(1, 2, 2)
    sns.boxplot(x='group', y='views', data=df)
    plt.title("View Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, 'distributions.png'))
    plt.close()

def generate_plots(df, output_folder):
    """
    Generates all plots and saves them to the specified folder.
    
    Args:
        df (pd.DataFrame): Main DataFrame with experiment data.
        output_folder (str): Directory to save the plots.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    metrics = compute_conversion_metrics(df)
    plot_conversion_rate(metrics, output_folder)
    plot_daily_conversion(df, output_folder)
    plot_cumulative_conversion(df, output_folder)
    plot_user_funnel(df, output_folder)
    plot_distributions(df, output_folder)