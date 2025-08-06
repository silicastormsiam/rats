# R.A.T.S. Workflow and Project Handover Document
## Metadata
- **File Name**: workflow.md
- **Owner**: silicastormsiam
- **Purpose**: Comprehensive handover for R.A.T.S. project, detailing introduction, objectives, workflow, version control, source identification, troubleshooting, critical guidance from Andrew, and project shutdown/resurrection details.
- **Version Control**: 1.10
- **Change Log**:
  - 2025-08-06: Updated to 1.6, project resurrected; transitioned storage from SQLite to JSON (rats_data.json); added parsed_jobs_output.txt for user-friendly output; enhanced parsing for English-only titles and remote positions; limited change logs to 5 entries; updated logging to data errors only per run; added support for LinkedInAlerts_1.txt; restricted console output; ensured metadata compliance across files.
  - 2025-08-06: Updated to 1.7, fixed syntax error in process_email_dumps.py; added 15-line limit for rats_data.json viewing; fixed 'remote' key error; documented logging/output enhancements; updated .gitignore to version 1.4; retained change log restriction and metadata compliance.
  - 2025-08-06: Updated to 1.8, added parsed_jobs_output.html for browser-friendly output; fixed 'remote' key error; documented HTML output addition; updated .gitignore to version 1.5; retained 15-line txt output limit, data error logging, and metadata compliance.
  - 2025-08-06: Updated to 1.9, added sorting/filtering to parsed_jobs_output.html; updated .gitignore to version 1.6; retained 15-line txt/json output limits, data error logging, English-only title prioritization, Remote prioritization, and metadata compliance.
  - 2025-08-06: Updated to 1.10, documented HTML output with ability to use pivot tables and filter data; updated .gitignore to version 1.7; retained all prior enhancements and metadata compliance.

## 0. Preliminary Note
Pause OneDrive syncing before Git operations (e.g., 2025-08-06, 07:49 PM +07, 7-hour pause) via system tray to prevent .git corruption. Resume after.

## 1. Introduction to the Project
The Recruitment Alerts Tracking System (R.A.T.S.) is an AI-powered tool designed to streamline job alert email management for job seekers. It aggregates alerts from platforms like Glassdoor, LinkedIn, and planned sources (12 total), extracting details into JSON for retrieval and analysis. Built with Python for backend processing, it includes plans for FastAPI backend, React/Tailwind frontend, and OpenAI/LangChain for AI keyword matching. Hosted locally on the ROG-STRIX-B550F at `M:\OneDrive\Documents\GitHub\RATS`, it syncs to GitHub for version control, adhering to compliance by incrementing version numbers.

### 1.1 Purpose of Handover
This document equips a new project manager with setup, workflow, and lessons learned (e.g., pivoting source identification, RAM optimization) to ensure seamless development for real-time, AI-driven job search features. The project was shut down due to regressions but resurrected with JSON storage and enhanced output/logging.

### 1.2 Development Context
Iterative development addressed malformed email headers, database access, and RAM issues. Version 2.7 of `process_email_dumps.py` was functional before shutdown. Resurrection updates (versions 5.0–7.2) transitioned to JSON storage (`rats_data.json`), added `parsed_jobs_output.txt` and `parsed_jobs_output.html` with sorting/filtering (including pivot table-like functionality for data aggregation), prioritized English-only titles and remote positions, limited console output to 15 lines, restricted logging to data errors per run, and fixed syntax/key errors.

## 2. Project Objectives
- **Automation**: Parse email dumps, store in JSON (`rats_data.json`).
- **Source Identification**: Detect sources (Glassdoor via copyright footer, GoogleCareers/LinkedIn via sender/content), supporting 12 sources without 'Unknown'.
- **Compliance**: Increment version numbers for traceability; limit change logs to 5 entries.
- **AI Integration**: Match alerts to preferences using OpenAI/LangChain.
- **User Experience**: Notifications, dashboards, auto-apply features; user-friendly `parsed_jobs_output.txt` and `parsed_jobs_output.html` with sorting/filtering/pivot tables.
- **Scalability**: API/RSS feeds, browser extensions, Trello-style boards.
- **Data Security**: Exclude sensitive data via `.gitignore`.

## 3. Metadata Requirements
- **Scope**: Scripts (.py) and documentation (.md) require metadata; data dumps (.txt) are raw.
- **Format**: File Name, Owner (silicastormsiam), Purpose, Version Control, Change Log (max 5 entries).
- **Compliance**: Increment versions for updates; no overwriting without increment. Each sequence of changes requires changing the version number to maintain traceability and adhere to government regulations.

## 4. System Components
- **Ingestion**: Email dumps in `data/email_dumps/` (e.g., `glassdoor_email_1.txt`, `GoogleCareers_1.txt`, `LinkedInAlerts_1.txt`).
- **Processing**: `scripts/process_email_dumps.py` identifies source via copyright footer or sender email.
- **Storage**: JSON `data/rats_data.json` (replaced SQLite `rats_data.db`).
- **Output**: `data/parsed_jobs_output.txt` (15-line limit), `data/parsed_jobs_output.html` (sortable/filterable with pivot table functionality), planned notifications, dashboards, auto-apply hooks.
- **Integration**: Planned FastAPI, React/Tailwind, OpenAI/LangChain.

## 5. High-Level Workflow
- **Ingest**: Place .txt dumps in `data/email_dumps/`.
- **Identify Source**: Check copyright footer or sender email; abort if unknown.
- **Parse**: Extract headers/body, prioritize English titles and remote positions.
- **Store**: Save to JSON `rats_data.json`.
- **Match**: Planned AI matching.
- **Notify**: Planned alerts, Trello-style boards.
- **Monitor**: View `parsed_jobs_output.txt` (15-line limit) or `parsed_jobs_output.html` (sort/filter/pivot); planned dashboards.

## 6. Detailed Process Flows
### 6.1 Email Data Dump Processing
- **Input**: .txt files in `data/email_dumps/` with headers, body, copyright footer, or sender email.
- **Source Identification**: Scan copyright footer (e.g., "Copyright © ... Glassdoor LLC") or sender email; abort if unknown.
- **Parse**: Extract From, Subject, Date, job postings; prioritize English titles and remote positions.
- **Store**: Save to JSON `rats_data.json`.
- **Execution**: Run `python scripts/process_email_dumps.py`.
- **Output**: Print summary (1 line); generate `parsed_jobs_output.txt` (15-line limit) and `parsed_jobs_output.html` (sortable/filterable/pivot table); log data errors to `parse_errors.log`.

### 6.2 Version Control Compliance
- Increment version numbers for each sequence of changes to ensure no overwriting and full traceability.
- Use Git with descriptive commits (e.g., "Update process_email_dumps.py with HTML sorting/filtering").
- **Critical Information**: Each sequence of changes requires changing the version number; limit change logs to 5 entries.

## 7. Directory Structure
- `/data/`: `email_dumps/` (raw .txt: `glassdoor_email_1.txt`, `glassdoor_email_2.txt`, `glassdoor_email_3.txt`, `glassdoor_email_4.txt`, `GoogleCareers_1.txt`, `LinkedInAlerts_1.txt`), `sample_jobs.json`, `rats_data.json`, `parsed_jobs_output.txt`, `parsed_jobs_output.html`.
- `/scripts/`: `process_email_dumps.py` (version 7.2).
- `/prompts/`: `job_matching_prompt.txt`.
- `/docs/`: `workflow.md` (version 1.10).
- `/logs/`: `parse_errors.log`.
- `.gitignore`: Excludes `data/email_dumps/`, `desktop.ini`, `Thumbs.db`.

## 8. Setup Instructions
- **Clone**: `git clone https://github.com/silicastormsiam/rats.git .`
- **Install**: Python 3.8+.
- **Add**: Email dumps to `data/email_dumps/`.
- **Run**: `cd /m/OneDrive/Documents/GitHub/RATS && python scripts/process_email_dumps.py`.
- **Verify**: `head -n 15 data/parsed_jobs_output.txt`; `start data/parsed_jobs_output.html`; `grep "ERROR\|WARNING" logs/parse_errors.log`.

## 9. Issues and Resolutions
- **SQLite Access**: Fixed with absolute path and OneDrive pause; transitioned to JSON storage.
- **Malformed Headers**: Resolved by parsing headers from body, skipping Gmail text.
- **Source Identification**: Pivoted to copyright footer and sender email (e.g., "careers-noreply@google.com").
- **Version Control**: Ensured increments; limited change logs to 5 entries.
- **RAM Overload**: Reduced output to 1 line; limited txt/json output to 15 lines.
- **Regression in Versions 2.8–3.7**: Overly restrictive parsing led to "Unknown" values; resurrected with JSON storage.
- **Non-English Characters**: Excluded Vietnam from Google Careers alerts; prioritized English-only titles.
- **Syntax Error**: Fixed in version 7.0 by removing Markdown code blocks.
- **'remote' Key Error**: Fixed in version 7.1 with `.get('remote', False)`.
- **HTML Output**: Added `parsed_jobs_output.html` with sorting/filtering in version 7.2; enhanced with pivot table functionality for data aggregation.

## 10. Project Files and Sync Details
- **Local Path**: `M:\OneDrive\Documents\GitHub\RATS`
- **GitHub Repo**: `https://github.com/silicastormsiam/rats`
- **Files/Folders**: `LICENSE`, `README.md`, `.gitignore`, `data/` (`email_dumps/`, `sample_jobs.json`, `rats_data.json`, `parsed_jobs_output.txt`, `parsed_jobs_output.html`), `docs/` (`workflow.md`), `prompts/` (`job_matching_prompt.txt`), `scripts/` (`process_email_dumps.py`), `logs/` (`parse_errors.log`).
- **Last Sync**: 2025-08-06, 07:49 PM +07. Verify in OneDrive tray after resume.

## 11. Next Steps
- API/RSS aggregation.
- OpenAI/LangChain AI matching.
- FastAPI backend.
- React/Tailwind frontend.
- Enhance HTML output with advanced pivot table features.

## 12. Reminder
Resume OneDrive syncing after Git operations and testing to back up changes.

## 13. Andrew Guru Teaching
- **Never assume, always verify**: Confirm details (e.g., file contents, paths, patterns) before taking action.
- **Never provide snippets of script code**: Provide complete files for clarity.
- **Do not repeat anything that is already confirmed and verified**: Avoid redundant information.
- **Too much script output kills RAM**: Limit output (e.g., to 15 lines) to prevent browser crashes.
- **Version control**: Each sequence of changes requires changing the version number for traceability.
- **Pause OneDrive syncing before Git operations**: Prevent .git corruption via system tray pause.
- **Save all files using Notepad++**: Use for editing and saving all files.
- **No GitHub updates until requested**: Do not commit or push until instructed.
- **Stop sending messages about saving with nano or Git notes**: Use Notepad++ and avoid Git notes.
- **Pivot and find a new method when previous methods fail**: Shift approaches (e.g., from regex to line-based parsing) to detect clear elements.