# File: combine_report_files.py
# Owner: silicastormsiam
# Purpose: Combine rats_data_report.txt, parsed_jobs_report.txt, parse_errors_report.txt, and error_recovery_report.txt into a single combined_reports.txt for the R.A.T.S. project to simplify error analysis in Notepad++.
# Version Control: 1.0
# Change Log:
# - 2025-08-07: Version 1.0 - Initial creation to merge report files into logs/combined_reports.txt.
import os
import logging

# Set up logging
LOG_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_DIR, 'combine_reports.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

def combine_report_files():
    try:
        report_files = [
            'rats_data_report.txt',
            'parsed_jobs_report.txt',
            'parse_errors_report.txt',
            'error_recovery_report.txt'
        ]
        output_file = os.path.join(LOG_DIR, 'combined_reports.txt')
        combined_content = []
        
        for file in report_files:
            file_path = os.path.join(LOG_DIR, file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    combined_content.append(f"--- Report File: {file} ---\n{content}\n")
                logging.info(f"Read content from {file}")
            else:
                logging.warning(f"Report file {file} not found.")
                combined_content.append(f"--- Report File: {file} ---\nFile not found.\n")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(combined_content))
        logging.info(f"Combined {len(combined_content)} report files into {output_file}")
        print(f"Combined {len(combined_content)} report files into {output_file}")
    except Exception as e:
        logging.error(f"Error combining report files: {e}")
        print(f"Error combining report files. Check {LOG_DIR}/combine_reports.log")

if __name__ == "__main__":
    combine_report_files()