"""
Observation domain model.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class ProvenanceType(Enum):
    """Source of the observation data."""
    MANUAL = 'manual'
    CSV_IMPORT = 'csv_import'
    SYNTHETIC = 'synthetic'
    WEARABLE = 'wearable'
    SCENARIO = 'scenario'


class DataSource(Enum):
    """Type of data source."""
    REAL = 'real'
    SYNTHETIC = 'synthetic'
    IMPORTED = 'imported'


@dataclass
class Observation:
    """Represents a single physiological observation."""
    
    id: Optional[int] = None
    patient_id: Optional[int] = None
    observation_type: str = ''  # e.g., 'heart_rate', 'systolic_bp'
    value: Optional[float] = None
    unit: str = ''
    timestamp: datetime = field(default_factory=datetime.utcnow)
    provenance: ProvenanceType = ProvenanceType.MANUAL
    data_source: DataSource = DataSource.REAL
    notes: Optional[str] = None
    is_valid: bool = True
    validation_error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def is_missing(self) -> bool:
        """Check if the observation value is missing."""
        return self.value is None
    
    @property
    def is_synthetic(self) -> bool:
        """Check if this is synthetic data."""
        return self.data_source == DataSource.SYNTHETIC
    
    def to_dict(self) -> dict:
        """Convert observation to dictionary representation."""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'observation_type': self.observation_type,
            'value': self.value,
            'unit': self.unit,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'provenance': self.provenance.value if self.provenance else None,
            'data_source': self.data_source.value if self.data_source else None,
            'notes': self.notes,
            'is_valid': self.is_valid,
            'validation_error': self.validation_error,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_missing': self.is_missing,
            'is_synthetic': self.is_synthetic
        }
