import sqlite3
import os
import sys

def get_base_dir():
    """Determines the correct base directory whether running as a script or a PyInstaller exe."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(__file__))

DB_DIR = os.path.join(get_base_dir(), 'database')
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DATABASE_PATH = os.path.join(DB_DIR, 'life_os.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
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