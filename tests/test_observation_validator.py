"""
Tests for observation validation.
"""
import pytest
from datetime import datetime, timedelta
from services.observation_validator import ObservationValidator
from domain.observation import Observation


@pytest.fixture
def validator():
    """Create validator fixture."""
    return ObservationValidator()


def test_valid_observation(validator):
    """Test validation of a valid observation."""
    obs = Observation(
        observation_type='heart_rate',
        value=72.0,
        unit='bpm',
        timestamp=datetime.utcnow()
    )
    
    is_valid, error = validator.validate(obs)
    
    assert is_valid is True
    assert error is None


def test_invalid_observation_type(validator):
    """Test validation with unsupported observation type."""
    obs = Observation(
        observation_type='invalid_type',
        value=72.0,
        unit='bpm'
    )
    
    is_valid, error = validator.validate(obs)
    
    assert is_valid is False
    assert 'Unsupported observation type' in error


def test_value_out_of_range(validator):
    """Test validation with value out of range."""
    obs = Observation(
        observation_type='heart_rate',
        value=300.0,  # Above max of 200
        unit='bpm'
    )
    
    is_valid, error = validator.validate(obs)
    
    assert is_valid is False
    assert 'out of valid range' in error


def test_unit_mismatch(validator):
    """Test validation with unit mismatch."""
    obs = Observation(
        observation_type='heart_rate',
        value=72.0,
        unit='mmHg'  # Wrong unit for heart rate
    )
    
    is_valid, error = validator.validate(obs)
    
    assert is_valid is False
    assert 'Unit mismatch' in error


def test_future_timestamp(validator):
    """Test validation with future timestamp."""
    obs = Observation(
        observation_type='heart_rate',
        value=72.0,
        unit='bpm',
        timestamp=datetime.utcnow() + timedelta(days=1)
    )
    
    is_valid, error = validator.validate(obs)
    
    assert is_valid is False
    assert 'cannot be in the future' in error


def test_missing_value_allowed(validator):
    """Test that missing values are allowed but flagged."""
    obs = Observation(
        observation_type='heart_rate',
        value=None,
        unit='bpm'
    )
    
    is_valid, error = validator.validate(obs)
    
    assert is_valid is True  # Missing values are allowed
    assert error is None


def test_validate_batch(validator):
    """Test batch validation."""
    observations = [
        Observation(
            observation_type='heart_rate',
            value=72.0,
            unit='bpm'
        ),
        Observation(
            observation_type='heart_rate',
            value=300.0,  # Invalid
            unit='bpm'
        )
    ]
    
    validated = validator.validate_batch(observations)
    
    assert validated[0].is_valid is True
    assert validated[1].is_valid is False
    assert validated[1].validation_error is not None


def test_check_duplicates(validator):
    """Test duplicate detection in batch."""
    timestamp = datetime.utcnow()
    observations = [
        Observation(
            patient_id=1,
            observation_type='heart_rate',
            value=72.0,
            unit='bpm',
            timestamp=timestamp
        ),
        Observation(
            patient_id=1,
            observation_type='heart_rate',
            value=75.0,
            unit='bpm',
            timestamp=timestamp
        )
    ]
    
    duplicates = validator.check_duplicates(observations)
    
    assert len(duplicates) == 1
    assert duplicates[0] == (0, 1)


def test_get_supported_types(validator):
    """Test getting supported observation types."""
    types = validator.get_supported_types()
    
    assert 'heart_rate' in types
    assert 'systolic_bp' in types
    assert 'bmi' in types
