# File: combine_glassdoor_emails.py
# Owner: silicastormsiam
# Purpose: Combine multiple Glassdoor email dump files into a single glassdoor_email_1.txt for the R.A.T.S. project, preserving all content with separators and deleting original files to streamline processing.
# Version Control: 1.0
# Change Log:
# - 2025-08-07: Version 1.0 - Initial creation to merge glassdoor_email_1.txt, glassdoor_email_2.txt, glassdoor_email_3.txt, and glassdoor_email_4.txt into glassdoor_email_1.txt.
import os
import logging

# Set up logging
LOG_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_DIR, 'combine_glassdoor.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

def combine_glassdoor_emails():
    try:
        email_dumps_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'data', 'email_dumps')
        output_file = os.path.join(email_dumps_dir, 'glassdoor_email_1.txt')
        glassdoor_files = [f for f in os.listdir(email_dumps_dir) if f.startswith('glassdoor_email_') and f.endswith('.txt')]
        
        if not glassdoor_files:
            logging.warning("No Glassdoor email dump files found.")
            print("No Glassdoor email dump files found.")
            return
        
        combined_content = []
        for file in glassdoor_files:
            file_path = os.path.join(email_dumps_dir, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                combined_content.append(f"--- {file} ---\n{content}\n")
            logging.info(f"Read content from {file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(combined_content))
        logging.info(f"Combined {len(glassdoor_files)} Glassdoor files into {output_file}")
        print(f"Combined {len(glassdoor_files)} Glassdoor files into {output_file}")
        
        # Delete original files (except glassdoor_email_1.txt)
        for file in glassdoor_files:
            if file != 'glassdoor_email_1.txt':
                os.remove(os.path.join(email_dumps_dir, file))
                logging.info(f"Deleted {file}")
                print(f"Deleted {file}")
    except Exception as e:
        logging.error(f"Error combining Glassdoor emails: {e}")
        print(f"Error combining Glassdoor emails. Check {LOG_DIR}/combine_glassdoor.log")

if __name__ == "__main__":
    combine_glassdoor_emails()