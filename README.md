# README


### Access DB information

- Option 1: Built-in SQLite Shell via Terminal

1. Access DB information - `sqlite3 expense_tracker.db`
2. Available Commands
    - .tables
    - .schema
        - .schema expenses
            - SELECT * FROM expenses;
        - .schema categories
        - .schema users

- Option 2: GUI Viewer

1. Install `brew install --cask db-browser-for-sqlite`
2. Open `DB Browser for SQLite
3. From Top Bar > File > Open Database > expense_tracker.db

### Adding Seed Data 

- Execute '/scripts/seed_data.py'

Notes:

- Turn on foreign key enforcement in SQLite. 

By default, SQLite ignores foreign key constraints (Unlike Postgres or MySQL). Basically in the event of deleting a user or category, this prevents SQLite from allowing `orphan` expense rows.

`conn.execute("PRAGMA foreign_keys = ON;")` 

On failture, Integrity Error is generated.

`sqlite3.IntegrityError: FOREIGN KEY constraint failed` 

- Why use SQLite instead of PostgreSQL or MySQL? This is because PostgresSQL and MySQL requires server databases. Meaning the system needs a running a background server process, configured users, passwords, ports and roles. This is designed for multi-user, concurrent, networked use. So SQLite is perfect for practice + local dev. PostSQL is perfect for "production + multi-user app.

- When adding a sample data with the following command, SQLite expects a tuple. Because of this, user_info.name expects a comma after user_info otherwise SQLite will iterate through each character in user_info.name

    """
    conn.execute(
        "INSERT OR IGNORE INTO users (name) VALUES (?)",
        (user_info.name, )
    )
    """
