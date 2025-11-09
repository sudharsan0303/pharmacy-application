import sqlite3
import os

# Get the absolute path to the database folder
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'user.db')

def create_user_connection():
    """Create a connection to the SQLite database for users."""
    return sqlite3.connect(DATABASE_PATH)

def create_user_db():
    """Create the users table in the database."""
    conn = create_user_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_user_db()
    print(f"Database created at {DATABASE_PATH}")