# this module manage DB

import sqlite3
from datetime import datetime
from typing import Tuple

DB_PATH = 'traffic.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=True)
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS packets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        src_ip TEXT,
        dst_ip TEXT,
        protocol INTEGER,
        size INTEGER,
        timestamp TEXT
    )''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        src_ip TEXT,
        count INTEGER,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

