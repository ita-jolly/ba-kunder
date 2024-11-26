import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('DB_PATH')

def init():
  ##
  def init():
    """Initialize the guests table if it doesn't exist."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE HERE
        ''')
