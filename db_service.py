import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('DB_PATH')

def init():
    with sqlite3.connect(db_path) as conn:
      c = conn.cursor()
      c.execute('''CREATE TABLE IF NOT EXISTS users (
                cpr INTEGER PRIMARY KEY, 
                navn TEXT, 
                tlf TEXT,
                email TEXT,
                adresse TEXT)
            ''')
      
    conn.commit()
    