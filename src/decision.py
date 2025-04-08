import os
from google import genai
from google.genai import types
import pandas as pd
from stats_engine import summarize_results
from dotenv import load_dotenv
from visualize import generate_plots

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

def generate_statistical_report(payload, statistical_report_path):
    # Build Metrics section
    metrics_section = ""
    if "metrics" in payload:
        metrics_section += "<h3>Metrics</h3>\n"
        for idx, record in enumerate(payload["metrics"], start=1):
            metrics_section += f"<p><b>Record {idx}:</b> {record}</p>\n"
    
    # Build T-Test Section
    t_test = payload.get("t_test", {})
    t_test_section = "<h3>T-Test Results</h3>\n"
    t_test_section += f"<p>Test Statistic: {t_test.get('t_stat', 'N/A')}</p>\n"
    t_test_section += f"<p>P-Value: {t_test.get('p_value', 'N/A')}</p>\n"
    t_test_section += f"<p>Is Significant: {t_test.get('is_significant', 'N/A')}</p>\n"
    
    # Build Chi-Squared Section
    chi_squared = payload.get("chi_squared", {})
    chi_squared_section = "<h3>Chi-Squared Test Results</h3>\n"
    chi_squared_section += f"<p>Test Statistic: {chi_squared.get('chi2_stat', 'N/A')}</p>\n"
    chi_squared_section += f"<p>P-Value: {chi_squared.get('p_value', 'N/A')}</p>\n"
    chi_squared_section += f"<p>Is Significant: {chi_squared.get('is_significant', 'N/A')}</p>\n"
    
    # Build Effect Size Section
    effect_size = payload.get("effect_size", {})
    effect_size_section = "<h3>Effect Size</h3>\n"
    effect_size_section += f"<p>Cohen's d: {effect_size.get('effect_size', 'N/A')}</p>\n"
    effect_size_section += f"<p>Interpretation: {effect_size.get('interpretation', 'N/A')}</p>\n"
    
    # Build the recommendations section
    recommendations = "<h3>Analysis & Recommendations</h3>\n"
    recommendations += "<p>The report indicates the performance differences between the control and test groups. "
    recommendations += "Based on the statistical tests (T-Test and Chi-Squared) and the effect size, evaluate the significance of the differences. "
    recommendations += "If the tests are statistically significant and the effect size is meaningful, consider rolling out the new feature. "
    recommendations += "Otherwise, further analysis or iteration might be required.</p>\n"
    
    # Combine everything into an HTML template
    html_content = f"""
    <html>
      <head>
        <title>Statistical Report</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
          }}
          h1, h2, h3 {{
            color: #333;
          }}
          p {{
            margin: 5px 0;
          }}
        </style>
      </head>
      <body>
        <h1>A/B Testing Statistical Report</h1>
        <p>This report provides a detailed analysis of the A/B testing results to support decision-making.</p>
        {metrics_section}
        {t_test_section}
        {chi_squared_section}
        {effect_size_section}
        {recommendations}
      </body>
    </html>
    """
    
    # Save the HTML content to the specified file path
    with open(statistical_report_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print(f"\n✅ Statistical Report successfully saved to {statistical_report_path}")


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
    report_path = "../output/reports/report.html"
    statistical_report_path = "../output/reports/statistical_report.html"
    plot_path = "../output/plots/"

    # Send the payload to the Gemini API for report generation
    send_to_gemini_for_report(payload, report_path)
    generate_statistical_report(payload, statistical_report_path)
    generate_plots(data, plot_path)
