"""
Patient repository for data access operations.
"""
import sqlite3
from typing import Optional, List
from datetime import datetime
from domain.patient import Patient, Gender
from repositories.database import Database


class PatientRepository:
    """Repository for patient data access."""
    
    def __init__(self, database: Database):
        """Initialize repository with database instance."""
        self.db = database
    
    def create(self, patient: Patient) -> Patient:
        """Create a new patient record."""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO patients (external_id, first_name, last_name, date_of_birth, 
                                     gender, created_at, updated_at, is_synthetic)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient.external_id,
                patient.first_name,
                patient.last_name,
                patient.date_of_birth.isoformat() if patient.date_of_birth else None,
                patient.gender.value if patient.gender else 'unknown',
                patient.created_at.isoformat() if patient.created_at else datetime.utcnow().isoformat(),
                patient.updated_at.isoformat() if patient.updated_at else datetime.utcnow().isoformat(),
                1 if patient.is_synthetic else 0
            ))
            patient.id = cursor.lastrowid
            return patient
    
    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        """Get a patient by ID."""
        with self.db.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM patients WHERE id = ?",
                (patient_id,)
            ).fetchone()
            
            if row:
                return self._row_to_patient(row)
            return None
    
    def get_by_external_id(self, external_id: str) -> Optional[Patient]:
        """Get a patient by external ID."""
        with self.db.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM patients WHERE external_id = ?",
                (external_id,)
            ).fetchone()
            
            if row:
                return self._row_to_patient(row)
            return None
    
    def get_all(self, limit: Optional[int] = None) -> List[Patient]:
        """Get all patients, optionally limited."""
        with self.db.get_connection() as conn:
            query = "SELECT * FROM patients ORDER BY created_at DESC"
            if limit:
                query += f" LIMIT {limit}"
            
            rows = conn.execute(query).fetchall()
            return [self._row_to_patient(row) for row in rows]
    
    def get_synthetic_patients(self) -> List[Patient]:
        """Get all synthetic patients."""
        with self.db.get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM patients WHERE is_synthetic = 1 ORDER BY created_at DESC"
            ).fetchall()
            return [self._row_to_patient(row) for row in rows]
    
    def update(self, patient: Patient) -> Patient:
        """Update an existing patient record."""
        patient.updated_at = datetime.utcnow()
        
        with self.db.get_connection() as conn:
            conn.execute("""
                UPDATE patients 
                SET external_id = ?, first_name = ?, last_name = ?, date_of_birth = ?,
                    gender = ?, updated_at = ?, is_synthetic = ?
                WHERE id = ?
            """, (
                patient.external_id,
                patient.first_name,
                patient.last_name,
                patient.date_of_birth.isoformat() if patient.date_of_birth else None,
                patient.gender.value if patient.gender else 'unknown',
                patient.updated_at.isoformat(),
                1 if patient.is_synthetic else 0,
                patient.id
            ))
            return patient
    
    def delete(self, patient_id: int) -> bool:
        """Delete a patient record."""
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM patients WHERE id = ?",
                (patient_id,)
            )
            return cursor.rowcount > 0
    
    def count(self) -> int:
        """Count total patients."""
        with self.db.get_connection() as conn:
            row = conn.execute("SELECT COUNT(*) as count FROM patients").fetchone()
            return row['count']
    
    def _row_to_patient(self, row: sqlite3.Row) -> Patient:
        """Convert database row to Patient object."""
        return Patient(
            id=row['id'],
            external_id=row['external_id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            date_of_birth=datetime.fromisoformat(row['date_of_birth']) if row['date_of_birth'] else None,
            gender=Gender(row['gender']) if row['gender'] else Gender.UNKNOWN,
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
            is_synthetic=bool(row['is_synthetic'])
        )
