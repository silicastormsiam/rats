---
# Metadata
File Name: workflow.md
Owner: silicastormsiam
Purpose: Comprehensive handover for R.A.T.S. project, detailing introduction, objectives, workflow, version control, source identification, and troubleshooting for a new project manager.
Version Control: 1.1
Change Log:
  - 2025-08-05: Initial creation with project overview, workflow, and lessons learned.
  - 2025-08-05: Updated to 1.1, added detailed source configuration, RAM optimization lessons, and expanded issue resolutions.

---

# R.A.T.S. Workflow and Project Handover Document

## 0. Preliminary Note
    Pause OneDrive syncing before Git operations (e.g., 2025-08-05, 08:10 PM +07, 2-hour pause) via system tray to prevent `.git` corruption. Resume after.

## 1. Introduction to the Project
    The Recruitment Alerts Tracking System (R.A.T.S.) is an AI-powered tool designed to streamline job alert email management for job seekers. It aggregates alerts from platforms like Glassdoor (currently implemented) and plans for LinkedIn, Indeed, and nine others (12 sources total), extracting details into a SQLite database for retrieval and analysis. Built with Python for backend processing, it includes plans for FastAPI backend, React/Tailwind frontend, and OpenAI/LangChain for AI keyword matching. Hosted locally on the ROG-STRIX-B550F at `M:\OneDrive\Documents\GitHub\RATS`, it syncs to GitHub for version control, adhering to compliance by incrementing version numbers.

    ### 1.1 Purpose of Handover
        This document equips a new project manager with all setup, workflow, and lessons learned (e.g., pivoting source identification, RAM optimization) to ensure seamless development for real-time, AI-driven job search features.

    ### 1.2 Development Context
        Iterative development addressed malformed email headers, database access, and RAM issues. Key lessons include strict version control, reducing output to prevent browser crashes, and pivoting to copyright footer for source identification, as taught by Andrew.

## 2. Project Objectives
    R.A.T.S. automates and personalizes job alert management. Objectives:
    - **Automation**: Parse email dumps, store in SQLite.
    - **Source Identification**: Detect sources (Glassdoor via copyright footer), supporting 12 sources without 'Unknown'.
    - **Compliance**: Increment version numbers for traceability per government regulations.
    - **AI Integration**: Match alerts to preferences using OpenAI/LangChain.
    - **User Experience**: Notifications, dashboards, auto-apply features.
    - **Scalability**: API/RSS feeds, browser extensions, Trello-style boards.
    - **Data Security**: Exclude sensitive data via `.gitignore`.

## 3. Metadata Requirements
    - **Scope**: Scripts (`.py`) and documentation (`.md`) require metadata; data dumps (`.txt`) are raw.
    - **Format**: File Name, Owner (silicastormsiam), Purpose, Version Control, Change Log.
    - **Compliance**: Increment versions for updates; no overwriting without increment.

## 4. System Components
    - **Ingestion**: Email dumps in `data/email_dumps/` (e.g., `example_email.txt`).
    - **Processing**: `scripts/process_email_dumps.py` identifies source via copyright footer.
    - **Storage**: SQLite `data/rats_data.db` (table: `email_dumps`).
    - **Output**: Planned notifications, dashboards, auto-apply hooks.
    - **Integration**: Future FastAPI, React/Tailwind, OpenAI/LangChain.

## 5. High-Level Workflow
    1. Ingest: Place `.txt` dumps in `data/email_dumps/`.
    2. Identify Source: Check copyright footer (e.g., "Copyright © ... Glassdoor LLC"); abort if unknown.
    3. Parse: Extract headers/body, handle Gmail interface text.
    4. Store: Save to SQLite with source.
    5. Match: Future AI matching.
    6. Notify: Planned alerts, Trello-style boards.
    7. Monitor: Planned dashboards.

## 6. Detailed Process Flows
    ### 6.1 Email Data Dump Processing
        - **Input**: `.txt` files in `data/email_dumps/` with headers, body, copyright footer.
        - **Source Identification**: Scan copyright footer (e.g., Glassdoor); abort if unknown, supporting 12 sources.
        - **Parse**: Extract From, Subject, Date from body if headers missing.
        - **Store**: Save to SQLite `email_dumps` table.
        - **Execution**: Run `python scripts/process_email_dumps.py`.
        - **Output**: Print sender, subject, source; save to database.
        - **Lesson**: Pivoted from sender-based to copyright footer identification, as taught by Andrew.

    ### 6.2 Version Control Compliance
        - Increment version numbers (e.g., 1.7 to 1.8).
        - Use Git with descriptive commits (e.g., "Update process_email_dumps.py with copyright source").
        - Ensures traceability for government regulations, as taught by Andrew.

    ### 6.3 Sources of Email
        - **Current Sources**: Glassdoor (via "Copyright © ... Glassdoor LLC").
        - **Configuration Requirements**:
            - **Glassdoor**: Pattern: r'Copyright.*Glassdoor LLC'.
            - **LinkedIn**: Future; pattern: r'Copyright.*LinkedIn'.
            - **Indeed**: Future; pattern: r'Copyright.*Indeed'.
            - **Monster**: Future; pattern: r'Copyright.*Monster'.
            - **CareerBuilder**: Future; pattern: r'Copyright.*CareerBuilder'.
            - **Dice**: Future; pattern: r'Copyright.*Dice'.
            - **ZipRecruiter**: Future; pattern: r'Copyright.*ZipRecruiter'.
            - **SimplyHired**: Future; pattern: r'Copyright.*SimplyHired'.
            - **Craigslist**: Future; pattern: r'Copyright.*Craigslist'.
            - **USAJobs**: Future; pattern: r'Copyright.*USAJobs'.
            - **Reed**: Future; pattern: r'Copyright.*Reed'.
            - **Totaljobs**: Future; pattern: r'Copyright.*Totaljobs'.
        - **Expansion**: Add patterns to SOURCES dictionary in `process_email_dumps.py`.

## 7. Directory Structure
    - `/data/`: `email_dumps/` (raw `.txt`: `example_email.txt`, `glassdoor_email_2.txt`, `glassdoor_email_3.txt`, `glassdoor_email_4.txt`), `sample_jobs.json`, `rats_data.db`.
    - `/scripts/`: `process_email_dumps.py` (version 1.8).
    - `/prompts/`: `job_matching_prompt.txt`.
    - `/docs/`: `workflow.md` (version 1.1).
    - `.gitignore`: Excludes `data/email_dumps/`, `data/rats_data.db`, `desktop.ini`, `Thumbs.db`.

## 8. Setup Instructions
    1. Clone: `git clone https://github.com/silicastormsiam/rats.git .`
    2. Install: Python 3.8+, SQLite tools[](https://www.sqlite.org/download.html).
    3. Add email dumps to `data/email_dumps/`.
    4. Run: `cd scripts && python process_email_dumps.py`.
    5. Verify: `sqlite3 data/rats_data.db "SELECT * FROM email_dumps;"`.

## 9. Issues and Resolutions
    - **SQLite Access**: Fixed with absolute path and OneDrive pause.
    - **Malformed Headers**: Resolved by parsing headers from body, skipping Gmail text.
    - **Source Identification**: Pivoted to copyright footer (e.g., "Copyright © ... Glassdoor LLC"), as taught by Andrew.
    - **Version Control**: Ensured increments for compliance, as taught by Andrew.
    - **RAM Overload**: Reduced output to 15 lines max to prevent browser crashes, as taught by Andrew.

## 10. Project Files and Sync Details
    - **Local Path**: `M:\OneDrive\Documents\GitHub\RATS`
    - **GitHub Repo**: https://github.com/silicastormsiam/rats
    - **Files/Folders**: LICENSE, README.md, .gitignore, data/ (email_dumps/, sample_jobs.json, rats_data.db), docs/ (workflow.md), prompts/ (job_matching_prompt.txt), scripts/ (process_email_dumps.py).
    - **Last Sync**: 2025-08-05, 08:10 PM +07. Verify in OneDrive tray after resume.

## 11. Next Steps
    - API/RSS aggregation.
    - OpenAI/LangChain AI matching.
    - FastAPI backend.
    - React/Tailwind frontend.

## 12. Reminder
    Resume OneDrive syncing after Git operations and testing to back up changes.