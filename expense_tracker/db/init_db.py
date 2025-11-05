'''
We can run init_db.py instead of calling/running 
sqlite3 expense_tracker.db ".read db/schema.sql
'''
import sqlite3
from pathlib import Path

# Define where the DB file will live (in project root)
DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"

def init_db():
    # Connect to the SQLite DB (creates the file if it doens't exists)
    conn = sqlite3.connect(DB_PATH)

    # Read all SQL statements froms schema.sql
    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, "r") as f:
        schema_sql = f.read()
    
    # Execute all the CREATE TABLE commands at once, save changes and close connection
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

    print(f"✅ Database initialized successfully at {DB_PATH}")

if __name__ == '__main__':
    init_db()