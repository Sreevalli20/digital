"""
Risk assessment domain model.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class RiskLevel(Enum):
    """Risk level categories."""
    LOW = 'low'
    MODERATE = 'moderate'
    HIGH = 'high'
    UNKNOWN = 'unknown'


@dataclass
class FeatureContribution:
    """Contribution of a feature to the risk assessment."""
    
    feature_name: str
    contribution_value: float
    direction: str  # 'increases_risk' or 'decreases_risk'
    baseline_value: Optional[float] = None
    current_value: Optional[float] = None
    explanation: str = ''
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'feature_name': self.feature_name,
            'contribution_value': self.contribution_value,
            'direction': self.direction,
            'baseline_value': self.baseline_value,
            'current_value': self.current_value,
            'explanation': self.explanation
        }


@dataclass
class RiskAssessment:
    """Represents a risk assessment for a patient."""
    
    patient_id: Optional[int] = None
    model_name: str = ''
    model_version: str = ''
    risk_level: RiskLevel = RiskLevel.UNKNOWN
    risk_score: Optional[float] = None  # 0.0 to 1.0
    target_condition: str = 'cardiometabolic_deterioration'
    generated_at: datetime = field(default_factory=datetime.utcnow)
    feature_contributions: List[FeatureContribution] = field(default_factory=list)
    data_quality_status: str = 'unknown'
    confidence: Optional[float] = None  # 0.0 to 1.0
    limitations: List[str] = field(default_factory=list)
    is_insufficient_data: bool = False
    insufficient_data_reason: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert risk assessment to dictionary."""
        return {
            'patient_id': self.patient_id,
            'model_name': self.model_name,
            'model_version': self.model_version,
            'risk_level': self.risk_level.value,
            'risk_score': self.risk_score,
            'target_condition': self.target_condition,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'feature_contributions': [fc.to_dict() for fc in self.feature_contributions],
            'data_quality_status': self.data_quality_status,
            'confidence': self.confidence,
            'limitations': self.limitations,
            'is_insufficient_data': self.is_insufficient_data,
            'insufficient_data_reason': self.insufficient_data_reason
        }
