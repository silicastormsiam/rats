# File Name: process_email_dumps.py
# Owner: silicastormsiam
# Purpose: Processes raw email data dumps to store job alerts in SQLite for R.A.T.S., with source identification from copyright footer.
# Version Control: 1.9
# Change Log:
#   - 2025-08-05: Initial creation.
#   - 2025-08-05: Added absolute path, error handling.
#   - 2025-08-05: Added source identification, updated schema.
#   - 2025-08-05: Improved parsing for Gmail interface.
#   - 2025-08-05: Enhanced header extraction from body to fix 'Unknown' issue.

import sqlite3
import os
from datetime import datetime, timezone
import email
from email import policy
import re
import sys

SOURCES = {
    'glassdoor': r'Copyright.*Glassdoor LLC',
    'linkedin': r'Copyright.*LinkedIn',
    'indeed': r'Copyright.*Indeed',
    'monster': r'Copyright.*Monster',
    'careerbuilder': r'Copyright.*CareerBuilder',
    'dice': r'Copyright.*Dice',
    'ziprecruiter': r'Copyright.*ZipRecruiter',
    'simplyhired': r'Copyright.*SimplyHired',
    'craigslist': r'Copyright.*Craigslist',
    'usajobs': r'Copyright.*USAJobs',
    'reed': r'Copyright.*Reed',
    'totaljobs': r'Copyright.*Totaljobs'
}

def init_db():
    db_path = r'M:\OneDrive\Documents\GitHub\RATS\data\rats_data.db'
    try:
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS email_dumps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                received_date TEXT,
                sender TEXT,
                subject TEXT,
                body TEXT,
                source TEXT,
                processed INTEGER DEFAULT 0,
                created_at TEXT
            )
        ''')
        c.execute("PRAGMA table_info(email_dumps)")
        columns = [row[1] for row in c.fetchall()]
        if 'source' not in columns:
            c.execute("ALTER TABLE email_dumps ADD COLUMN source TEXT")
        conn.commit()
        return conn
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        sys.exit(1)

def clean_email_content(email_content):
    lines = email_content.splitlines()
    start_index = 0
    for i, line in enumerate(lines):
        if re.search(r'^(From:|Subject:|Date:)', line, re.I):
            start_index = i
            break
    return '\n'.join(lines[start_index:])

def extract_headers_from_body(body):
    sender = 'Unknown'
    subject = 'No Subject'
    date = datetime.now(timezone.utc).isoformat()
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if re.match(r'^From:.*<noreply@glassdoor\.com>', line, re.I):
            sender = line.split(':', 1)[1].strip()
        elif re.match(r'^Subject:.*Job alert:', line, re.I):
            subject = line.split(':', 1)[1].strip()
        elif re.match(r'^Date:', line, re.I):
            date = line.split(':', 1)[1].strip()
    return sender, subject, date

def identify_source(email_content):
    for source, pattern in SOURCES.items():
        if re.search(pattern, email_content, re.I):
            return source.capitalize()
    return None

def parse_email(email_content):
    source = identify_source(email_content)
    if not source:
        print("Aborting: Unknown source")
        sys.exit(1)
    cleaned_content = clean_email_content(email_content)
    msg = email.message_from_string(cleaned_content, policy=policy.default)
    sender = msg.get('From', 'Unknown')
    subject = msg.get('Subject', 'No Subject')
    received_date = msg.get('Date', datetime.now(timezone.utc).isoformat())
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    body = re.sub(r'\n\s*\n', '\n', body.strip())
    if sender == 'Unknown' or subject == 'No Subject':
        sender, subject, received_date = extract_headers_from_body(body)
    return {
        'sender': sender,
        'subject': subject,
        'received_date': received_date,
        'body': body,
        'source': source
    }

def save_to_db(conn, email_data):
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO email_dumps (received_date, sender, subject, body, source, processed, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            email_data['received_date'],
            email_data['sender'],
            email_data['subject'],
            email_data['body'],
            email_data['source'],
            0,
            datetime.now(timezone.utc).isoformat()
        ))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving to database: {e}")
        sys.exit(1)

def process_email_file(file_path, conn):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        email_content = f.read()
    email_data = parse_email(email_content)
    save_to_db(conn, email_data)
    print(f"Processed {os.path.basename(file_path)}: {email_data['sender']} | {email_data['subject']} | {email_data['source']}")

def main():
    conn = init_db()
    email_dir = 'data/email_dumps/'
    if not os.path.exists(email_dir):
        os.makedirs(email_dir)
    for filename in os.listdir(email_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(email_dir, filename)
            process_email_file(file_path, conn)
    conn.close()

if __name__ == "__main__":
    main()