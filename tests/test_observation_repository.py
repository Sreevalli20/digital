"""
Tests for observation repository operations.
"""
import pytest
from datetime import datetime, timedelta
from repositories.database import Database
from repositories.patient_repository import PatientRepository
from repositories.observation_repository import ObservationRepository
from domain.patient import Patient
from domain.observation import Observation, ProvenanceType, DataSource


@pytest.fixture
def test_db():
    """Create a test database."""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        db_path = f.name
    
    db = Database(db_path)
    db.initialize_schema()
    
    yield db
    
    os.unlink(db_path)


@pytest.fixture
def patient_repo(test_db):
    """Create patient repository fixture."""
    return PatientRepository(test_db)


@pytest.fixture
def obs_repo(test_db):
    """Create observation repository fixture."""
    return ObservationRepository(test_db)


@pytest.fixture
def test_patient(patient_repo):
    """Create a test patient."""
    patient = Patient(
        first_name='Test',
        last_name='Patient'
    )
    return patient_repo.create(patient)


def test_create_observation(obs_repo, test_patient):
    """Test creating an observation."""
    obs = Observation(
        patient_id=test_patient.id,
        observation_type='heart_rate',
        value=72.0,
        unit='bpm',
        timestamp=datetime.utcnow()
    )
    
    created = obs_repo.create(obs)
    
    assert created.id is not None
    assert created.observation_type == 'heart_rate'
    assert created.value == 72.0


def test_create_batch_observations(obs_repo, test_patient):
    """Test creating multiple observations in batch."""
    observations = [
        Observation(
            patient_id=test_patient.id,
            observation_type='heart_rate',
            value=70.0 + i,
            unit='bpm',
            timestamp=datetime.utcnow() - timedelta(days=i)
        )
        for i in range(5)
    ]
    
    created = obs_repo.create_batch(observations)
    
    assert len(created) == 5
    assert all(obs.id is not None for obs in created)


def test_get_observations_by_patient(obs_repo, test_patient):
    """Test retrieving observations for a patient."""
    obs1 = Observation(
        patient_id=test_patient.id,
        observation_type='heart_rate',
        value=70.0,
        unit='bpm'
    )
    obs2 = Observation(
        patient_id=test_patient.id,
        observation_type='systolic_bp',
        value=120.0,
        unit='mmHg'
    )
    
    obs_repo.create(obs1)
    obs_repo.create(obs2)
    
    observations = obs_repo.get_by_patient(test_patient.id)
    
    assert len(observations) == 2


def test_get_observations_by_type(obs_repo, test_patient):
    """Test retrieving observations filtered by type."""
    obs_repo.create(Observation(
        patient_id=test_patient.id,
        observation_type='heart_rate',
        value=70.0,
        unit='bpm'
    ))
    obs_repo.create(Observation(
        patient_id=test_patient.id,
        observation_type='systolic_bp',
        value=120.0,
        unit='mmHg'
    ))
    
    hr_obs = obs_repo.get_by_patient(test_patient.id, observation_type='heart_rate')
    
    assert len(hr_obs) == 1
    assert hr_obs[0].observation_type == 'heart_rate'


def test_get_latest_by_type(obs_repo, test_patient):
    """Test retrieving the latest observation of a type."""
    older = Observation(
        patient_id=test_patient.id,
        observation_type='heart_rate',
        value=70.0,
        unit='bpm',
        timestamp=datetime.utcnow() - timedelta(days=10)
    )
    newer = Observation(
        patient_id=test_patient.id,
        observation_type='heart_rate',
        value=75.0,
        unit='bpm',
        timestamp=datetime.utcnow()
    )
    
    obs_repo.create(older)
    obs_repo.create(newer)
    
    latest = obs_repo.get_latest_by_type(test_patient.id, 'heart_rate')
    
    assert latest.value == 75.0


def test_count_by_patient(obs_repo, test_patient):
    """Test counting observations for a patient."""
    assert obs_repo.count_by_patient(test_patient.id) == 0
    
    obs_repo.create(Observation(
        patient_id=test_patient.id,
        observation_type='heart_rate',
        value=70.0,
        unit='bpm'
    ))
    
    assert obs_repo.count_by_patient(test_patient.id) == 1


def test_delete_by_patient(obs_repo, test_patient):
    """Test deleting all observations for a patient."""
    obs_repo.create(Observation(
        patient_id=test_patient.id,
        observation_type='heart_rate',
        value=70.0,
        unit='bpm'
    ))
    obs_repo.create(Observation(
        patient_id=test_patient.id,
        observation_type='systolic_bp',
        value=120.0,
        unit='mmHg'
    ))
    
    deleted_count = obs_repo.delete_by_patient(test_patient.id)
    
    assert deleted_count == 2
    assert obs_repo.count_by_patient(test_patient.id) == 0
