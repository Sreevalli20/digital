"""
Observation repository for data access operations.
"""
import sqlite3
from typing import Optional, List, Dict
from datetime import datetime
from domain.observation import Observation, ProvenanceType, DataSource
from repositories.database import Database


class ObservationRepository:
    """Repository for observation data access."""
    
    def __init__(self, database: Database):
        """Initialize repository with database instance."""
        self.db = database
    
    def create(self, observation: Observation) -> Observation:
        """Create a new observation record."""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO observations (patient_id, observation_type, value, unit, 
                                         timestamp, provenance, data_source, notes, 
                                         is_valid, validation_error, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                observation.patient_id,
                observation.observation_type,
                observation.value,
                observation.unit,
                observation.timestamp.isoformat() if observation.timestamp else datetime.utcnow().isoformat(),
                observation.provenance.value if observation.provenance else 'manual',
                observation.data_source.value if observation.data_source else 'real',
                observation.notes,
                1 if observation.is_valid else 0,
                observation.validation_error,
                observation.created_at.isoformat() if observation.created_at else datetime.utcnow().isoformat()
            ))
            observation.id = cursor.lastrowid
            return observation
    
    def create_batch(self, observations: List[Observation]) -> List[Observation]:
        """Create multiple observation records in a single transaction."""
        created = []
        with self.db.get_connection() as conn:
            for obs in observations:
                cursor = conn.execute("""
                    INSERT INTO observations (patient_id, observation_type, value, unit, 
                                             timestamp, provenance, data_source, notes, 
                                             is_valid, validation_error, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    obs.patient_id,
                    obs.observation_type,
                    obs.value,
                    obs.unit,
                    obs.timestamp.isoformat() if obs.timestamp else datetime.utcnow().isoformat(),
                    obs.provenance.value if obs.provenance else 'manual',
                    obs.data_source.value if obs.data_source else 'real',
                    obs.notes,
                    1 if obs.is_valid else 0,
                    obs.validation_error,
                    obs.created_at.isoformat() if obs.created_at else datetime.utcnow().isoformat()
                ))
                obs.id = cursor.lastrowid
                created.append(obs)
        return created
    
    def get_by_id(self, observation_id: int) -> Optional[Observation]:
        """Get an observation by ID."""
        with self.db.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM observations WHERE id = ?",
                (observation_id,)
            ).fetchone()
            
            if row:
                return self._row_to_observation(row)
            return None
    
    def get_by_patient(self, patient_id: int, 
                      observation_type: Optional[str] = None,
                      limit: Optional[int] = None) -> List[Observation]:
        """Get observations for a patient, optionally filtered by type."""
        with self.db.get_connection() as conn:
            query = "SELECT * FROM observations WHERE patient_id = ?"
            params = [patient_id]
            
            if observation_type:
                query += " AND observation_type = ?"
                params.append(observation_type)
            
            query += " ORDER BY timestamp DESC"
            
            if limit:
                query += f" LIMIT {limit}"
            
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_observation(row) for row in rows]
    
    def get_latest_by_type(self, patient_id: int, observation_type: str) -> Optional[Observation]:
        """Get the most recent observation of a specific type for a patient."""
        with self.db.get_connection() as conn:
            row = conn.execute("""
                SELECT * FROM observations 
                WHERE patient_id = ? AND observation_type = ? AND is_valid = 1
                ORDER BY timestamp DESC LIMIT 1
            """, (patient_id, observation_type)).fetchone()
            
            if row:
                return self._row_to_observation(row)
            return None
    
    def get_observations_for_period(self, patient_id: int, 
                                   start_date: datetime,
                                   end_date: datetime) -> List[Observation]:
        """Get observations for a patient within a time period."""
        with self.db.get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM observations 
                WHERE patient_id = ? 
                AND timestamp >= ? 
                AND timestamp <= ?
                ORDER BY timestamp ASC
            """, (patient_id, start_date.isoformat(), end_date.isoformat())).fetchall()
            
            return [self._row_to_observation(row) for row in rows]
    
    def delete_by_patient(self, patient_id: int) -> int:
        """Delete all observations for a patient."""
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM observations WHERE patient_id = ?",
                (patient_id,)
            )
            return cursor.rowcount
    
    def count_by_patient(self, patient_id: int) -> int:
        """Count observations for a patient."""
        with self.db.get_connection() as conn:
            row = conn.execute(
                "SELECT COUNT(*) as count FROM observations WHERE patient_id = ?",
                (patient_id,)
            ).fetchone()
            return row['count']
    
    def get_observation_types_for_patient(self, patient_id: int) -> List[str]:
        """Get list of observation types for a patient."""
        with self.db.get_connection() as conn:
            rows = conn.execute("""
                SELECT DISTINCT observation_type 
                FROM observations 
                WHERE patient_id = ? AND is_valid = 1
                ORDER BY observation_type
            """, (patient_id,)).fetchall()
            return [row['observation_type'] for row in rows]
    
    def _row_to_observation(self, row: sqlite3.Row) -> Observation:
        """Convert database row to Observation object."""
        return Observation(
            id=row['id'],
            patient_id=row['patient_id'],
            observation_type=row['observation_type'],
            value=row['value'],
            unit=row['unit'],
            timestamp=datetime.fromisoformat(row['timestamp']) if row['timestamp'] else None,
            provenance=ProvenanceType(row['provenance']) if row['provenance'] else ProvenanceType.MANUAL,
            data_source=DataSource(row['data_source']) if row['data_source'] else DataSource.REAL,
            notes=row['notes'],
            is_valid=bool(row['is_valid']),
            validation_error=row['validation_error'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        )
