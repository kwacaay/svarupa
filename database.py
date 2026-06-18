import sqlite3

conn = sqlite3.connect("svarupa.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
               )
""")

conn.commit()
conn.close()

print("Database berhasil dibuat")