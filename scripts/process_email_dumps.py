# File: process_email_dumps.py
# Owner: silicastormsiam
# Purpose: Process email dumps for R.A.T.S. project, including source identification, parsing, and storage in JSON for job alert management, prioritizing English job titles and Remote positions, with minimal console output, robust logging limited to data errors per run, and user-friendly output files (txt/html/reports) with static HTML table, sortable headers, dropdown checkbox filtering, and pivot tables styled with Cyberpunk Monk color palette.
# Version Control: 7.26
# Change Log:
# - 2025-08-07: Version 7.22 - Removed redundant File dropdown; added Remote dropdown filter; fixed parsing issues for GoogleCareers; enhanced English-only filtering; maintained .gitignore at version 2.3; updated analyze_errors.py for processing failure diagnostics; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
# - 2025-08-07: Version 7.23 - Fixed 'pos' keyword error in parse_email; removed File column; added footer note with script version; restored all job postings with deduplication; enhanced GoogleCareers parsing; improved remote detection; maintained .gitignore at version 2.3; updated analyze_errors.py for remote field diagnostics; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
# - 2025-08-07: Version 7.24 - Fixed limited data issue by improving section parsing and deduplication; corrected non-English job titles and invalid positions; enhanced remote status detection; maintained .gitignore at version 2.3; updated analyze_errors.py for remote field and parsing diagnostics; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
# - 2025-08-07: Version 7.25 - Removed deduplication to restore all data; fixed IndentationError in HTML output; corrected non-English job titles and invalid locations; enhanced remote detection; maintained .gitignore at version 2.3; updated analyze_errors.py for indentation and data limitation diagnostics; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
# - 2025-08-07: Version 7.26 - Fixed JavaScript filtering to display all data; corrected IndentationError in HTML output; refined non-English job title filtering; improved remote status detection; maintained .gitignore at version 2.3; updated analyze_errors.py for JavaScript and parsing diagnostics; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
import os
import re
import json
from datetime import datetime
import logging
import html
import unicodedata

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
RATS_DATA_REPORT_PATH = os.path.join(PROJECT_ROOT, 'logs', 'rats_data_report.txt')
PARSED_JOBS_REPORT_PATH = os.path.join(PROJECT_ROOT, 'logs', 'parsed_jobs_report.txt')
PARSE_ERRORS_REPORT_PATH = os.path.join(PROJECT_ROOT, 'logs', 'parse_errors_report.txt')

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
        logging.warning(f"Initialized JSON storage at {JSON_PATH} with {len(data)} entries")
        return data
    except json.JSONDecodeError as e:
        logging.error(f"JSON initialization error: Invalid JSON in {JSON_PATH}: {e}")
        raise
    except Exception as e:
        logging.error(f"JSON initialization error: {e}")
        raise

# Save to JSON (append without overwriting)
def save_to_json(data, entry):
    try:
        # Validate entry before appending
        required_fields = ['filename', 'source', 'sender', 'job_position', 'location', 'minimum_qualifications', 'remote']
        for field in required_fields:
            if field not in entry:
                logging.error(f"Missing field {field} in entry for {entry.get('filename', 'unknown')}")
                raise ValueError(f"Missing field {field} in entry")
        data.append(entry)
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logging.warning(f"Saved entry for {entry['filename']} to {JSON_PATH}")
    except json.JSONDecodeError as e:
        logging.error(f"Error saving to JSON for {entry.get('filename', 'unknown')}: Invalid JSON: {e}")
        raise
    except Exception as e:
        logging.error(f"Error saving to JSON for {entry.get('filename', 'unknown')}: {e}")
        raise

# Generate user-friendly output files (txt, html, reports)
def generate_output(data):
    try:
        # Text output (all entries)
        with open(TXT_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write("R.A.T.S. - Recruitment Alert Tracking System for CAPM\n")
            f.write("==================================================\n")
            for entry in data:
                f.write(f"\nSource: {entry['source']} (Email: {entry['sender']})\n")
                f.write(f"Job Position: {entry['job_position']}\n")
                f.write(f"Location: {entry['location']}\n")
                f.write(f"Min Requirements: {entry['minimum_qualifications']}\n")
                f.write(f"Remote: {'Yes' if entry.get('remote', False) else 'No'}\n")
                f.write("------------------------------------\n")
        logging.warning(f"Generated text output at {TXT_OUTPUT_PATH} with {len(data)} entries")
        
        # Validate JSON data with encoding checks
        json_data_str = "[]"
        validated_data = []
        try:
            for entry in data:
                validated_entry = {}
                for key, value in entry.items():
                    if isinstance(value, str):
                        # Normalize Unicode and encode to ASCII, ignoring errors
                        validated_entry[key] = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
                    else:
                        validated_entry[key] = value
                validated_data.append(validated_entry)
            json_data_str = json.dumps(validated_data, indent=2, ensure_ascii=False)
            logging.warning(f"Validated JSON data with {len(validated_data)} entries for HTML output")
        except json.JSONDecodeError as e:
            logging.error(f"JSON serialization error: Invalid JSON data: {e}")
            json_data_str = "[]"
        except Exception as e:
            logging.error(f"JSON serialization error: {e}")
            json_data_str = "[]"
        
        # Generate static table in Python
        static_table = ""
        if validated_data:
            for entry in validated_data:
                try:
                    static_table += (
                        f'<tr data-source="{html.escape(str(entry["source"]))}" data-remote="{html.escape("Yes" if entry.get("remote", False) else "No")}">'
                        f'<td>{html.escape(str(entry["source"]))} ({html.escape(str(entry["sender"]))})</td>'
                        f'<td>{html.escape(str(entry["job_position"]))}</td>'
                        f'<td>{html.escape(str(entry["location"]))}</td>'
                        f'<td>{html.escape(str(entry["minimum_qualifications"])).replace("\n", "<br>")}</td>'
                        f'<td>{"Yes" if entry.get("remote", False) else "No"}</td>'
                        f'</tr>'
                    )
                except Exception as e:
                    logging.error(f"Error generating static table entry for {entry.get('source', 'unknown')}: {e}")
            logging.warning(f"Generated static table with {len(validated_data)} entries")
        else:
            static_table = '<tr><td colspan="5">No data available</td></tr>'
            logging.warning("No data available for static table")
        
        # Generate source options for dropdown
        source_options = "".join([f'<div class="dropdown-option"><input type="checkbox" class="filter-checkbox" data-type="source" value="{html.escape(source)}"> {html.escape(source)}</div>' for source in sorted(set(entry["source"] for entry in validated_data))])
        # Generate remote options for dropdown
        remote_options = (
            '<div class="dropdown-option"><input type="checkbox" class="filter-checkbox" data-type="remote" value="Yes"> Yes</div>'
            '<div class="dropdown-option"><input type="checkbox" class="filter-checkbox" data-type="remote" value="No"> No</div>'
        )
        
        # HTML output (static table with sortable headers, source and remote dropdown checkbox filtering, and pivot tables, Cyberpunk Monk palette)
        with open(HTML_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            html_content = [
                '<!DOCTYPE html>',
                '<html>',
                '<head>',
                '    <title>R.A.T.S. - Recruitment Alert Tracking System for CAPM</title>',
                '    <style>',
                '        body { font-family: Arial, sans-serif; margin: 20px; background-color: #1F2937; color: #1F2937; }',
                '        h1 { text-align: center; color: #FFFFFF; background-color: #0F172A; padding: 10px; }',
                '        table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #E2E8F0; }',
                '        th, td { border: 1px solid #D1D5DB; padding: 8px; text-align: left; color: #4B5563; }',
                '        th { background-color: #0F172A; color: #FFFFFF; cursor: pointer; }',
                '        th:hover { color: #F472B6; }',
                '        tr:nth-child(even) { background-color: #D1D5DB; }',
                '        tr:hover { background-color: #E2E8F0; }',
                '        .filter { margin-bottom: 20px; background-color: #D1D5DB; padding: 10px; }',
                '        .filter label { color: #F472B6; font-size: 18px; }',
                '        .dropdown { position: relative; display: inline-block; margin-right: 20px; }',
                '        .dropdown-button { background-color: #3B82F6; color: #FFFFFF; border: 1px solid #FFFFFF; padding: 5px 10px; cursor: pointer; }',
                '        .dropdown-button:hover { background-color: #2563EB; }',
                '        .dropdown-content { display: none; position: absolute; background-color: #E2E8F0; min-width: 200px; box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2); z-index: 1; padding: 10px; }',
                '        .dropdown:hover .dropdown-content { display: block; }',
                '        .dropdown-option { padding: 5px; }',
                '        .error { color: #DC2626; }',
                '        footer { margin-top: 20px; text-align: center; color: #4B5563; }',
                '        #pivotTable { margin-top: 20px; border: 1px solid #F472B6; background-color: #0F172A; }',
                '        #pivotTable .pvtTable { background-color: #E2E8F0; color: #4B5563; }',
                '        #pivotTable .pvtTable th { background-color: #0F172A; color: #FFFFFF; }',
                '        #pivotTable .pvtTable td { border: 1px solid #D1D5DB; }',
                '        #debugJson { display: none; margin-top: 20px; background-color: #E2E8F0; padding: 10px; }',
                '        #debugToggle { margin-top: 10px; background-color: #3B82F6; color: #FFFFFF; border: 1px solid #FFFFFF; padding: 5px 10px; cursor: pointer; }',
                '        #debugToggle:hover { background-color: #2563EB; }',
                '    </style>',
                '    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>',
                '    <script src="https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.js"></script>',
                '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.css">',
                '    <script>',
                '        document.addEventListener("DOMContentLoaded", function() {',
                '            let data = [];',
                '            try {',
                f'                data = {json_data_str};',
                '                console.log("JSON data loaded with " + data.length + " entries");',
                '            } catch (e) {',
                '                console.error("Failed to parse JSON data: " + e.message);',
                '                document.getElementById("jobTable").insertAdjacentHTML("afterend", \'<p class="error">Failed to parse job data: \' + e.message + \'</p>\');',
                '            }',
                '            function renderTable(filteredData) {',
                '                console.log("Rendering table with " + filteredData.length + " entries");',
                '                const tbody = document.querySelector("#jobTable tbody");',
                '                tbody.innerHTML = "";',  # Clear table before rendering
                '                filteredData.forEach(entry => {',
                '                    tbody.innerHTML += `',
                '                        <tr data-source="${entry.source}" data-remote="${entry.remote ? "Yes" : "No"}">',
                '                            <td>${entry.source} (${entry.sender})</td>',
                '                            <td>${entry.job_position}</td>',
                '                            <td>${entry.location}</td>',
                '                            <td>${entry.minimum_qualifications.replace(/\\n/g, "<br>")}</td>',
                '                            <td>${entry.remote ? "Yes" : "No"}</td>',
                '                        </tr>`;',
                '                });',
                '                if (filteredData.length === 0) {',
                '                    tbody.innerHTML = \'<tr><td colspan="5">No data matches the selected filters</td></tr>\';',
                '                }',
                '            }',
                '            try {',
                '                renderTable(data);',  # Display all data initially
                '                $("#pivotTable").pivotUI(data, {',
                '                    rows: ["source"],',
                '                    cols: ["remote"],',
                '                    vals: ["job_position"],',
                '                    aggregatorName: "Count",',
                '                    rendererName: "Table"',
                '                });',
                '                console.log("Pivot table rendered");',
                '            } catch (e) {',
                '                console.error("Failed to process job data: " + e.message);',
                '                document.getElementById("jobTable").insertAdjacentHTML("afterend", \'<p class="error">Failed to process job data: \' + e.message + \'</p>\');',
                '            }',
                '            document.querySelectorAll("#jobTable th").forEach(th => {',
                '                th.addEventListener("click", function() {',
                '                    const column = this.getAttribute("data-column");',
                '                    let order = this.getAttribute("data-order") === "asc" ? "desc" : "asc";',
                '                    this.setAttribute("data-order", order);',
                '                    console.log("Sorting by " + column + " in " + order + " order");',
                '                    data.sort((a, b) => {',
                '                        let aValue = a[column] || "";',
                '                        let bValue = b[column] || "";',
                '                        if (column === "remote") {',
                '                            aValue = a[column] ? "Yes" : "No";',
                '                            bValue = b[column] ? "Yes" : "No";',
                '                        }',
                '                        return order === "asc" ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);',
                '                    });',
                '                    renderTable(data);',
                '                });',
                '            });',
                '            function applyFilters() {',
                '                console.log("Applying filters");',
                '                const selectedSources = Array.from(document.querySelectorAll("#sourceFilter .filter-checkbox:checked")).map(cb => cb.value);',
                '                const selectedRemotes = Array.from(document.querySelectorAll("#remoteFilter .filter-checkbox:checked")).map(cb => cb.value);',
                '                console.log("Selected Sources: " + selectedSources);',
                '                console.log("Selected Remotes: " + selectedRemotes);',
                '                const filteredData = data.filter(entry => {',
                '                    const sourceMatch = selectedSources.length === 0 || selectedSources.includes(entry.source);',
                '                    const remoteMatch = selectedRemotes.length === 0 || selectedRemotes.includes(entry.remote ? "Yes" : "No");',
                '                    return sourceMatch && remoteMatch;',
                '                });',
                '                console.log("Filtered data to " + filteredData.length + " entries");',
                '                renderTable(filteredData);',
                '            }',
                '            document.querySelectorAll(".filter-checkbox").forEach(cb => {',
                '                cb.addEventListener("change", function() {',
                '                    console.log("Checkbox changed: " + this.value + " is " + (this.checked ? "checked" : "unchecked"));',
                '                    applyFilters();',
                '                });',
                '            });',
                '            document.getElementById("resetFilter").addEventListener("click", function() {',
                '                document.querySelectorAll(".filter-checkbox").forEach(cb => {',
                '                    cb.checked = false;',
                '                    console.log("Reset checkbox: " + cb.value);',
                '                });',
                '                console.log("Filters reset");',
                '                renderTable(data);',
                '            });',
                '            document.getElementById("debugToggle").addEventListener("click", function() {',
                '                const debugJson = document.getElementById("debugJson");',
                '                debugJson.style.display = debugJson.style.display === "none" ? "block" : "none";',
                '                console.log("Debug JSON toggled");',
                '            });',
                '        });',
                '    </script>',
                '</head>',
                '<body>',
                '    <h1>R.A.T.S. - Recruitment Alert Tracking System for CAPM</h1>',
                '    <div class="filter">',
                '        <div class="dropdown">',
                '            <label>Select Sources: </label>',
                '            <button class="dropdown-button">Select Sources</button>',
                '            <div class="dropdown-content" id="sourceFilter">',
                f'                {source_options}',
                '            </div>',
                '        </div>',
                '        <div class="dropdown">',
                '            <label>Select Remote: </label>',
                '            <button class="dropdown-button">Select Remote</button>',
                '            <div class="dropdown-content" id="remoteFilter">',
                f'                {remote_options}',
                '            </div>',
                '        </div>',
                '        <button id="resetFilter">Reset Filters</button>',
                '    </div>',
                '    <table id="jobTable">',
                '        <thead>',
                '            <tr>',
                '                <th data-column="source">Source (Email)</th>',
                '                <th data-column="job_position">Job Position</th>',
                '                <th data-column="location">Location</th>',
                '                <th data-column="minimum_qualifications">Minimum Requirements</th>',
                '                <th data-column="remote">Remote</th>',
                '            </tr>',
                '        </thead>',
                '        <tbody>',
                f'            {static_table}',
                '        </tbody>',
                '    </table>',
                '    <h2>Pivot Table</h2>',
                '    <div id="pivotTable"></div>',
                '    <button id="debugToggle">Toggle Debug JSON</button>',
                f'    <pre id="debugJson">{html.escape(json_data_str)}</pre>',
                '    <footer>Generated by process_email_dumps.py version 7.26</footer>',
                '</body>',
                '</html>'
            ]
            f.write('\n'.join(html_content))
        
        # Generate separate log reports
        with open(RATS_DATA_REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write("R.A.T.S. rats_data.json Report\n")
            f.write("=============================\n\n")
            with open(JSON_PATH, 'r', encoding='utf-8') as json_file:
                f.write(json_file.read())
        
        with open(PARSED_JOBS_REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write("R.A.T.S. parsed_jobs_output.txt Report\n")
            f.write("=====================================\n\n")
            with open(TXT_OUTPUT_PATH, 'r', encoding='utf-8') as txt_file:
                f.write(txt_file.read())
        
        with open(PARSE_ERRORS_REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write("R.A.T.S. parse_errors.log Report (Data Errors)\n")
            f.write("============================================\n\n")
            with open(os.path.join(LOG_DIR, 'parse_errors.log'), 'r', encoding='utf-8', errors='ignore') as log_file:
                f.write(log_file.read())
        
        logging.warning(f"Generated output files at {TXT_OUTPUT_PATH}, {HTML_OUTPUT_PATH}, {RATS_DATA_REPORT_PATH}, {PARSED_JOBS_REPORT_PATH}, {PARSE_ERRORS_REPORT_PATH}")
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
        # Handle combined Glassdoor file with separators
        sections = [content] if 'glassdoor_email_1.txt' not in filename else re.split(r'--- glassdoor_email_\d+\.txt ---', content)
        all_job_postings = []
        all_seen_positions = set()
        from_header = 'Unknown'
        subject_text = 'Unknown'
        date_text = 'Unknown'
        job_position = 'Unknown'
        location = 'Unknown'
        minimum_qualifications = 'Unknown'
        remote = False

        for section in sections:
            section = section.strip()
            if not section:
                continue
            cleaned_lines = [line for line in section.splitlines() if not re.search(r'(None selected|Skip to content|Using Gmail with screen readers|to me|Google apps|–Conversations|Your job alert|has been created)', line, re.IGNORECASE)]
            job_postings = []
            seen_positions = set()
            
            # Parse first 50 lines for metadata
            for i, line in enumerate(cleaned_lines[:50], 1):
                line = line.strip()
                if from_header == 'Unknown' and re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line, re.IGNORECASE):
                    from_header = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line, re.IGNORECASE).group()
                if subject_text == 'Unknown' and line and not re.match(r'[\w\.-]+@[\w\.-]+\.\w+|^\w{3},\s+\w{3}\s+\d{1,2}(,\s+\d{4})?,\s+\d{1,2}:\d{2}\s*(?:AM|PM)', line, re.IGNORECASE):
                    if re.search(r'job|jobs|career|careers|opportunity|opportunities|New job\(s\)|Project|Program|Assistant|alert|matching', line, re.IGNORECASE):
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
                    if re.search(r'job|jobs|career|careers|opportunity|opportunities|alert|matching', line, re.IGNORECASE):
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
            
            # Extract job postings with Remote prioritization and enhanced GoogleCareers parsing
            job_section = False
            current_posting = {'position': '', 'location': '', 'qualifications': ''}
            start_str = r'Turn on job alerts for this search|Job alerts|New jobs|Your job listings for|New Jobs on LinkedIn|Jobs matching your search'
            
            # Enhanced patterns for GoogleCareers
            position_pattern = r'(?:Manager|Engineer|Developer|Analyst|Specialist|Associate|Coordinator|Director|Senior|Junior|Lead|Executive|Officer|Consultant|Designer|Administrator|Technician|Operator|Supervisor|Architect|Scientist|Artist|Writer|Teacher|Professor|Nurse|Doctor|Lawyer|Accountant|Marketing|Sales|HR|IT|Support|Service|Project|Program|Assistant|HVAC|Customer Solutions|Cloud|AI|Machine Learning|Data Scientist|Product Manager|Business|Operations|Strategist|Researcher|Technical Lead|Acquisition|MarTech)\b(?:\s*(?:[-/&]\s*\w+)*)?'
            location_pattern = r'(?:Bangkok|Manhattan|New York|Long Island City|Astoria|Remote|On-site|Hybrid|Thailand|Singapore|USA|India|London|San Francisco|Seattle|Mountain View|Sunnyvale|Atlanta|Chicago|Boston|Dublin|Zurich|Hyderabad|Bangalore|Tokyo|Sydney|Kuala Lumpur|Canada|NAMER|[A-Z][a-z]+,\s*[A-Z]{2}|place\s+.*|\b[A-Z][a-zA-Z\s]*(?:,\s*[A-Z]{2})?\b|Multiple locations)'
            qualifications_pattern = r"(?:Bachelor\'s degree|Master\'s degree|PhD|years of experience|practical experience|Microsoft|AutoCAD|Architecture|Construction|Management|Full-time|Background check|Weekly pay|Equivalent experience|Ability to|Knowledge of|Proficient in|Experience with|Required|Preferred|Qualifications|Skills|Education|Minimum qualifications|Easy Apply|hour shift|Report writing|Commission pay|Oracle|PMP|Weekends as needed|Yearly pay|Mid-level|Multiple hires|Laboratory|Paid parental leave|Fluency in [A-Za-z]+|Certifications?|Technical skills|Strong communication|Team collaboration|\$[0-9]+K\s*-\s*\$[0-9]+K)"
            
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
                        # Strict English check with allowed special characters
                        if all(ord(c) < 128 or c in '-/&[]' for c in line) and not re.search(r'[^\x00-\x7F]', line):
                            if current_posting['position'] and current_posting['position'] not in seen_positions:
                                job_postings.append({
                                    'position': current_posting['position'],
                                    'location': current_posting['location'] or 'Unknown',
                                    'qualifications': current_posting['qualifications'] or 'Unknown'
                                })
                                seen_positions.add(current_posting['position'])
                            current_posting = {'position': line, 'location': '', 'qualifications': ''}
                            if english_job_position == 'Unknown':
                                english_job_position = line
                            # Prioritize Remote positions
                            if re.search(r'\bRemote\b|\(Remote\)|Hybrid|Remote eligible', line, re.IGNORECASE):
                                remote_job_position = line
                                remote = True
                                logging.warning(f"Remote position prioritized for {filename}: {line}")
                        else:
                            logging.warning(f"Non-English position skipped for {filename}: {line}")
                        continue
                    if line:
                        if re.search(location_pattern, line, re.IGNORECASE) and not re.search(r'\d{1,2}:\d{2}\s*(?:AM|PM)', line, re.IGNORECASE):
                            current_posting['location'] = line.replace('place ', '')
                            if location == 'Unknown':
                                location = line.replace('place ', '')
                            # Prioritize Remote location
                            if re.search(r'\bRemote\b|\(Remote\)|Hybrid|Remote eligible', line, re.IGNORECASE):
                                remote_job_position = current_posting['position'] or english_job_position
                                remote = True
                                logging.warning(f"Remote location prioritized for {filename}: {line}")
                        elif re.search(qualifications_pattern, line, re.IGNORECASE) and not re.search(r'weeks of paid vacation', line, re.IGNORECASE):
                            if current_posting['qualifications']:
                                current_posting['qualifications'] += '\n' + line
                            else:
                                current_posting['qualifications'] = line
                            if minimum_qualifications == 'Unknown':
                                minimum_qualifications = line
            
            # Enhanced fallback parsing for GoogleCareers
            if source == 'GoogleCareers' and not job_postings:
                logging.warning(f"No job postings found for {filename}. Attempting enhanced fallback parsing.")
                for i, line in enumerate(cleaned_lines):
                    line = line.strip()
                    if re.search(r'\b[A-Z][a-zA-Z\s]*(?:Manager|Engineer|Specialist|Analyst|Developer|Consultant|Coordinator|Director|Customer Solutions|Cloud|AI|Machine Learning|Data Scientist|Product Manager|Business|Operations|Strategist|Researcher|Technical Lead|Acquisition|MarTech)\b(?:\s*(?:[-/&]\s*\w+)*)?', line, re.IGNORECASE):
                        if all(ord(c) < 128 or c in '-/&[]' for c in line) and not re.search(r'[^\x00-\x7F]', line):
                            if current_posting['position'] and current_posting['position'] not in seen_positions:
                                job_postings.append({
                                    'position': current_posting['position'],
                                    'location': current_posting['location'] or 'Unknown',
                                    'qualifications': current_posting['qualifications'] or 'Unknown'
                                })
                                seen_positions.add(current_posting['position'])
                            current_posting = {'position': line, 'location': '', 'qualifications': ''}
                            if english_job_position == 'Unknown':
                                english_job_position = line
                            if re.search(r'\bRemote\b|\(Remote\)|Hybrid|Remote eligible', line, re.IGNORECASE):
                                remote_job_position = line
                                remote = True
                        continue
                    if re.search(location_pattern, line, re.IGNORECASE) and not re.search(r'\d{1,2}:\d{2}\s*(?:AM|PM)', line, re.IGNORECASE):
                        current_posting['location'] = line
                        if location == 'Unknown':
                            location = line
                        if re.search(r'\bRemote\b|\(Remote\)|Hybrid|Remote eligible', line, re.IGNORECASE):
                            remote = True
                        continue
                    if re.search(qualifications_pattern, line, re.IGNORECASE) and not re.search(r'weeks of paid vacation', line, re.IGNORECASE):
                        if current_posting['qualifications']:
                            current_posting['qualifications'] += '\n' + line
                        else:
                            current_posting['qualifications'] = line
                        if minimum_qualifications == 'Unknown':
                            minimum_qualifications = line
            
            if current_posting['position'] and current_posting['position'] not in seen_positions:
                job_postings.append({
                    'position': current_posting['position'],
                    'location': current_posting['location'] or 'Unknown',
                    'qualifications': current_posting['qualifications'] or 'Unknown'
                })
                seen_positions.add(current_posting['position'])
            
            # Aggregate job postings
            for posting in job_postings:
                all_job_postings.append(posting)
        
        if not all_job_postings:
            logging.warning(f"No job postings identified for {filename}. First 20 lines:")
            for i, line in enumerate(cleaned_lines[:20], 1):
                logging.warning(f"Line {i}: {line}")
        else:
            logging.warning(f"Extracted {len(all_job_postings)} job postings for {filename}")
        
        # Select the first remote job or first English job
        job_position = remote_job_position if remote_job_position != 'Unknown' else english_job_position
        job_postings_str = ', '.join([f"{p['position']} | {p['location']} | {p['qualifications']}" for p in all_job_postings]) if all_job_postings else 'Unknown'
        
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