# File: analyze_errors.py
# Owner: silicastormsiam
# Purpose: Analyze parse_errors_report.txt, rats_data.json, parsed_jobs_output.txt, parsed_jobs_output.html, and combined_reports.txt to identify errors and suggest recovery actions for the R.A.T.S. project, with focus on HTML rendering stability, Google Careers data discrepancies, dropdown functionality, and large file handling.
# Version Control: 1.18
# Change Log:
# - 2025-08-07: Version 1.14 - Enhanced diagnostics for JavaScript syntax and dropdown functionality; refined recovery suggestions for non-English skips and Google Careers parsing; retained large file handling and f-string diagnostics.
# - 2025-08-07: Version 1.15 - Added diagnostics for processing failures and file access errors; enhanced Google Careers parsing checks; added checks for redundant File dropdown and Remote filter; retained JavaScript, dropdown, and non-English skip diagnostics.
# - 2025-08-07: Version 1.16 - Added diagnostics for 'pos' keyword errors and duplicate entries; enhanced remote field checks; improved deduplication checks; retained Google Careers parsing and dropdown diagnostics.
# - 2025-08-07: Version 1.17 - Enhanced diagnostics for limited data and invalid job positions; improved remote field type checks; refined non-English skip and location validation; retained deduplication and parsing diagnostics.
# - 2025-08-07: Version 1.18 - Added diagnostics for JavaScript rendering issues and IndentationError; enhanced remote field and parsing diagnostics; retained non-English skip and location validation.
import os
import re
import json
from datetime import datetime
import logging

# Set up logging
LOG_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_DIR, 'error_recovery.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

def analyze_errors():
    try:
        report_path = os.path.join(LOG_DIR, 'parse_errors_report.txt')
        json_path = os.path.join(os.path.dirname(LOG_DIR), 'data', 'rats_data.json')
        txt_path = os.path.join(os.path.dirname(LOG_DIR), 'data', 'parsed_jobs_output.txt')
        html_path = os.path.join(os.path.dirname(LOG_DIR), 'data', 'parsed_jobs_output.html')
        combined_reports_path = os.path.join(LOG_DIR, 'combined_reports.txt')
        output_path = os.path.join(LOG_DIR, 'error_recovery_report.txt')
        errors = []
        recovery_suggestions = []
        seen_keys = set()

        # Analyze combined_reports.txt
        if os.path.exists(combined_reports_path):
            file_size = os.path.getsize(combined_reports_path) / (1024 * 1024)  # Size in MB
            if file_size > 10:
                recovery_suggestions.append(f"WARNING: combined_reports.txt is large ({file_size:.2f} MB).\n  Recovery: Split file into sections for analysis or upload directly to Grok interface.")
            with open(combined_reports_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                sections = re.split(r'--- Report File: .+? ---', content)
                for section in sections[1:]:
                    section = section.strip()
                    if not section:
                        continue
                    if re.search(r'ERROR|WARNING', section):
                        errors.append(section[:100] + '...')
                        if 'JSON initialization error' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: JSON initialization error\n  Recovery: Verify data/rats_data.json exists and is valid JSON. Check file permissions and OneDrive sync status.")
                        elif 'JSON serialization error' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: JSON serialization error\n  Recovery: Validate rats_data.json for syntax errors (e.g., unescaped characters, missing commas). Ensure data entries are properly formatted.")
                        elif 'Error saving to JSON' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: Error saving to JSON\n  Recovery: Ensure write permissions for data/rats_data.json. Check for OneDrive file locking.")
                        elif 'Error generating output files' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: Error generating output files\n  Recovery: Validate JSON data in rats_data.json. Check write permissions for output files. Verify HTML rendering in parsed_jobs_output.html.")
                        elif 'No source identified' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: No source identified\n  Recovery: Review email dump content for missing copyright footer or sender email. Update SOURCES/SENDER_PATTERNS in process_email_dumps.py.")
                        elif 'Error parsing' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: Error parsing\n  Recovery: Inspect email dump for malformed content. Adjust regex patterns in parse_email function.")
                        elif 'No job postings identified' in section and 'GoogleCareers' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: No job postings for GoogleCareers\n  Recovery: Review GoogleCareers email dump for job posting format. Update position_pattern, location_pattern, and qualifications_pattern in parse_email function.")
                        elif 'Non-English position skipped' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: Non-English position skipped\n  Recovery: Review skipped lines for valid job titles with special characters (e.g., 'MarTech'). Adjust English-only filter in parse_email to allow valid titles.")
                        elif 'unterminated string literal' in section or 'f-string' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: Syntax error in f-string\n  Recovery: Check HTML output section in process_email_dumps.py for unclosed f-string literals or improper escaping.")
                        elif 'Failed to parse job data' in section or 'Failed to process job data' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: JavaScript error\n  Recovery: Validate embedded JSON and JavaScript syntax in generate_output function of process_email_dumps.py.")
                        elif 'Error processing' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: Error processing file\n  Recovery: Check file access permissions for email dumps in data/email_dumps/. Verify parse_email function for robust error handling.")
                        elif 'pos' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: 'pos' keyword error\n  Recovery: Remove invalid 'pos' and 'endpos' arguments from re.search in parse_email function.")
                        elif 'IndentationError' in section:
                            recovery_suggestions.append(f"Found in combined_reports.txt: IndentationError\n  Recovery: Check process_email_dumps.py for incorrect indentation in HTML output block.")
                        else:
                            recovery_suggestions.append(f"Found in combined_reports.txt: {section[:100]}...\n  Recovery: Manual review required. Check email dump content and script logic.")
        else:
            recovery_suggestions.append("WARNING: combined_reports.txt not found.\n  Recovery: Run combine_report_files.py to generate the combined report.")

        # Analyze parse_errors_report.txt
        if os.path.exists(report_path):
            with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                for line in lines:
                    if re.search(r'ERROR|WARNING', line):
                        errors.append(line.strip())
                        if 'JSON initialization error' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Verify data/rats_data.json exists and is valid JSON. Check file permissions and OneDrive sync status.")
                        elif 'JSON serialization error' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Validate rats_data.json for syntax errors (e.g., unescaped characters, missing commas). Ensure data entries are properly formatted.")
                        elif 'Error saving to JSON' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Ensure write permissions for data/rats_data.json. Check for OneDrive file locking.")
                        elif 'Error generating output files' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Validate JSON data in rats_data.json. Check write permissions for output files. Verify HTML rendering in parsed_jobs_output.html.")
                        elif 'No source identified' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Review email dump content for missing copyright footer or sender email. Update SOURCES/SENDER_PATTERNS in process_email_dumps.py.")
                        elif 'Error parsing' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Inspect email dump for malformed content. Adjust regex patterns in parse_email function.")
                        elif 'No job postings identified' in line and 'GoogleCareers' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Review GoogleCareers email dump for job posting format. Update position_pattern, location_pattern, and qualifications_pattern in parse_email function.")
                        elif 'Non-English position skipped' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Review skipped lines for valid job titles with special characters (e.g., 'MarTech'). Adjust English-only filter in parse_email to allow valid titles.")
                        elif 'unterminated string literal' in line or 'f-string' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Check HTML output section in process_email_dumps.py for unclosed f-string literals or improper escaping.")
                        elif 'Failed to parse job data' in line or 'Failed to process job data' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Validate embedded JSON and JavaScript syntax in generate_output function of process_email_dumps.py.")
                        elif 'Error processing' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Check file access permissions for email dumps in data/email_dumps/. Verify parse_email function for robust error handling.")
                        elif 'IndentationError' in line:
                            recovery_suggestions.append(f"{line}\n  Recovery: Check process_email_dumps.py for incorrect indentation in HTML output block.")
                        else:
                            recovery_suggestions.append(f"{line}\n  Recovery: Manual review required. Check email dump content and script logic.")
        else:
            recovery_suggestions.append("WARNING: parse_errors_report.txt not found.\n  Recovery: Run process_email_dumps.py to generate the report.")

        # Analyze rats_data.json
        json_data = []
        json_entry_count = 0
        google_careers_count = 0
        glassdoor_count = 0
        seen_keys = set()
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                if not json_data:
                    recovery_suggestions.append("ERROR: rats_data.json is empty.\n  Recovery: Check email dump processing in process_email_dumps.py. Ensure email_dumps/ contains valid .txt files.")
                for entry in json_data:
                    json_entry_count += 1
                    if not isinstance(entry, dict):
                        recovery_suggestions.append(f"ERROR: Invalid entry in rats_data.json: {entry}\n  Recovery: Ensure all entries are valid dictionaries.")
                        continue
                    required_fields = ['filename', 'source', 'sender', 'job_position', 'location', 'minimum_qualifications', 'remote']
                    for field in required_fields:
                        if field not in entry:
                            recovery_suggestions.append(f"ERROR: Missing field {field} in rats_data.json for {entry.get('filename', 'unknown file')}\n  Recovery: Review email dump {entry.get('filename', 'unknown file')} for missing data. Update parse_email function.")
                        elif field == 'remote' and not isinstance(entry[field], bool):
                            recovery_suggestions.append(f"ERROR: Invalid 'remote' field type in rats_data.json for {entry.get('filename', 'unknown file')}: {entry[field]}\n  Recovery: Ensure parse_email function sets 'remote' as boolean.")
                        elif entry[field] == 'Unknown':
                            recovery_suggestions.append(f"WARNING: 'Unknown' {field} in rats_data.json for {entry.get('filename', 'unknown file')}\n  Recovery: Review email dump {entry.get('filename', 'unknown file')} for missing data. Update parse_email function.")
                        elif field == 'job_position' and re.search(r'[^\x00-\x7F]', entry[field]):
                            recovery_suggestions.append(f"WARNING: Non-English job position in rats_data.json for {entry.get('filename', 'unknown file')}: {entry[field]}\n  Recovery: Enhance English-only filter in parse_email function.")
                        elif field == 'location' and re.search(r'\d{1,2}:\d{2}\s*(?:AM|PM)', entry[field], re.IGNORECASE):
                            recovery_suggestions.append(f"WARNING: Invalid location in rats_data.json for {entry.get('filename', 'unknown file')}: {entry[field]}\n  Recovery: Exclude timestamps from location parsing in parse_email function.")
                    key = (entry.get('source', ''), entry.get('job_position', ''), entry.get('location', ''), entry.get('minimum_qualifications', ''))
                    if key in seen_keys:
                        recovery_suggestions.append(f"WARNING: Duplicate entry in rats_data.json for {entry.get('filename', 'unknown file')} with source {entry.get('source', '')} and job {entry.get('job_position', '')}\n  Recovery: Review parse_email function for duplicate job posting extraction.")
                    seen_keys.add(key)
                    if entry.get('source') == 'GoogleCareers':
                        google_careers_count += 1
                    if entry.get('source') == 'Glassdoor':
                        glassdoor_count += 1
                email_dumps_dir = os.path.join(os.path.dirname(json_path), 'email_dumps')
                google_careers_files = len([f for f in os.listdir(email_dumps_dir) if 'GoogleCareers' in f])
                glassdoor_files = len([f for f in os.listdir(email_dumps_dir) if 'glassdoor_email' in f])
                if json_entry_count < 50 and (google_careers_files > 0 or glassdoor_files > 0):
                    recovery_suggestions.append(f"WARNING: Limited entries ({json_entry_count}) in rats_data.json despite available email dumps.\n  Recovery: Review parse_email function for incomplete section parsing.")
                if google_careers_count < glassdoor_count and google_careers_files >= glassdoor_files:
                    recovery_suggestions.append(f"WARNING: Fewer GoogleCareers entries ({google_careers_count}) than Glassdoor ({glassdoor_count}) in rats_data.json despite similar input volumes.\n  Recovery: Review GoogleCareers email dumps for missing job postings. Update position_pattern, location_pattern, and qualifications_pattern in parse_email function.")
                if glassdoor_count > 0 and glassdoor_files == 1:
                    logging.info("Detected combined Glassdoor file (glassdoor_email_1.txt).")
                elif glassdoor_count > 0 and glassdoor_files > 1:
                    recovery_suggestions.append("WARNING: Multiple Glassdoor files detected in email_dumps/. Run combine_glassdoor_emails.py to merge into glassdoor_email_1.txt.")
            except json.JSONDecodeError as e:
                recovery_suggestions.append(f"ERROR: Invalid JSON in rats_data.json: {e}\n  Recovery: Validate JSON syntax. Check for unescaped characters or incomplete entries.")
            except Exception as e:
                recovery_suggestions.append(f"ERROR: Failed to read rats_data.json: {e}\n  Recovery: Verify file accessibility and OneDrive sync status.")
        else:
            recovery_suggestions.append("ERROR: rats_data.json not found.\n  Recovery: Run process_email_dumps.py to generate the file.")

        # Analyze parsed_jobs_output.txt
        txt_entries = []
        seen_keys = set()
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                current_entry = {}
                for line in lines:
                    if line.startswith('Source:'):
                        if current_entry:
                            txt_entries.append(current_entry)
                        current_entry = {'source': line.split('Source: ')[1].strip()}
                    elif line.startswith('Job Position:'):
                        current_entry['job_position'] = line.split('Job Position: ')[1].strip()
                    elif line.startswith('Location:'):
                        current_entry['location'] = line.split('Location: ')[1].strip()
                    elif line.startswith('Min Requirements:'):
                        current_entry['minimum_qualifications'] = line.split('Min Requirements: ')[1].strip()
                    elif line.startswith('Remote:'):
                        current_entry['remote'] = line.split('Remote: ')[1].strip() == 'Yes'
                    if 'Unknown' in line and not line.startswith('---'):
                        recovery_suggestions.append(f"WARNING: 'Unknown' value in parsed_jobs_output.txt for {current_entry.get('source', 'unknown source')}: {line.strip()}\n  Recovery: Cross-check with rats_data.json. Update parse_email function to handle missing data.")
                    if 'job_position' in current_entry and re.search(r'[^\x00-\x7F]', current_entry['job_position']):
                        recovery_suggestions.append(f"WARNING: Non-English job position in parsed_jobs_output.txt for {current_entry.get('source', 'unknown source')}: {current_entry['job_position']}\n  Recovery: Enhance English-only filter in parse_email function.")
                    if 'location' in current_entry and re.search(r'\d{1,2}:\d{2}\s*(?:AM|PM)', current_entry['location'], re.IGNORECASE):
                        recovery_suggestions.append(f"WARNING: Invalid location in parsed_jobs_output.txt for {current_entry.get('source', 'unknown source')}: {current_entry['location']}\n  Recovery: Exclude timestamps from location parsing in parse_email function.")
                if current_entry:
                    txt_entries.append(current_entry)
                if not txt_entries:
                    recovery_suggestions.append("ERROR: No entries found in parsed_jobs_output.txt.\n  Recovery: Verify rats_data.json contains data. Check generate_output function in process_email_dumps.py.")
                for entry in txt_entries:
                    key = (entry.get('source', ''), entry.get('job_position', ''), entry.get('location', ''), entry.get('minimum_qualifications', ''))
                    if key in seen_keys:
                        recovery_suggestions.append(f"WARNING: Duplicate entry in parsed_jobs_output.txt for source {entry.get('source', '')} and job {entry.get('job_position', '')}\n  Recovery: Review parse_email function for duplicate job posting extraction.")
                    seen_keys.add(key)
                if len(txt_entries) < 50:
                    recovery_suggestions.append(f"WARNING: Limited entries ({len(txt_entries)}) in parsed_jobs_output.txt.\n  Recovery: Verify parse_email function for incomplete job posting extraction.")
        else:
            recovery_suggestions.append("ERROR: parsed_jobs_output.txt not found.\n  Recovery: Run process_email_dumps.py to generate the file.")

        # Analyze parsed_jobs_output.html
        html_entries = []
        seen_keys = set()
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                if '<div class="dropdown-content" id="sourceFilter">' not in html_content:
                    recovery_suggestions.append("ERROR: Source dropdown filter missing in parsed_jobs_output.html.\n  Recovery: Verify generate_output function in process_email_dumps.py for correct dropdown HTML.")
                if '<div class="dropdown-content" id="remoteFilter">' not in html_content:
                    recovery_suggestions.append("ERROR: Remote dropdown filter missing in parsed_jobs_output.html.\n  Recovery: Verify generate_output function in process_email_dumps.py for correct dropdown HTML.")
                if '<div class="dropdown-content" id="fileFilter">' in html_content:
                    recovery_suggestions.append("WARNING: Redundant File dropdown found in parsed_jobs_output.html.\n  Recovery: Remove File dropdown from generate_output function as only one file per source is used.")
                if 'Generated by process_email_dumps.py version 7.26' not in html_content:
                    recovery_suggestions.append("WARNING: Incorrect or missing footer note in parsed_jobs_output.html.\n  Recovery: Update footer note in generate_output function.")
                if 'Failed to parse job data' in html_content or 'Failed to process job data' in html_content:
                    recovery_suggestions.append("ERROR: JavaScript errors in parsed_jobs_output.html.\n  Recovery: Validate embedded JSON and JavaScript syntax in generate_output function of process_email_dumps.py.")
                tbody_start = html_content.find('<tbody>')
                tbody_end = html_content.find('</tbody>')
                if tbody_start != -1 and tbody_end != -1:
                    tbody_content = html_content[tbody_start + 7:tbody_end]
                    rows = tbody_content.split('<tr')
                    for row in rows[1:]:
                        cols = row.split('<td>')
                        if len(cols) >= 6:
                            entry = {
                                'source': cols[1].split('</td>')[0].strip().split(' (')[0],
                                'job_position': cols[2].split('</td>')[0].strip(),
                                'location': cols[3].split('</td>')[0].strip(),
                                'minimum_qualifications': cols[4].split('</td>')[0].replace('<br>', '\n').strip(),
                                'remote': cols[5].split('</td>')[0].strip() == 'Yes'
                            }
                            html_entries.append(entry)
                            key = (entry['source'], entry['job_position'], entry['location'], entry['minimum_qualifications'])
                            if key in seen_keys:
                                recovery_suggestions.append(f"WARNING: Duplicate entry in parsed_jobs_output.html for source {entry['source']} and job {entry['job_position']}\n  Recovery: Review parse_email function for duplicate job posting extraction.")
                            seen_keys.add(key)
                if not html_entries:
                    recovery_suggestions.append("ERROR: No entries found in parsed_jobs_output.html.\n  Recovery: Verify rats_data.json contains data. Check generate_output function for HTML table generation.")
                else:
                    if len(html_entries) < len(txt_entries):
                        recovery_suggestions.append(f"WARNING: Fewer entries ({len(html_entries)}) in parsed_jobs_output.html than in parsed_jobs_output.txt ({len(txt_entries)}).\n  Recovery: Verify generate_output function for complete HTML table generation.")
                    for json_entry in json_data:
                        if 'source' in json_entry:
                            matching_html = [e for e in html_entries if e['source'] == json_entry['source'] and e['job_position'] == json_entry['job_position']]
                            if not matching_html:
                                recovery_suggestions.append(f"WARNING: Source {json_entry['source']} with job {json_entry['job_position']} in rats_data.json not found in parsed_jobs_output.html.\n  Recovery: Verify static table generation in process_email_dumps.py.")
                            else:
                                for field in ['source', 'job_position', 'location', 'minimum_qualifications', 'remote']:
                                    if field in json_entry and json_entry[field] != matching_html[0][field]:
                                        recovery_suggestions.append(f"WARNING: Mismatch in {field} for {json_entry['source']} with job {json_entry['job_position']} between rats_data.json and parsed_jobs_output.html.\n  Recovery: Verify data consistency in generate_output function.")
                    if len(html_entries) < 50:
                        recovery_suggestions.append(f"WARNING: Limited entries ({len(html_entries)}) in parsed_jobs_output.html.\n  Recovery: Verify parse_email and generate_output functions for complete data processing.")
                    google_careers_html = [e for e in html_entries if 'GoogleCareers' in e['source']]
                    if len(google_careers_html) < google_careers_count:
                        recovery_suggestions.append(f"WARNING: Fewer GoogleCareers entries ({len(google_careers_html)}) in parsed_jobs_output.html than in rats_data.json ({google_careers_count}).\n  Recovery: Verify HTML table generation in process_email_dumps.py.")
        else:
            recovery_suggestions.append("ERROR: parsed_jobs_output.html not found.\n  Recovery: Run process_email_dumps.py to generate the file.")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("R.A.T.S. Error Recovery Report\n")
            f.write("=============================\n\n")
            if recovery_suggestions:
                f.write("Detected Errors and Recovery Suggestions:\n")
                f.write("\n".join(recovery_suggestions))
            else:
                f.write("No errors or warnings detected.\n")
        
        logging.info(f"Generated error recovery report at {output_path}")
        print(f"Error recovery report generated at {output_path}")
    except Exception as e:
        logging.error(f"Error analyzing errors: {e}")
        print(f"Error during analysis. Check {LOG_DIR}/error_recovery.log")

if __name__ == "__main__":
    analyze_errors()