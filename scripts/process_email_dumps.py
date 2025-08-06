# File: process_email_dumps.py
# Owner: silicastormsiam
# Purpose: Process email dumps for R.A.T.S. project, including source identification, parsing, and storage in JSON for job alert management, prioritizing English job titles and Remote positions, with minimal console output, robust logging limited to data errors per run, and user-friendly output files (txt/html) with 15-line readability for txt.
# Version Control: 7.1
# Change Log:
# - 2025-08-06: Version 6.7 - Limited parsed_jobs_output.txt to 15 lines; restricted parse_errors.log to data errors; retained English-only title prioritization, Remote prioritization, minimal console output; ensured metadata compliance.
# - 2025-08-06: Version 6.8 - Restricted change log to five entries; retained 15-line output limit, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
# - 2025-08-06: Version 6.9 - Fixed syntax error by removing Markdown code blocks; retained change log restriction, 15-line output limit, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
# - 2025-08-06: Version 7.0 - Fixed 'remote' key error in generate_output; retained change log restriction, 15-line output limit, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
# - 2025-08-06: Version 7.1 - Added parsed_jobs_output.html for browser-friendly output; fixed 'remote' key error; retained 15-line txt output limit, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
import os
import re
import json
from datetime import datetime
import logging

# Set up logging to file (clear previous log to limit to current run)
LOG_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_DIR, 'parse_errors.log'), level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

# Define paths (absolute for robustness)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EMAIL_DUMPS_DIR = os.path.join(PROJECT_ROOT, 'data', 'email_dumps')
JSON_PATH = os.path.join(PROJECT_ROOT, 'data', 'rats_data.json')
TXT_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'parsed_jobs_output.txt')
HTML_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'parsed_jobs_output.html')

# Source identification patterns (copyright footers)
SOURCES = {
    "Glassdoor": r"Copyright.*Glassdoor LLC",
    "LinkedIn": r"Copyright.*LinkedIn|LinkedIn Corporation",
    "Indeed": r"Copyright.*Indeed",
    "GoogleCareers": r"Google is proud to be an equal opportunity|careers-noreply@google.com"
}

# Sender email patterns for fallback identification
SENDER_PATTERNS = {
    "GoogleCareers": r"careers-noreply@google.com",
    "LinkedIn": r"jobs-noreply@linkedin.com|jobs-list@linkedin.com|jobalerts-noreply@linkedin.com",
    "Glassdoor": r"no-reply@glassdoor.com|jobs@glassdoor.com|andrewjohnholland@gmail.com",
    "Indeed": r"alert@indeed.com"
}

# Initialize JSON storage
def init_json():
    try:
        if not os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump([], f)
            logging.warning(f"Created {JSON_PATH}")
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.warning(f"Initialized JSON storage at {JSON_PATH}")
        return data
    except Exception as e:
        logging.error(f"JSON initialization error: {e}")
        raise

# Save to JSON (append without overwriting)
def save_to_json(data, entry):
    try:
        data.append(entry)
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logging.warning(f"Saved entry for {entry['filename']} to {JSON_PATH}")
    except Exception as e:
        logging.error(f"Error saving to JSON for {entry['filename']}: {e}")
        raise

# Generate user-friendly output files (txt and html, txt limited to 15 lines)
def generate_output(data):
    try:
        # Text output (limited to 15 lines)
        with open(TXT_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write("Parsed Job Data for R.A.T.S. Project\n")
            f.write("====================================\n")
            # Limit to first two entries to fit within 15 lines
            for entry in data[:2]:
                f.write(f"\nFile: {entry['filename']}\n")
                f.write(f"Source: {entry['source']} (Email: {entry['sender']})\n")
                f.write(f"Job Position: {entry['job_position']}\n")
                f.write(f"Location: {entry['location']}\n")
                f.write(f"Min Requirements: {entry['minimum_qualifications']}\n")
                f.write(f"Remote: {'Yes' if entry.get('remote', False) else 'No'}\n")
                f.write("------------------------------------\n")
        
        # HTML output (all data, styled for readability)
        with open(HTML_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>R.A.T.S. Parsed Job Data</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { text-align: center; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        tr:hover { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <h1>Parsed Job Data for R.A.T.S. Project</h1>
    <table>
        <tr>
            <th>File</th>
            <th>Source (Email)</th>
            <th>Job Position</th>
            <th>Location</th>
            <th>Minimum Requirements</th>
            <th>Remote</th>
        </tr>
""")
            for entry in data:
                f.write(f"""        <tr>
            <td>{entry['filename']}</td>
            <td>{entry['source']} ({entry['sender']})</td>
            <td>{entry['job_position']}</td>
            <td>{entry['location']}</td>
            <td>{entry['minimum_qualifications'].replace('\n', '<br>')}</td>
            <td>{'Yes' if entry.get('remote', False) else 'No'}</td>
        </tr>
""")
            f.write("""    </table>
</body>
</html>""")
        logging.warning(f"Generated output files at {TXT_OUTPUT_PATH} and {HTML_OUTPUT_PATH}")
    except Exception as e:
        logging.error(f"Error generating output files: {e}")
        raise

# Identify source
def identify_source(content, from_header):
    try:
        if from_header:
            for source, pattern in SENDER_PATTERNS.items():
                if re.search(pattern, from_header, re.IGNORECASE):
                    return source
        for source, pattern in SENDER_PATTERNS.items():
            if re.search(pattern, content, re.IGNORECASE):
                return source
        for source, pattern in SOURCES.items():
            if re.search(pattern, content, re.IGNORECASE):
                return source
        if re.search(r'\bGoogle\b', content, re.IGNORECASE):
            return "GoogleCareers"
        if re.search(r'\bLinkedIn\b', content, re.IGNORECASE):
            return "LinkedIn"
        logging.warning(f"No source identified for content. First 20 lines:\n{content[:500]}")
        return None
    except Exception as e:
        logging.error(f"Error in source identification: {e}")
        return None

# Parse email content
def parse_email(content, filename, source):
    try:
        cleaned_lines = [line for line in content.splitlines() if not re.search(r'(None selected|Skip to content|Using Gmail with screen readers|to me|Google apps|–Conversations)', line, re.IGNORECASE)]
        
        from_header = 'Unknown'
        subject_text = 'Unknown'
        date_text = 'Unknown'
        job_position = 'Unknown'
        location = 'Unknown'
        minimum_qualifications = 'Unknown'
        job_postings = []
        remote = False
        
        # Parse first 50 lines for metadata
        for i, line in enumerate(cleaned_lines[:50], 1):
            line = line.strip()
            if from_header == 'Unknown' and re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line, re.IGNORECASE):
                from_header = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line, re.IGNORECASE).group()
            if subject_text == 'Unknown' and line and not re.match(r'[\w\.-]+@[\w\.-]+\.\w+|^\w{3},\s+\w{3}\s+\d{1,2}(,\s+\d{4})?,\s+\d{1,2}:\d{2}\s*(?:AM|PM)', line, re.IGNORECASE):
                if re.search(r'job|jobs|career|careers|opportunity|opportunities|New job\(s\)|Project|Program|Assistant|alert|matching', line, re.IGNORECASE) and not re.search(r'Your job alert|has been created', line, re.IGNORECASE):
                    subject_text = line
            if date_text == 'Unknown' and re.match(r'^\w{3},\s+\w{3}\s+\d{1,2}(,\s+\d{4})?,\s+\d{1,2}:\d{2}\s*(?:AM|PM)\s*\(\d+ (?:hours|days) ago\)$|^\w{3}\s+\d{1,2}(,\s+\d{4})?,\s+\d{1,2}:\d{2}\s*(?:AM|PM)|^\w{3}\s+\d{1,2}(,\s+\d{4})?$|^Today$|\d{4}-\d{2}-\d{2}T|^\d{1,2}:\d{2}\s*(?:AM|PM)\s*\(\d+ (?:hours|days) ago\)$|^as-it-happens$', line, re.IGNORECASE):
                date_text = line
        
        # Fallback for metadata if not found
        if from_header == 'Unknown':
            for i, line in enumerate(cleaned_lines, 1):
                if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line, re.IGNORECASE):
                    from_header = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line, re.IGNORECASE).group()
                    logging.warning(f"Fallback sender identified for {filename}: {line}")
                    break
        if subject_text == 'Unknown':
            for i, line in enumerate(cleaned_lines, 1):
                if re.search(r'job|jobs|career|careers|opportunity|opportunities|alert|matching', line, re.IGNORECASE) and not re.search(r'Your job alert|has been created', line, re.IGNORECASE):
                    subject_text = line
                    logging.warning(f"Fallback subject identified for {filename}: {line}")
                    break
        if date_text == 'Unknown':
            for i, line in enumerate(cleaned_lines, 1):
                if re.search(r'\d{4}-\d{2}-\d{2}|\w{3},\s+\w{3}\s+\d{1,2}|as-it-happens|\d{1,2}:\d{2}\s*(?:AM|PM)', line, re.IGNORECASE):
                    date_text = line
                    logging.warning(f"Fallback date identified for {filename}: {line}")
                    break
        
        # Log parsing results (only warnings/errors)
        logging.warning(f"Parsed metadata for {filename}: sender={from_header}, subject={subject_text}, date={date_text}")
        if from_header == 'Unknown':
            logging.warning(f"Sender not identified for {filename}. First 20 lines:")
            for i, line in enumerate(cleaned_lines[:20], 1):
                logging.warning(f"Line {i}: {line}")
        if subject_text == 'Unknown':
            logging.warning(f"Subject not identified for {filename}. First 20 lines:")
            for i, line in enumerate(cleaned_lines[:20], 1):
                logging.warning(f"Line {i}: {line}")
        if date_text == 'Unknown':
            logging.warning(f"Date not identified for {filename}. First 20 lines:")
            for i, line in enumerate(cleaned_lines[:20], 1):
                logging.warning(f"Line {i}: {line}")
        
        # Extract job postings with Remote prioritization
        job_section = False
        current_posting = {'position': '', 'location': '', 'qualifications': ''}
        start_str = 'Turn on job alerts for this search|Job alerts|New jobs|Your job listings for|New Jobs on LinkedIn'
        seen_positions = set()  # For deduplication
        
        position_pattern = r'Manager|Engineer|Developer|Analyst|Specialist|Associate|Coordinator|Director|Senior|Junior|Lead|Executive|Officer|Consultant|Designer|Administrator|Technician|Operator|Supervisor|Architect|Scientist|Artist|Writer|Teacher|Professor|Nurse|Doctor|Lawyer|Accountant|Marketing|Sales|HR|IT|Support|Service|Project|Program|Assistant|HVAC'
        location_pattern = r'Bangkok|Manhattan|New York|Long Island City|Astoria|Remote|On-site|Thailand|Singapore|USA|India|London|San Francisco|Seattle|Mountain View|Sunnyvale|Atlanta|Chicago|Boston|Dublin|Zurich|Hyderabad|Bangalore|Tokyo|Sydney|Ho Chi Minh City|Kuala Lumpur|Jakarta|Hanoi|Nong Yai|Hong Kong|Taiwan|Canada|NAMER|[A-Z][a-z]+,\s*[A-Z]{2}|place\s+.*'
        qualifications_pattern = r"Bachelor\'s degree|Master\'s degree|PhD|years of experience|practical experience|Microsoft|AutoCAD|Architecture|Construction|Management|Full-time|Background check|Weekly pay|Equivalent experience|Ability to|Knowledge of|Proficient in|Experience with|Required|Preferred|Qualifications|Skills|Education|Minimum qualifications|Easy Apply|hour shift|Report writing|Commission pay|Oracle|PMP|Weekends as needed|Yearly pay|Mid-level|Multiple hires|Laboratory|Paid parental leave"
        
        # Prioritize Remote and English job titles
        remote_job_position = 'Unknown'
        english_job_position = 'Unknown'
        for line in cleaned_lines:
            line = line.strip()
            if re.search(start_str, line, re.IGNORECASE):
                job_section = True
                continue
            if job_section:
                if re.search(position_pattern, line, re.IGNORECASE):
                    # Check if the line is ASCII-only (English)
                    if all(ord(c) < 128 for c in line):
                        if current_posting['position'] and current_posting['position'] not in seen_positions:
                            job_postings.append(f"{current_posting['position']} | {current_posting['location'] or 'Unknown'} | {current_posting['qualifications'] or 'Unknown'}")
                            seen_positions.add(current_posting['position'])
                        current_posting = {'position': line, 'location': '', 'qualifications': ''}
                        if english_job_position == 'Unknown':
                            english_job_position = line
                        # Prioritize Remote positions
                        if re.search(r'\bRemote\b|\(Remote\)', line, re.IGNORECASE):
                            remote_job_position = line
                            remote = True
                            logging.warning(f"Remote position prioritized for {filename}: {line}")
                    else:
                        logging.warning(f"Non-English position skipped for {filename}: {line}")
                    continue
                if line:
                    if re.search(location_pattern, line, re.IGNORECASE):
                        current_posting['location'] = line.replace('place ', '')
                        if location == 'Unknown':
                            location = line.replace('place ', '')
                        # Prioritize Remote location
                        if re.search(r'\bRemote\b|\(Remote\)', line, re.IGNORECASE):
                            remote_job_position = current_posting['position'] or english_job_position
                            remote = True
                            logging.warning(f"Remote location prioritized for {filename}: {line}")
                    elif re.search(qualifications_pattern, line, re.IGNORECASE):
                        if current_posting['qualifications']:
                            current_posting['qualifications'] += '\n' + line
                        else:
                            current_posting['qualifications'] = line
                        if minimum_qualifications == 'Unknown':
                            minimum_qualifications = line
        
        if current_posting['position'] and current_posting['position'] not in seen_positions:
            job_postings.append(f"{current_posting['position']} | {current_posting['location'] or 'Unknown'} | {current_posting['qualifications'] or 'Unknown'}")
            seen_positions.add(current_posting['position'])
        
        job_postings_str = ', '.join(job_postings) if job_postings else 'Unknown'
        job_position = remote_job_position if remote_job_position != 'Unknown' else english_job_position  # Prioritize Remote
        
        if job_postings_str == 'Unknown':
            logging.warning(f"No job postings identified for {filename}. First 20 lines:")
            for i, line in enumerate(cleaned_lines[:20], 1):
                logging.warning(f"Line {i}: {line}")
        else:
            logging.warning(f"Extracted job postings for {filename}: {job_postings_str[:100]}...")
        
        return from_header, subject_text, date_text, job_position, location, minimum_qualifications, job_postings_str, remote
    except Exception as e:
        logging.error(f"Error parsing {filename}: {e}")
        raise

# Process email dumps
def process_email_dumps():
    json_data = init_json()
    success_count = 0
    fail_count = 0
    
    try:
        for filename in os.listdir(EMAIL_DUMPS_DIR):
            if filename.endswith('.txt'):
                file_path = os.path.join(EMAIL_DUMPS_DIR, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    source = identify_source(content, '')
                    if source is None:
                        logging.warning(f"Unknown source for {filename}. Aborting processing.")
                        fail_count += 1
                        continue
                    
                    from_header, subject, date, job_position, location, minimum_qualifications, job_postings, remote = parse_email(content, filename, source)
                    
                    processed_at = datetime.now().isoformat()
                    entry = {
                        'id': len(json_data) + 1,
                        'filename': filename,
                        'sender': from_header,
                        'subject': subject,
                        'date': date,
                        'source': source,
                        'content': content,
                        'processed_at': processed_at,
                        'job_position': job_position,
                        'location': location,
                        'minimum_qualifications': minimum_qualifications,
                        'job_postings': job_postings,
                        'remote': remote
                    }
                    save_to_json(json_data, entry)
                    success_count += 1
                except Exception as e:
                    logging.error(f"Error processing {filename}: {e}")
                    fail_count += 1
                    continue
        print(f"Processed {success_count} files successfully, {fail_count} failed. Details in {LOG_DIR}/parse_errors.log")
        generate_output(json_data)
    except Exception as e:
        logging.error(f"Processing error: {e}")
        print(f"Error during processing. Check {LOG_DIR}/parse_errors.log")

if __name__ == "__main__":
    process_email_dumps()