"""
Tests for Digital Twin state engine.
"""
import pytest
from datetime import datetime, timedelta
from repositories.database import Database
from repositories.patient_repository import PatientRepository
from repositories.observation_repository import ObservationRepository
from services.digital_twin_engine import DigitalTwinEngine
from domain.patient import Patient
from domain.observation import Observation, DataSource


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
def twin_engine(obs_repo):
    """Create Digital Twin engine fixture."""
    return DigitalTwinEngine(obs_repo)


@pytest.fixture
def test_patient(patient_repo):
    """Create a test patient with observations."""
    patient = Patient(first_name='Test', last_name='Patient')
    created = patient_repo.create(patient)
    return created


def test_compute_state_no_observations(twin_engine, test_patient):
    """Test computing state with no observations."""
    state = twin_engine.compute_state(test_patient.id)
    
    assert state.patient_id == test_patient.id
    assert state.total_observations == 0
    assert state.overall_data_quality.value == 'insufficient'


def test_compute_state_with_observations(twin_engine, obs_repo, test_patient):
    """Test computing state with observations."""
    # Add observations
    for i in range(10):
        obs = Observation(
            patient_id=test_patient.id,
            observation_type='heart_rate',
            value=70.0 + i,
            unit='bpm',
            timestamp=datetime.utcnow() - timedelta(days=i)
        )
        obs_repo.create(obs)
    
    state = twin_engine.compute_state(test_patient.id)
    
    assert state.total_observations == 10
    assert 'heart_rate' in state.features
    
    hr_feature = state.features['heart_rate']
    assert hr_feature.observation_count == 10
    assert hr_feature.current_value is not None


def test_baseline_calculation(twin_engine, obs_repo, test_patient):
    """Test baseline value calculation."""
    # Add observations
    for i in range(5):
        obs = Observation(
            patient_id=test_patient.id,
            observation_type='heart_rate',
            value=70.0,
            unit='bpm',
            timestamp=datetime.utcnow() - timedelta(days=i)
        )
        obs_repo.create(obs)
    
    state = twin_engine.compute_state(test_patient.id)
    hr_feature = state.features['heart_rate']
    
    assert hr_feature.baseline_value is not None
    assert hr_feature.baseline_value == 70.0


def test_rolling_average_calculation(twin_engine, obs_repo, test_patient):
    """Test rolling average calculation."""
    # Add observations over 30 days
    for i in range(30):
        obs = Observation(
            patient_id=test_patient.id,
            observation_type='heart_rate',
            value=70.0 + (i % 5),
            unit='bpm',
            timestamp=datetime.utcnow() - timedelta(days=i)
        )
        obs_repo.create(obs)
    
    state = twin_engine.compute_state(test_patient.id)
    hr_feature = state.features['heart_rate']
    
    assert hr_feature.rolling_avg is not None


def test_change_from_baseline(twin_engine, obs_repo, test_patient):
    """Test change from baseline calculation."""
    # Add baseline observations
    for i in range(3):
        obs = Observation(
            patient_id=test_patient.id,
            observation_type='heart_rate',
            value=70.0,
            unit='bpm',
            timestamp=datetime.utcnow() - timedelta(days=10 + i)
        )
        obs_repo.create(obs)
    
    # Add current observation with different value
    obs = Observation(
        patient_id=test_patient.id,
        observation_type='heart_rate',
        value=80.0,
        unit='bpm',
        timestamp=datetime.utcnow()
    )
    obs_repo.create(obs)
    
    state = twin_engine.compute_state(test_patient.id)
    hr_feature = state.features['heart_rate']
    
    assert hr_feature.change_from_baseline == 10.0
    assert hr_feature.percent_change is not None


def test_trend_calculation(twin_engine, obs_repo, test_patient):
    """Test trend calculation."""
    # Add increasing trend
    for i in range(10):
        obs = Observation(
            patient_id=test_patient.id,
            observation_type='heart_rate',
            value=70.0 + i,
            unit='bpm',
            timestamp=datetime.utcnow() - timedelta(days=i)
        )
        obs_repo.create(obs)
    
    state = twin_engine.compute_state(test_patient.id)
    hr_feature = state.features['heart_rate']
    
    assert hr_feature.trend in ['increasing', 'decreasing', 'stable', 'unknown']


def test_data_quality_assessment(twin_engine, obs_repo, test_patient):
    """Test data quality assessment."""
    # Add recent observations
    for i in range(5):
        obs = Observation(
            patient_id=test_patient.id,
            observation_type='heart_rate',
            value=70.0,
            unit='bpm',
            timestamp=datetime.utcnow() - timedelta(days=i)
        )
        obs_repo.create(obs)
    
    state = twin_engine.compute_state(test_patient.id)
    hr_feature = state.features['heart_rate']
    
    assert hr_feature.data_quality.value in ['excellent', 'good', 'fair', 'poor', 'insufficient']


def test_completeness_score(twin_engine, obs_repo, test_patient):
    """Test completeness score calculation."""
    # Add observations for multiple types
    types = ['heart_rate', 'systolic_bp', 'diastolic_bp']
    for obs_type in types:
        for i in range(5):
            obs = Observation(
                patient_id=test_patient.id,
                observation_type=obs_type,
                value=70.0,
                unit='bpm' if obs_type == 'heart_rate' else 'mmHg',
                timestamp=datetime.utcnow() - timedelta(days=i)
            )
            obs_repo.create(obs)
    
    state = twin_engine.compute_state(test_patient.id)
    
    assert 0.0 <= state.completeness_score <= 1.0
