import sqlite3
import os

# Get the absolute path to the database folder
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'medicine.db')

def create_medicine_connection():
    """Create a connection to the SQLite database for medicines."""
    print(f"Connecting to database at {DATABASE_PATH}")
    return sqlite3.connect(DATABASE_PATH)

def create_medicine_db():
    """Create the medicines table in the database."""
    conn = create_medicine_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            picture TEXT NOT NULL,
            price REAL NOT NULL,
            availability TEXT NOT NULL DEFAULT 'NO' CHECK (availability IN ('YES', 'NO'))
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_medicine_db()
    print(f"Medicine database created at {DATABASE_PATH}")