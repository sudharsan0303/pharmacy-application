import sqlite3
import os
from datetime import datetime

# Get the absolute path to the database folder
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'order.db')

def create_order_connection():
    """Create a connection to the SQLite database for orders."""
    return sqlite3.connect(DATABASE_PATH)

def create_order_db():
    """Create the orders table in the database."""
    conn = create_order_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            medicine_name TEXT NOT NULL,
            full_name TEXT NOT NULL,  -- Added full_name column
            phone TEXT NOT NULL,      -- Added phone column
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (medicine_id) REFERENCES medicines (id)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_order_db()
    print(f"Order database created at {DATABASE_PATH}")