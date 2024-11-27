import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('DB_PATH')

def init():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS kunder (
                cpr INTEGER PRIMARY KEY,
                navn TEXT,
                tlf TEXT,
                email TEXT,
                adresse TEXT)
            ''')

        cur.execute('SELECT COUNT(*) FROM kunder')
        row_count = cur.fetchone()[0]

        if row_count == 0:
            cur.execute(''' INSERT INTO kunder (cpr, navn, tlf, email, adresse)
                        VALUES (1234567890, 'Test Testesen', '12345678', 'test@testmail.dk', 'Testvej 1')
                        ''')

    conn.commit()

def get_kunder():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM kunder')
        rows = cur.fetchall()

        alle_kunder = [{'cpr': row[0], 'navn': row[1], 'tlf': row[2], 'email': row[3], 'adresse': row[4]} for row in rows]
        if len(alle_kunder) == 0:
            return None

        return alle_kunder


def get_kunde(cpr):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM kunder WHERE cpr = ?', (cpr,))
        row = cur.fetchone()

        if row is None:
            return None

        kunde = {'cpr': row[0], 'navn': row[1], 'tlf': row[2], 'email': row[3], 'adresse': row[4]}

        return kunde

def create_kunde(cpr, navn, tlf, email, adresse):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO kunder (cpr, navn, tlf, email, adresse) VALUES (?, ?, ?, ?, ?)', (cpr, navn, tlf, email, adresse))
        conn.commit()

        cur.execute('SELECT * FROM kunder WHERE cpr = ?', (cpr,))
        row = cur.fetchone()

        if row is None:
            return None
        return row
