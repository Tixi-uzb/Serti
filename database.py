import sqlite3
import datetime
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, 'bot_database.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            phone TEXT,
            profession TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            serial_number TEXT UNIQUE,
            profession TEXT,
            created_at TIMESTAMP,
            file_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, username, created_at) VALUES (?, ?, ?)',
              (user_id, username, datetime.datetime.now()))
    conn.commit()
    conn.close()

def update_user_info(user_id, **kwargs):
    conn = get_connection()
    c = conn.cursor()
    for key, value in kwargs.items():
        c.execute(f'UPDATE users SET {key} = ? WHERE user_id = ?', (value, user_id))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def create_certificate_record(user_id, serial_number, profession, file_path):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO certificates (user_id, serial_number, profession, created_at, file_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, serial_number, profession, datetime.datetime.now(), file_path))
    conn.commit()
    conn.close()

def get_certificate(serial_number):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT certificates.*, users.full_name 
        FROM certificates 
        JOIN users ON certificates.user_id = users.user_id 
        WHERE serial_number = ?
    ''', (serial_number,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None
