import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('database/data.db')
    cursor = conn.cursor()

    # Create users table with hashed password storage
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        preferences TEXT,
        language TEXT DEFAULT 'en'
    )
    ''')

    # Create attractions table with latitude and longitude for location
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attractions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT,
        latitude REAL,
        longitude REAL,
        rating REAL CHECK(rating >= 1 AND rating <= 5),
        price REAL,
        opening_hours TEXT
    )
    ''')

    # Create reviews table with rating constraint
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attraction_id INTEGER,
        user_id INTEGER,
        review TEXT,
        rating REAL CHECK(rating >= 1 AND rating <= 5),
        FOREIGN KEY(attraction_id) REFERENCES attractions(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

# Initialize the database
init_db()
