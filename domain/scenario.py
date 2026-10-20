"""
Scenario domain model for hypothetical simulations.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class ScenarioStatus(Enum):
    """Status of a scenario simulation."""
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'


@dataclass
class ScenarioModification:
    """A modification to a feature in a scenario."""
    
    feature_name: str
    original_value: Optional[float]
    modified_value: float
    unit: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'feature_name': self.feature_name,
            'original_value': self.original_value,
            'modified_value': self.modified_value,
            'unit': self.unit
        }


@dataclass
class Scenario:
    """Represents a hypothetical scenario simulation."""
    
    id: Optional[int] = None
    patient_id: Optional[int] = None
    name: str = ''
    description: str = ''
    modifications: Dict[str, ScenarioModification] = field(default_factory=dict)
    baseline_risk_score: Optional[float] = None
    scenario_risk_score: Optional[float] = None
    baseline_risk_level: Optional[str] = None
    scenario_risk_level: Optional[str] = None
    status: ScenarioStatus = ScenarioStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    
    def add_modification(self, feature_name: str, original_value: Optional[float], 
                        modified_value: float, unit: str):
        """Add a feature modification to the scenario."""
        self.modifications[feature_name] = ScenarioModification(
            feature_name=feature_name,
            original_value=original_value,
            modified_value=modified_value,
            unit=unit
        )
    
    def get_risk_change(self) -> Optional[float]:
        """Calculate the change in risk score."""
        if self.baseline_risk_score is not None and self.scenario_risk_score is not None:
            return self.scenario_risk_score - self.baseline_risk_score
        return None
    
    def to_dict(self) -> dict:
        """Convert scenario to dictionary."""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'name': self.name,
            'description': self.description,
            'modifications': {k: v.to_dict() for k, v in self.modifications.items()},
            'baseline_risk_score': self.baseline_risk_score,
            'scenario_risk_score': self.scenario_risk_score,
            'baseline_risk_level': self.baseline_risk_level,
            'scenario_risk_level': self.scenario_risk_level,
            'risk_change': self.get_risk_change(),
            'status': self.status.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'notes': self.notes
        }
