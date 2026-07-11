import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'life_os.db')

def get_db_connection():
    """Establishes and returns a database connection with dictionary-like rows."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def execute_query(query, args=(), commit=False, fetchone=False):
    """Utility function to execute a query and return results."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        
        if commit:
            conn.commit()
            return cursor.lastrowid
            
        if fetchone:
            return cursor.fetchone()
            
        return cursor.fetchall()