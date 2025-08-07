# R.A.T.S. Workflow and Project Handover Document
## Metadata
- **File Name**: workflow.md
- **Owner**: silicastormsiam
- **Purpose**: Comprehensive handover for R.A.T.S. project, detailing introduction, objectives, workflow, version control, source identification, troubleshooting, critical guidance from Andrew, and project shutdown/resurrection details.
- **Version Control**: 1.40
- **Change Log**:
  - 2025-08-07: Version 1.36 - Fixed JavaScript filtering to display all data; confirmed R.A.T.S. online with full data and filtering; added local backup with date stamp; maintained .gitignore at version 2.3; updated analyze_errors.py for JavaScript and parsing diagnostics; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
  - 2025-08-07: Version 1.37 - Added backup options for zip failure; confirmed R.A.T.S. stability with full data display; maintained .gitignore at version 2.3; updated analyze_errors.py for backup and parsing diagnostics; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
  - 2025-08-07: Version 1.38 - Verified tar backup success; added PowerShell backup instructions; confirmed R.A.T.S. data display stability; maintained .gitignore at version 2.3; updated analyze_errors.py for backup verification; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
  - 2025-08-07: Version 1.39 - Clarified PowerShell backup in PowerShell terminal; confirmed tar backup integrity; maintained .gitignore at version 2.3; updated analyze_errors.py for backup and parsing diagnostics; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.
  - 2025-08-07: Version 1.40 - Confirmed tar and PowerShell backup success; resolved PowerShell command errors in Git Bash; maintained .gitignore at version 2.3; updated analyze_errors.py for backup verification; retained separate report files, no line limits, sortable headers, dropdown checkbox filtering, Cyberpunk Monk palette, data error logging, English-only title prioritization, Remote prioritization; ensured metadata compliance.

## 0. Preliminary Note
Pause OneDrive syncing before Git operations (e.g., 2025-08-07, 08:02 AM +07, 7-hour pause) via system tray to prevent .git corruption. Resume after.

## 1. Introduction to the Project
The Recruitment Alerts Tracking System (R.A.T.S.) is an AI-powered tool designed to streamline job alert email management for job seekers, intended as a backend for a recruitment dashboard. It aggregates alerts from platforms like Glassdoor, LinkedIn, and planned sources (12 total), extracting details into JSON for retrieval and analysis. Built with Python for backend processing, it includes plans for FastAPI backend, React/Tailwind frontend, and OpenAI/LangChain for AI keyword matching. Hosted locally on the ROG-STRIX-B550F at `M:\OneDrive\Documents\GitHub\RATS`, it syncs to GitHub for version control, adhering to compliance by incrementing version numbers.

### 1.1 Purpose of Handover
This document equips a new project manager with setup, workflow, and lessons learned (e.g., pivoting source identification, RAM optimization) to ensure seamless development for real-time, AI-driven job search features. The project was shut down due to regressions but resurrected with JSON storage and enhanced output/logging.

### 1.2 Development Context
Iterative development addressed malformed email headers, database access, and RAM issues. Version 2.7 of `process_email_dumps.py` was functional before shutdown. Resurrection updates (versions 5.0–7.26) transitioned to JSON storage (`rats_data.json`), added `parsed_jobs_output.txt`, `parsed_jobs_output.html` with static table, sortable headers, dropdown checkbox filtering, and optional pivot tables styled with Cyberpunk Monk palette, separate report files (`rats_data_report.txt`, `parsed_jobs_report.txt`, `parse_errors_report.txt`, `error_recovery_report.txt`, `combined_reports.txt`), `analyze_errors.py` for error recovery, `combine_glassdoor_emails.py` for merging Glassdoor files, `combine_report_files.py` for merging reports, removed line limits for txt/json outputs, restricted logging to data errors per run, and fixed syntax/key/data rendering/GoogleCareers parsing/dropdown issues.

## 2. Project Objectives
- **Automation**: Parse email dumps, store in JSON (`rats_data.json`).
- **Source Identification**: Detect sources (Glassdoor via copyright footer, GoogleCareers/LinkedIn via sender/content), supporting 12 sources without 'Unknown'.
- **Compliance**: Increment version numbers for traceability; limit change logs to 5 entries; update `.gitignore` only for file structure changes.
- **AI Integration**: Match alerts to preferences using OpenAI/LangChain.
- **User Experience**: Notifications, dashboards, auto-apply features; user-friendly `parsed_jobs_output.txt`, `parsed_jobs_output.html` (static table, sortable headers, dropdown checkbox filtering, optional pivot tables, Cyberpunk Monk palette), and report files.
- **Scalability**: API/RSS feeds, browser extensions, Trello-style boards.
- **Data Security**: Exclude sensitive data via `.gitignore`.

## 3. Metadata Requirements
- **Scope**: Scripts (.py) and documentation (.md) require metadata; data dumps (.txt) are raw.
- **Format**: File Name, Owner (silicastormsiam), Purpose, Version Control, Change Log (max 5 entries).
- **Compliance**: Increment versions only for the updated file; no overwriting without increment. Each sequence of changes requires changing the version number for traceability and adherence to government regulations. Update `.gitignore` only when file structure changes (e.g., new files like `combine_report_files.py`).

## 4. System Components
- **Ingestion**: Email dumps in `data/email_dumps/` (e.g., `glassdoor_email_1.txt`, `GoogleCareers_1.txt`, `LinkedInAlerts_1.txt`).
- **Processing**: `scripts/process_email_dumps.py` identifies source and parses data; `scripts/analyze_errors.py` for error recovery; `scripts/combine_glassdoor_emails.py` for merging Glassdoor files; `scripts/combine_report_files.py` for merging reports.
- **Storage**: JSON `data/rats_data.json` (replaced SQLite `rats_data.db`).
- **Output**: `data/parsed_jobs_output.txt` (no line limit), `data/parsed_jobs_output.html` (static table, sortable headers, dropdown checkbox filtering, optional pivot tables, Cyberpunk Monk palette), `logs/rats_data_report.txt`, `logs/parsed_jobs_report.txt`, `logs/parse_errors_report.txt`, `logs/error_recovery_report.txt`, `logs/combined_reports.txt`, planned notifications, dashboards, auto-apply hooks.
- **Integration**: Planned FastAPI, React/Tailwind, OpenAI/LangChain.

## 5. High-Level Workflow
- **Ingest**: Place .txt dumps in `data/email_dumps/`; merge Glassdoor files using `combine_glassdoor_emails.py`.
- **Identify Source**: Check copyright footer or sender email; abort if unknown.
- **Parse**: Extract headers/body, prioritize English titles and remote positions; enhanced parsing for GoogleCareers.
- **Store**: Save to JSON `rats_data.json`.
- **Match**: Planned AI matching.
- **Notify**: Planned alerts, Trello-style boards.
- **Monitor**: View `parsed_jobs_output.txt`, `parsed_jobs_output.html` (static table, sortable headers, dropdown checkbox filtering, optional pivot, Cyberpunk Monk palette), report files; run `analyze_errors.py` for error recovery; merge reports using `combine_report_files.py`; open `combined_reports.txt` in Notepad++ for analysis; planned dashboards.

## 6. Detailed Process Flows
### 6.1 Email Data Dump Processing
- **Input**: .txt files in `data/email_dumps/` with headers, body, copyright footer, or sender email.
- **Source Identification**: Scan copyright footer (e.g., "Copyright © ... Glassdoor LLC") or sender email; abort if unknown.
- **Parse**: Extract From, Subject, Date, job postings; prioritize English titles and remote positions; enhanced parsing for GoogleCareers.
- **Store**: Save to JSON `rats_data.json`.
- **Execution**: Run `python scripts/process_email_dumps.py`.
- **Output**: Print summary (1 line); generate `parsed_jobs_output.txt` (no line limit), `parsed_jobs_output.html` (static table, sortable headers, dropdown checkbox filtering, optional pivot tables, Cyberpunk Monk palette), `logs/rats_data_report.txt`, `logs/parsed_jobs_report.txt`, `logs/parse_errors_report.txt`; log data errors to `parse_errors.log`.
- **Error Recovery**: Run `python scripts/analyze_errors.py` to scan `parse_errors_report.txt`, `rats_data.json`, `parsed_jobs_output.txt`, and `parsed_jobs_output.html` and generate `error_recovery_report.txt`.

### 6.2 Version Control Compliance
- Increment version numbers for each sequence of changes to the modified file to ensure no overwriting and full traceability.
- Use Git with descriptive commits (e.g., "Fix JavaScript rendering in process_email_dumps.py").
- Update `.gitignore` only when file structure changes (e.g., new files like `combine_report_files.py`).
- **Critical Information**: Each sequence of changes requires changing the version number of the updated file; limit change logs to 5 entries.

## 7. Directory Structure
- `/data/`: `email_dumps/` (raw .txt: `glassdoor_email_1.txt`, `GoogleCareers_1.txt`, `LinkedInAlerts_1.txt`), `sample_jobs.json`, `rats_data.json`, `parsed_jobs_output.txt`, `parsed_jobs_output.html`.
- `/scripts/`: `process_email_dumps.py` (version 7.26), `analyze_errors.py` (version 1.18), `combine_glassdoor_emails.py` (version 1.0), `combine_report_files.py` (version 1.0).
- `/prompts/`: `job_matching_prompt.txt`.
- `/docs/`: `workflow.md` (version 1.40).
- `/logs/`: `parse_errors.log`, `rats_data_report.txt`, `parsed_jobs_report.txt`, `parse_errors_report.txt`, `error_recovery_report.txt`, `combined_reports.txt`.
- `.gitignore`: Excludes `data/email_dumps/`, `desktop.ini`, `Thumbs.db`.

## 8. Setup Instructions
- **Clone**: `git clone https://github.com/silicastormsiam/rats.git .`
- **Install**: Python 3.8+.
- **Add**: Email dumps to `data/email_dumps/`.
- **Run**: `cd /m/OneDrive/Documents/GitHub/RATS && python scripts/process_email_dumps.py`.
- **Error Recovery**: `cd /m/OneDrive/Documents/GitHub/RATS && python scripts/analyze_errors.py`.
- **Verify**: `cd /m/OneDrive/Documents/GitHub/RATS && start notepad++ data/parsed_jobs_output.txt`; `cd /m/OneDrive/Documents/GitHub/RATS && start data/parsed_jobs_output.html`; `cd /m/OneDrive\Documents\GitHub\RATS && start notepad++ logs/rats_data_report.txt`; `cd /m/OneDrive\Documents\GitHub\RATS && start notepad++ logs/parsed_jobs_report.txt`; `cd /m/OneDrive\Documents\GitHub\RATS && start notepad++ logs/parse_errors_report.txt`; `cd /m/OneDrive\Documents\GitHub\RATS && start notepad++ logs/error_recovery_report.txt`; `cd /m/OneDrive\Documents\GitHub\RATS && grep "ERROR\|WARNING" logs/parse_errors.log`.
- **Debug HTML**: Open `parsed_jobs_output.html` in a browser, check console for errors, and use "Toggle Debug JSON" button to view raw data.
- **Merge Reports**: Run `cd /m/OneDrive\Documents\GitHub\RATS && python scripts/combine_report_files.py`; open with `cd /m/OneDrive\Documents\GitHub\RATS && start notepad++ logs/combined_reports.txt`.
- **Backup**: Create timestamped backup with `tar -czf RATS_20250807_0802.tar.gz RATS` in Git Bash or `Compress-Archive -Path RATS -DestinationPath RATS_20250807_0802.zip` in PowerShell; verify with `ls -lh /m/OneDrive/Backups/RATS_20250807_0802.tar.gz` or `dir M:\OneDrive\Backups\RATS_20250807_0802.zip`.

## 9. Issues and Resolutions
- **SQLite Access**: Fixed with absolute path and OneDrive pause; transitioned to JSON storage.
- **Malformed Headers**: Resolved by parsing headers from body, skipping Gmail text.
- **Source Identification**: Pivoted to copyright footer and sender email (e.g., "careers-noreply@google.com").
- **Version Control**: Ensured increments for updated files only; limited change logs to 5 entries; clarified `.gitignore` updates only for file structure changes.
- **RAM Overload**: Reduced console output to 1 line; removed line limits for txt/json outputs; optimized HTML rendering.
- **Regression in Versions 2.8–3.7**: Overly restrictive parsing led to "Unknown" values; resurrected with JSON storage.
- **Non-English Characters**: Excluded Vietnam from Google Careers alerts; prioritized English-only titles.
- **Syntax Error**: Fixed in version 7.0 by removing Markdown code blocks; fixed in version 7.9 for HTML fallback table syntax; enhanced in version 7.10 with encoding checks; fixed in version 7.18 with syntax correction; fixed in version 7.21 with list-based HTML; fixed in version 7.25 for IndentationError.
- **'remote' Key Error**: Fixed in version 7.1 with `.get('remote', False)`.
- **HTML Output**: Added `parsed_jobs_output.html` with sorting/filtering in version 7.2; added pivot tables in version 7.3; fixed data rendering in version 7.4; applied Cyberpunk Monk palette in version 7.6; fixed data population with embedded JSON in version 7.7; added fallback table and JSON validation in version 7.8; fixed syntax in version 7.9; enhanced JSON validation and fallback table in version 7.10; added debug mode and extensive logging in version 7.11; pivoted to static HTML table in version 7.12; enhanced GoogleCareers parsing, fixed sorting, and added dropdown checkbox filtering in version 7.13; added combine_glassdoor_emails.py and enhanced parsing in version 7.14; added combine_report_files.py and ensured reliable filtering in version 7.15; updated CLI for Notepad++ and enhanced parsing in version 7.16; fixed syntax error and enhanced parsing in version 7.17; pivoted to Select2 library for dropdown checkboxes in version 7.18; pivoted to Chosen library for improved multi-select checkboxes in version 7.19; fixed unterminated f-string literal and pivoted to custom vanilla JavaScript for reliable multi-select checkboxes in version 7.20; fixed unterminated f-string literal with list-based HTML output and enhanced vanilla JavaScript dropdowns in version 7.21; removed redundant File dropdown and added Remote dropdown filter in version 7.22; fixed 'pos' keyword error, removed File column, added footer note with script version, restored all job postings with deduplication in version 7.23; fixed limited data issue by improving section parsing and deduplication in version 7.24; removed deduplication to restore all data in version 7.25; fixed JavaScript rendering to display all data in version 7.26; added backup options for zip failure in version 7.26; verified tar backup success in version 1.38; clarified PowerShell backup in version 1.39; confirmed tar and PowerShell backup success in version 1.40.
- **Large Files**: Resolved with `start notepad++` for viewing; added `analyze_errors.py` for Grok analysis; added `combine_report_files.py` for merging reports.
- **GoogleCareers Data**: Enhanced parsing in version 7.13 with broader regex and fallback parsing; further enhanced in version 7.26.
- **Backup Failure**: Added `tar` and PowerShell options for timestamped backups in version 1.37; verified `tar` success and corrected PowerShell commands in version 1.38; clarified PowerShell terminal usage in version 1.39; confirmed tar and PowerShell backup success in version 1.40.

## 10. Project Files and Sync Details
- **Local Path**: `M:\OneDrive\Documents\GitHub\RATS`
- **GitHub Repo**: `https://github.com/silicastormsiam/rats`
- **Files/Folders**: `LICENSE`, `README.md`, `.gitignore`, `data/` (`email_dumps/`, `sample_jobs.json`, `rats_data.json`, `parsed_jobs_output.txt`, `parsed_jobs_output.html`), `docs/` (`workflow.md`), `prompts/` (`job_matching_prompt.txt`), `scripts/` (`process_email_dumps.py`, `analyze_errors.py`, `combine_glassdoor_emails.py`, `combine_report_files.py`), `logs/` (`parse_errors.log`, `rats_data_report.txt`, `parsed_jobs_report.txt`, `parse_errors_report.txt`, `error_recovery_report.txt`, `combined_reports.txt`).
- **Last Sync**: 2025-08-07, 08:02 AM +07. Verify in OneDrive tray after resume.

## 11. Next Steps
- API/RSS aggregation.
- OpenAI/LangChain AI matching.
- FastAPI backend.
- React/Tailwind frontend for recruitment dashboard.
- Enhance HTML pivot table with additional aggregation options.

## 12. Reminder
Resume OneDrive syncing after Git operations and testing to back up changes.

## 13. Andrew Guru Teaching
- **Never assume, always verify**: Confirm details (e.g., file contents, file paths, patterns) before taking action.
- **Never provide snippets of script code**: Provide complete files for clarity.
- **Do not repeat anything that is already confirmed and verified**: Avoid redundant information.
- **Too much script output kills RAM**: Limit console output (e.g., to 1 line) to prevent browser crashes.
- **Version control**: Each sequence of changes requires changing the version number of the updated file; limited change logs to 5 entries; clarified `.gitignore` updates only for file structure changes.
- **Pause OneDrive syncing before Git operations**: Prevent .git corruption via system tray pause.
- **Save all files using Notepad++**: Use for editing and saving all files.
- **No GitHub updates until requested**: Do not commit or push until instructed.
- **Stop sending messages about saving with nano or Git notes**: Use Notepad++ and avoid Git notes.
- **Pivot and find a new method when previous methods fail**: Shift approaches (e.g., from regex to line-based parsing) to detect clear elements.

## 14. Logging
- Restricted to data errors per run.

## 15. Output Limits
- Removed for `parsed_jobs_output.txt`, `rats_data.json`, and `parse_errors.log`.

## 16. Change Log
- Limited to five entries.

## 17. Console Output
- Minimal, meeting section 13 requirements.

## 18. GitHub
- No commits until requested (section 13).

## 19. Non-English Characters
- Version 7.26 ensures English-only positions; Google Careers adjustment prevents Vietnamese characters.

## 20. Database
- No tables; JSON storage exclusive.