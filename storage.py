import sqlite3
import pandas as pd
from datetime import datetime

class DataStorage:
    def __init__(self, db_path='supply_chain_research.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                terminal_id TEXT,
                activity_count INTEGER,
                z_score REAL,
                alpha_signal TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_activity(self, terminal_id, count, z_score, signal):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activity_logs (terminal_id, activity_count, z_score, alpha_signal)
            VALUES (?, ?, ?, ?)
        ''', (terminal_id, count, z_score, signal))
        conn.commit()
        conn.close()

    def get_history(self, limit=100):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(f'SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT {limit}', conn)
        conn.close()
        return df

if __name__ == "__main__":
    storage = DataStorage()
    storage.log_activity('ALPHA-1', 15, 1.2, 'Neutral')
    print("Database initialized and test entry added.")
