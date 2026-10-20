"""
Scenario repository for data access operations.
"""
import sqlite3
import json
from typing import Optional, List
from datetime import datetime
from domain.scenario import Scenario, ScenarioStatus
from repositories.database import Database


class ScenarioRepository:
    """Repository for scenario data access."""
    
    def __init__(self, database: Database):
        """Initialize repository with database instance."""
        self.db = database
    
    def create(self, scenario: Scenario) -> Scenario:
        """Create a new scenario record."""
        with self.db.get_connection() as conn:
            modifications_json = json.dumps({
                k: v.to_dict() for k, v in scenario.modifications.items()
            })
            
            cursor = conn.execute("""
                INSERT INTO scenarios (patient_id, name, description, modifications,
                                      baseline_risk_score, scenario_risk_score,
                                      baseline_risk_level, scenario_risk_level,
                                      status, created_at, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                scenario.patient_id,
                scenario.name,
                scenario.description,
                modifications_json,
                scenario.baseline_risk_score,
                scenario.scenario_risk_score,
                scenario.baseline_risk_level,
                scenario.scenario_risk_level,
                scenario.status.value,
                scenario.created_at.isoformat() if scenario.created_at else datetime.utcnow().isoformat(),
                scenario.notes
            ))
            scenario.id = cursor.lastrowid
            return scenario
    
    def get_by_id(self, scenario_id: int) -> Optional[Scenario]:
        """Get a scenario by ID."""
        with self.db.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM scenarios WHERE id = ?",
                (scenario_id,)
            ).fetchone()
            
            if row:
                return self._row_to_scenario(row)
            return None
    
    def get_by_patient(self, patient_id: int, limit: Optional[int] = None) -> List[Scenario]:
        """Get scenarios for a patient."""
        with self.db.get_connection() as conn:
            query = "SELECT * FROM scenarios WHERE patient_id = ? ORDER BY created_at DESC"
            if limit:
                query += f" LIMIT {limit}"
            
            rows = conn.execute(query, (patient_id,)).fetchall()
            return [self._row_to_scenario(row) for row in rows]
    
    def update(self, scenario: Scenario) -> Scenario:
        """Update an existing scenario record."""
        with self.db.get_connection() as conn:
            modifications_json = json.dumps({
                k: v.to_dict() for k, v in scenario.modifications.items()
            })
            
            conn.execute("""
                UPDATE scenarios 
                SET name = ?, description = ?, modifications = ?,
                    baseline_risk_score = ?, scenario_risk_score = ?,
                    baseline_risk_level = ?, scenario_risk_level = ?,
                    status = ?, notes = ?
                WHERE id = ?
            """, (
                scenario.name,
                scenario.description,
                modifications_json,
                scenario.baseline_risk_score,
                scenario.scenario_risk_score,
                scenario.baseline_risk_level,
                scenario.scenario_risk_level,
                scenario.status.value,
                scenario.notes,
                scenario.id
            ))
            return scenario
    
    def delete(self, scenario_id: int) -> bool:
        """Delete a scenario record."""
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM scenarios WHERE id = ?",
                (scenario_id,)
            )
            return cursor.rowcount > 0
    
    def delete_by_patient(self, patient_id: int) -> int:
        """Delete all scenarios for a patient."""
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM scenarios WHERE patient_id = ?",
                (patient_id,)
            )
            return cursor.rowcount
    
    def _row_to_scenario(self, row: sqlite3.Row) -> Scenario:
        """Convert database row to Scenario object."""
        from domain.scenario import ScenarioModification
        
        modifications_dict = json.loads(row['modifications']) if row['modifications'] else {}
        modifications = {}
        
        for key, value in modifications_dict.items():
            modifications[key] = ScenarioModification(
                feature_name=value['feature_name'],
                original_value=value['original_value'],
                modified_value=value['modified_value'],
                unit=value['unit']
            )
        
        return Scenario(
            id=row['id'],
            patient_id=row['patient_id'],
            name=row['name'],
            description=row['description'],
            modifications=modifications,
            baseline_risk_score=row['baseline_risk_score'],
            scenario_risk_score=row['scenario_risk_score'],
            baseline_risk_level=row['baseline_risk_level'],
            scenario_risk_level=row['scenario_risk_level'],
            status=ScenarioStatus(row['status']) if row['status'] else ScenarioStatus.PENDING,
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            notes=row['notes']
        )
