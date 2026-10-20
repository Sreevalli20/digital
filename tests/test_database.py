"""
Tests for database initialization and operations.
"""
import pytest
import os
import tempfile
from repositories.database import Database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        db_path = f.name
    
    db = Database(db_path)
    db.initialize_schema()
    
    yield db
    
    # Cleanup
    os.unlink(db_path)


def test_database_initialization(temp_db):
    """Test that database initializes correctly."""
    assert os.path.exists(temp_db.db_path)
    
    with temp_db.get_connection() as conn:
        # Check that tables exist
        tables = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table'
        """).fetchall()
        
        table_names = [t['name'] for t in tables]
        assert 'patients' in table_names
        assert 'observations' in table_names
        assert 'scenarios' in table_names
        assert 'provenance_ledger' in table_names


def test_database_indexes(temp_db):
    """Test that indexes are created."""
    with temp_db.get_connection() as conn:
        indexes = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='index'
        """).fetchall()
        
        index_names = [i['name'] for i in indexes]
        assert 'idx_observations_patient_id' in index_names
        assert 'idx_observations_timestamp' in index_names


def test_database_backup(temp_db):
    """Test database backup functionality."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        backup_path = f.name
    
    try:
        temp_db.backup_database(backup_path)
        assert os.path.exists(backup_path)
    finally:
        if os.path.exists(backup_path):
            os.unlink(backup_path)


def test_database_reset(temp_db):
    """Test database reset functionality."""
    # Add some data first
    with temp_db.get_connection() as conn:
        conn.execute("INSERT INTO patients (first_name, last_name, created_at, updated_at) VALUES (?, ?, ?, ?)",
                    ('Test', 'Patient', '2024-01-01', '2024-01-01'))
    
    # Reset
    temp_db.reset_database()
    
    # Check data is gone
    with temp_db.get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) as count FROM patients").fetchone()
        assert count['count'] == 0
