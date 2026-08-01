# database/database.py
import os
import sqlite3

try:
    import psycopg2
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False


class DatabaseManager:

    def __init__(self, db_path):
        self.db_path = db_path
        self.db_url = os.environ.get("DATABASE_URL")
        self.is_postgres = False
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """
        Connects to either Cloud PostgreSQL or Local SQLite based on configuration.
        """
        if self.db_url and HAS_POSTGRES:
            try:
                # Support Neon/Supabase connection pooling parameters if present
                self.conn = psycopg2.connect(self.db_url)
                self.is_postgres = True
                self.cursor = self.conn.cursor()
                self.create_table()
                return
            except Exception as e:
                print(f"[DATABASE] Cloud Postgres connection failed: {e}. Falling back to local SQLite.")
        
        # Local SQLite fallback
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.is_postgres = False
            self.cursor = self.conn.cursor()
            self.create_table()
        except Exception as e:
            print(f"[DATABASE] Local SQLite connection failed: {e}")

    def create_table(self):
        """
        Creates the tracking logs table inside the connected database.
        """
        if not self.conn or not self.cursor:
            return

        try:
            if self.is_postgres:
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking_logs(
                    id SERIAL PRIMARY KEY,
                    timestamp VARCHAR(50) NOT NULL,
                    object_id INTEGER NOT NULL,
                    object_class VARCHAR(50) NOT NULL,
                    is_intrusion INTEGER DEFAULT 0
                )
                """)
            else:
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracking_logs(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    object_id INTEGER,
                    object_class TEXT,
                    is_intrusion INTEGER DEFAULT 0
                )
                """)
            self.conn.commit()
        except Exception as e:
            print(f"[DATABASE] Table creation failed: {e}")

    def insert_log(self, timestamp, object_id, object_class, is_intrusion=0):
        """
        Inserts a tracking log entry. Handles SQL syntax differences between Postgres and SQLite.
        """
        if not self.conn or not self.cursor:
            self.connect()
            if not self.conn or not self.cursor:
                return

        try:
            if self.is_postgres:
                self.cursor.execute(
                    """
                    INSERT INTO tracking_logs (timestamp, object_id, object_class, is_intrusion)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (timestamp, int(object_id), object_class, int(is_intrusion))
                )
            else:
                self.cursor.execute(
                    """
                    INSERT INTO tracking_logs (timestamp, object_id, object_class, is_intrusion)
                    VALUES (?, ?, ?, ?)
                    """,
                    (timestamp, int(object_id), object_class, int(is_intrusion))
                )
            self.conn.commit()
        except Exception as e:
            print(f"[DATABASE] Insert failed: {e}. Attempting reconnect...")
            # Try to reconnect and insert once more
            self.connect()
            try:
                if self.is_postgres:
                    self.cursor.execute(
                        """
                        INSERT INTO tracking_logs (timestamp, object_id, object_class, is_intrusion)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (timestamp, int(object_id), object_class, int(is_intrusion))
                    )
                else:
                    self.cursor.execute(
                        """
                        INSERT INTO tracking_logs (timestamp, object_id, object_class, is_intrusion)
                        VALUES (?, ?, ?, ?)
                        """,
                        (timestamp, int(object_id), object_class, int(is_intrusion))
                    )
                self.conn.commit()
            except Exception as re_err:
                print(f"[DATABASE] Reconnect insert failed: {re_err}")