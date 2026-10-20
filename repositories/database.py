"""
Database initialization and connection management.
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Optional
import config


class Database:
    """SQLite database connection and schema management."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database with optional custom path."""
        self.db_path = db_path or config.DATABASE_PATH
        self._ensure_db_directory()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Get a database connection with context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def initialize_schema(self):
        """Initialize all database tables."""
        with self.get_connection() as conn:
            self._create_patients_table(conn)
            self._create_observations_table(conn)
            self._create_scenarios_table(conn)
            self._create_provenance_ledger_table(conn)
            self._create_indexes(conn)
    
    def _create_patients_table(self, conn: sqlite3.Connection):
        """Create patients table."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                external_id TEXT UNIQUE,
                first_name TEXT NOT NULL DEFAULT '',
                last_name TEXT NOT NULL DEFAULT '',
                date_of_birth TEXT,
                gender TEXT NOT NULL DEFAULT 'unknown',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_synthetic INTEGER NOT NULL DEFAULT 0
            )
        """)
    
    def _create_observations_table(self, conn: sqlite3.Connection):
        """Create observations table."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                observation_type TEXT NOT NULL,
                value REAL,
                unit TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                provenance TEXT NOT NULL DEFAULT 'manual',
                data_source TEXT NOT NULL DEFAULT 'real',
                notes TEXT,
                is_valid INTEGER NOT NULL DEFAULT 1,
                validation_error TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
        """)
    
    def _create_scenarios_table(self, conn: sqlite3.Connection):
        """Create scenarios table."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                modifications TEXT NOT NULL,
                baseline_risk_score REAL,
                scenario_risk_score REAL,
                baseline_risk_level TEXT,
                scenario_risk_level TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
        """)
    
    def _create_provenance_ledger_table(self, conn: sqlite3.Connection):
        """Create provenance ledger table."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS provenance_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                record_type TEXT NOT NULL,
                record_id INTEGER NOT NULL,
                source TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                processing_status TEXT NOT NULL DEFAULT 'success',
                metadata TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
        """)
    
    def _create_indexes(self, conn: sqlite3.Connection):
        """Create database indexes for performance."""
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_observations_patient_id 
            ON observations(patient_id)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_observations_timestamp 
            ON observations(timestamp)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_observations_patient_timestamp 
            ON observations(patient_id, timestamp)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_provenance_patient 
            ON provenance_ledger(patient_id)
        """)
    
    def backup_database(self, backup_path: str):
        """Create a backup of the database."""
        import shutil
        shutil.copy2(self.db_path, backup_path)
    
    def restore_database(self, backup_path: str):
        """Restore database from a backup."""
        import shutil
        shutil.copy2(backup_path, self.db_path)
    
    def reset_database(self):
        """Drop all tables and reinitialize schema."""
        with self.get_connection() as conn:
            conn.execute("DROP TABLE IF EXISTS provenance_ledger")
            conn.execute("DROP TABLE IF EXISTS scenarios")
            conn.execute("DROP TABLE IF EXISTS observations")
            conn.execute("DROP TABLE IF EXISTS patients")
        self.initialize_schema()
