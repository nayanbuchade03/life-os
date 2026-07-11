import sqlite3
import os

DB_DIR = os.path.dirname(__file__)
SCHEMA_PATH = os.path.join(DB_DIR, 'schema.sql')
DB_PATH = os.path.join(DB_DIR, 'life_os.db')

def init_db():
    print(f"Initializing database at {DB_PATH}...")
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, 'r') as f:
            schema_script = f.read()
            conn.executescript(schema_script)
            
    print("Database initialization complete.")

if __name__ == '__main__':
    init_db()