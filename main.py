import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.decision import process_ab_test_results

if __name__ == "__main__":
    data_path = "data/synthetic/ab_test_fintech_data.csv"
    report_path = "output/reports/report.txt"
    statistical_report_path = "output/reports/statistical_report.txt"
    plot_path = "output/plots/"
    output_pdf_path = "output/reports/combined_report.pdf"

    process_ab_test_results(data_path, report_path, 
                            statistical_report_path, plot_path, 
                            output_pdf_path)