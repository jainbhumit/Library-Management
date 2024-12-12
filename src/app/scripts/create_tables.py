import sqlite3
import src.app.config.config as config

conn = sqlite3.connect(config.DB_ADDR)
conn.execute("PRAGMA foreign_keys = ON;")

with conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user (
        id TEXT PRIMARY KEY, 
        name TEXT NOT NULL, 
        role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
        year TEXT NOT NULL,
        branch TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS book (
        id TEXT PRIMARY KEY,
        title TEXT UNIQUE NOT NULL,                  
        author TEXT NOT NULL,                 
        number_of_copies INTEGER NOT NULL,    
        number_of_available_books INTEGER NOT NULL 
    );
    ''')

    conn.execute('''
       CREATE TABLE IF NOT EXISTS issuedBook (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,           
        book_id TEXT NOT NULL,            
        borrow_date DATE NOT NULL,            
        return_date DATE,                  
        FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
        FOREIGN KEY (book_id) REFERENCES book (id) ON DELETE CASCADE
    );
    ''')

