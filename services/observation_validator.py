"""
Observation validation service.
"""
from typing import Optional, Tuple, List
from datetime import datetime
import config
from domain.observation import Observation


class ObservationValidator:
    """Validates observation data against defined constraints."""
    
    def __init__(self):
        """Initialize validator with observation type configurations."""
        self.observation_types = config.OBSERVATION_TYPES
    
    def validate(self, observation: Observation) -> Tuple[bool, Optional[str]]:
        """
        Validate a single observation.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if observation type is supported
        if observation.observation_type not in self.observation_types:
            return False, f"Unsupported observation type: {observation.observation_type}"
        
        type_config = self.observation_types[observation.observation_type]
        
        # Check for missing value
        if observation.value is None:
            return True, None  # Missing values are allowed but flagged
        
        # Check value range
        if observation.value < type_config['min'] or observation.value > type_config['max']:
            return False, (
                f"Value {observation.value} out of valid range "
                f"[{type_config['min']}, {type_config['max']}] for {observation.observation_type}"
            )
        
        # Check unit match
        if observation.unit != type_config['unit']:
            return False, (
                f"Unit mismatch: expected '{type_config['unit']}', got '{observation.unit}'"
            )
        
        # Check timestamp is not in the future
        if observation.timestamp and observation.timestamp > datetime.utcnow():
            return False, "Observation timestamp cannot be in the future"
        
        return True, None
    
    def validate_batch(self, observations: List[Observation]) -> List[Observation]:
        """
        Validate a batch of observations.
        
        Returns observations with validation status set.
        """
        for obs in observations:
            is_valid, error = self.validate(obs)
            obs.is_valid = is_valid
            obs.validation_error = error
        
        return observations
    
    def check_duplicates(self, observations: List[Observation]) -> List[Tuple[int, int]]:
        """
        Check for duplicate observations in a batch.
        
        Returns list of (index1, index2) tuples for duplicates.
        """
        duplicates = []
        seen = {}
        
        for i, obs in enumerate(observations):
            key = (obs.patient_id, obs.observation_type, obs.timestamp)
            if key in seen:
                duplicates.append((seen[key], i))
            else:
                seen[key] = i
        
        return duplicates
    
    def get_observation_type_config(self, observation_type: str) -> Optional[dict]:
        """Get configuration for an observation type."""
        return self.observation_types.get(observation_type)
    
    def get_supported_types(self) -> List[str]:
        """Get list of supported observation types."""
        return list(self.observation_types.keys())
