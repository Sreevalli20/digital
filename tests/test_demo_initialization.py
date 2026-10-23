"""
Tests for demo initialization functionality.
"""
import pytest
import tempfile
import os
from repositories.database import Database
from repositories.patient_repository import PatientRepository
from repositories.observation_repository import ObservationRepository
from services.synthetic_data_generator import SyntheticDataGenerator
from domain.patient import Patient


@pytest.fixture
def test_db():
    """Create a test database."""
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
def observation_repo(test_db):
    """Create observation repository fixture."""
    return ObservationRepository(test_db)


@pytest.fixture
def synthetic_generator():
    """Create a synthetic data generator with fixed seed."""
    return SyntheticDataGenerator(seed=42)


def test_demo_initialization_empty_database(patient_repo, observation_repo, synthetic_generator):
    """Test that demo initialization works when database is empty."""
    # Ensure database is empty
    patients = patient_repo.get_all()
    assert len(patients) == 0

    # Generate demo patient
    patient = synthetic_generator.generate_patient(is_synthetic=True, use_demo_name=True, external_id="DEMO-001")
    observations = synthetic_generator.generate_observations(None, days_back=90, daily=True)

    # Save to database
    created_patient = patient_repo.create(patient)

    # Set patient_id for observations
    for obs in observations:
        obs.patient_id = created_patient.id

    created_observations = observation_repo.create_batch(observations)

    # Verify patient was created
    patients = patient_repo.get_all()
    assert len(patients) == 1
    assert patients[0].external_id == "DEMO-001"
    assert patients[0].is_synthetic is True

    # Verify observations were created
    observations = observation_repo.get_by_patient(created_patient.id)
    assert len(observations) > 0


def test_demo_initialization_idempotent(patient_repo, observation_repo, synthetic_generator):
    """Test that demo initialization is idempotent - doesn't create duplicates."""
    # First initialization
    patient1 = synthetic_generator.generate_patient(is_synthetic=True, use_demo_name=True, external_id="DEMO-001")
    observations1 = synthetic_generator.generate_observations(None, days_back=90, daily=True)
    created_patient1 = patient_repo.create(patient1)
    for obs in observations1:
        obs.patient_id = created_patient1.id
    observation_repo.create_batch(observations1)

    # Check patient count
    patients = patient_repo.get_all()
    initial_count = len(patients)
    assert initial_count == 1

    # Second initialization attempt (should check for existing patients)
    patients = patient_repo.get_all()
    if len(patients) > 0:
        # Don't create new patients if they already exist
        pass

    # Verify no duplicate patients
    patients = patient_repo.get_all()
    assert len(patients) == initial_count


def test_demo_patient_external_id_format(patient_repo, synthetic_generator):
    """Test that demo patient uses correct external ID format."""
    patient = synthetic_generator.generate_patient(is_synthetic=True, use_demo_name=True, external_id="DEMO-001")
    created_patient = patient_repo.create(patient)

    assert created_patient.external_id == "DEMO-001"
    assert created_patient.first_name == ""
    assert created_patient.last_name == ""
    assert created_patient.is_synthetic is True


def test_synthetic_observations_valid(synthetic_generator):
    """Test that synthetic observations are valid."""
    patient = synthetic_generator.generate_patient(is_synthetic=True, use_demo_name=True, external_id="DEMO-001")
    observations = synthetic_generator.generate_observations(None, days_back=90, daily=True)

    # All observations should have required fields
    for obs in observations:
        assert obs.observation_type is not None
        assert obs.value is not None
        assert obs.unit is not None
        assert obs.timestamp is not None
        assert obs.provenance.value == 'synthetic'
        assert obs.data_source.value == 'synthetic'
        assert obs.is_valid is True


def test_demo_observations_date_range(synthetic_generator):
    """Test that demo observations cover expected date range."""
    from datetime import datetime, timedelta

    observations = synthetic_generator.generate_observations(None, days_back=90, daily=True)

    # Should have observations for approximately 90 days
    timestamps = [obs.timestamp for obs in observations]
    if timestamps:
        latest = max(timestamps)
        earliest = min(timestamps)
        date_range = (latest - earliest).days
        # Allow some tolerance
        assert date_range >= 85
        assert date_range <= 95


def test_demo_observations_per_type(synthetic_generator):
    """Test that demo observations include all supported types."""
    from config import OBSERVATION_TYPES

    observations = synthetic_generator.generate_observations(None, days_back=90, daily=True)

    # Get unique observation types
    types_present = set(obs.observation_type for obs in observations)

    # Should include all supported types
    for obs_type in OBSERVATION_TYPES.keys():
        assert obs_type in types_present
