import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('DB_PATH')

def init():
  ##
  with sqlite3.connect(db_path) as con:
    cur = con.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS kunder (
      cpr integer [primary key]  
      navn string 
      tlf string 
      email string
      adresse string 
    ''')
  con.commit()