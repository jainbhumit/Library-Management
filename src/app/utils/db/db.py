import sqlite3
import src.app.config.config as config

class DB:
    @staticmethod
    def get_connection():
        conn = sqlite3.connect(config.DB_ADDR)
        conn.row_factory = sqlite3.Row
        return conn