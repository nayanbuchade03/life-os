import sqlite3
import os
import sys

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(__file__))

DB_DIR = os.path.join(get_base_dir(), 'database')
os.makedirs(DB_DIR, exist_ok=True)
DATABASE_PATH = os.path.join(DB_DIR, 'life_os.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY CHECK (id = 1), theme TEXT DEFAULT 'dark', notifications_enabled INTEGER DEFAULT 1, last_backup_date TEXT);
INSERT OR IGNORE INTO settings (id, theme, notifications_enabled) VALUES (1, 'dark', 1);

CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT, category TEXT, priority TEXT, frequency TEXT, start_date TEXT NOT NULL, end_date TEXT, reminder_time TEXT, estimated_time INTEGER, is_active INTEGER DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS task_completions (id INTEGER PRIMARY KEY AUTOINCREMENT, task_id INTEGER NOT NULL, completion_date TEXT NOT NULL, status TEXT DEFAULT 'Completed', notes TEXT, FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS quarterly_goals (id INTEGER PRIMARY KEY AUTOINCREMENT, quarter TEXT NOT NULL, title TEXT NOT NULL, description TEXT, target_date TEXT, status TEXT DEFAULT 'Not Started', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS dsa_problems (id INTEGER PRIMARY KEY AUTOINCREMENT, problem_name TEXT NOT NULL, platform TEXT, difficulty TEXT, topic TEXT, link TEXT, date_solved TEXT NOT NULL, time_taken INTEGER, mistakes TEXT, confidence_level INTEGER, need_revision INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS dsa_revisions (id INTEGER PRIMARY KEY AUTOINCREMENT, problem_id INTEGER NOT NULL, revision_date TEXT NOT NULL, stage TEXT, status TEXT DEFAULT 'Pending', FOREIGN KEY(problem_id) REFERENCES dsa_problems(id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS job_applications (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT NOT NULL, role TEXT NOT NULL, location TEXT, salary TEXT, source TEXT, job_link TEXT, resume_version TEXT, date_applied TEXT NOT NULL, current_status TEXT DEFAULT 'Wishlist', notes TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS follow_ups (id INTEGER PRIMARY KEY AUTOINCREMENT, application_id INTEGER NOT NULL, follow_up_date TEXT NOT NULL, reminder_time TEXT, is_completed INTEGER DEFAULT 0, notes TEXT, FOREIGN KEY(application_id) REFERENCES job_applications(id) ON DELETE CASCADE);
"""

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    conn.executescript(SCHEMA)
    return conn

def execute_query(query, args=(), commit=False, fetchone=False):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        
        if commit:
            conn.commit()
            return cursor.lastrowid
            
        if fetchone:
            return cursor.fetchone()
            
        return cursor.fetchall()