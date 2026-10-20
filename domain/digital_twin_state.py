"""
Digital Twin state domain model.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class DataQuality(Enum):
    """Data quality assessment."""
    EXCELLENT = 'excellent'
    GOOD = 'good'
    FAIR = 'fair'
    POOR = 'poor'
    INSUFFICIENT = 'insufficient'


@dataclass
class FeatureState:
    """State of a single feature in the Digital Twin."""
    
    feature_name: str
    baseline_value: Optional[float] = None
    current_value: Optional[float] = None
    rolling_avg: Optional[float] = None
    change_from_baseline: Optional[float] = None
    percent_change: Optional[float] = None
    trend: Optional[str] = None  # 'increasing', 'decreasing', 'stable', 'unknown'
    data_quality: DataQuality = DataQuality.INSUFFICIENT
    last_observation: Optional[datetime] = None
    observation_count: int = 0
    days_since_last_observation: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert feature state to dictionary."""
        return {
            'feature_name': self.feature_name,
            'baseline_value': self.baseline_value,
            'current_value': self.current_value,
            'rolling_avg': self.rolling_avg,
            'change_from_baseline': self.change_from_baseline,
            'percent_change': self.percent_change,
            'trend': self.trend,
            'data_quality': self.data_quality.value,
            'last_observation': self.last_observation.isoformat() if self.last_observation else None,
            'observation_count': self.observation_count,
            'days_since_last_observation': self.days_since_last_observation
        }


@dataclass
class DigitalTwinState:
    """Represents the complete state of a patient's Digital Twin."""
    
    patient_id: Optional[int] = None
    generated_at: datetime = field(default_factory=datetime.utcnow)
    features: Dict[str, FeatureState] = field(default_factory=dict)
    overall_data_quality: DataQuality = DataQuality.INSUFFICIENT
    total_observations: int = 0
    data_freshness_days: Optional[int] = None
    completeness_score: float = 0.0
    
    def get_feature(self, feature_name: str) -> Optional[FeatureState]:
        """Get state for a specific feature."""
        return self.features.get(feature_name)
    
    def add_feature(self, feature_state: FeatureState):
        """Add or update a feature state."""
        self.features[feature_state.feature_name] = feature_state
    
    def to_dict(self) -> dict:
        """Convert Digital Twin state to dictionary."""
        return {
            'patient_id': self.patient_id,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'features': {k: v.to_dict() for k, v in self.features.items()},
            'overall_data_quality': self.overall_data_quality.value,
            'total_observations': self.total_observations,
            'data_freshness_days': self.data_freshness_days,
            'completeness_score': self.completeness_score
        }
