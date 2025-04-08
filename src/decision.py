import os
from google import genai
from google.genai import types
import pandas as pd
from stats_engine import summarize_results
from dotenv import load_dotenv

# Load API key from config.env
load_dotenv("../config.env")
API_KEY = os.getenv("GEMINI_API_KEY")

def send_to_gemini_for_report(payload, output_path):
    """
    Sends the A/B test results to the Gemini API and requests a detailed report.
    Saves the generated report to the specified output path.
    """
    client = genai.Client(api_key=API_KEY)

    # Define the model and content
    model = "gemini-2.0-flash"
    prompt = f"""
        You are a data analyst. Please generate a plain text detailed A/B testing report based on the following data. 
        Do not use markdown formatting; output plain text only.
        The report should help in decision-making by providing a clear, strong preliminary analysis of the results and offering 
        recommendations on next steps.

        Data provided:

        Metrics: {payload['metrics']}
        T-Test Results:
        Test Statistic: {payload['t_test']['t_stat']}
        P-Value: {payload['t_test']['p_value']}
        Is Significant: {payload['t_test']['is_significant']}
        
        Chi-Squared Test Results:
        Test Statistic: {payload['chi_squared']['chi2_stat']}
        P-Value: {payload['chi_squared']['p_value']}
        Is Significant: {payload['chi_squared']['is_significant']}

        Effect Size:
        Cohen's d: {payload['effect_size']['effect_size']}
        Interpretation: {payload['effect_size']['interpretation']}

        Based on the above data, provide a strong preliminary analysis of the performance 
        differences between the control and test groups. Evaluate the statistical 
        significance of the results and interpret the effect size. Conclude with actionable 
        recommendations for decision-making regarding the new product feature.
    """

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]

    # Configure the content generation
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    # Send the prompt and save the response to a file
    print("Generating report...")
    report = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        report += chunk.text

    # Save the report to the specified output path
    with open(output_path, "w") as file:
        file.write(f"<html><body><pre>{report}</pre></body></html>")
    print(f"\n✅ Report saved to {output_path}")

if __name__ == "__main__":
    # Load data and summarize results
    data = pd.read_csv("../data/synthetic/ab_test_fintech_data.csv")
    results = summarize_results(data)

    # Prepare metrics for display
    metrics = results['metrics'].copy()
    metrics['conversion_rate'] = (metrics['conversion_rate'] * 100).round(1).astype(str) + '%'
    metrics['conversion_CI_lower'] = (metrics['conversion_CI_lower'] * 100).round(1).astype(str) + '%'
    metrics['conversion_CI_upper'] = (metrics['conversion_CI_upper'] * 100).round(1).astype(str) + '%'

    metrics_result = metrics[['group', 'conversion_rate', 'conversion_CI_lower', 'conversion_CI_upper']]
    t_test = results['t_test']
    chi2 = results['chi_squared']
    effect = results['effect_size']

    payload = {
        "metrics": metrics_result.to_dict(orient="records"),
        "t_test": t_test,
        "chi_squared": chi2,
        "effect_size": effect
    }

    # Output path for the report
    report_path = "../output/report/report.html"
    statisticalـreport_path = "../output/report/report.html"
    plot_path = "../output/plots/"

    # Send the payload to the Gemini API for report generation
    send_to_gemini_for_report(payload, report_path)