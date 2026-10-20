"""
Tests for patient repository operations.
"""
import pytest
from datetime import datetime
from repositories.database import Database
from repositories.patient_repository import PatientRepository
from domain.patient import Patient, Gender


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


def test_create_patient(patient_repo):
    """Test creating a patient."""
    patient = Patient(
        first_name='John',
        last_name='Doe',
        gender=Gender.MALE,
        is_synthetic=False
    )
    
    created = patient_repo.create(patient)
    
    assert created.id is not None
    assert created.first_name == 'John'
    assert created.last_name == 'Doe'
    assert created.gender == Gender.MALE


def test_get_patient_by_id(patient_repo):
    """Test retrieving a patient by ID."""
    patient = Patient(
        first_name='Jane',
        last_name='Smith',
        gender=Gender.FEMALE
    )
    
    created = patient_repo.create(patient)
    retrieved = patient_repo.get_by_id(created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.first_name == 'Jane'


def test_get_patient_by_external_id(patient_repo):
    """Test retrieving a patient by external ID."""
    patient = Patient(
        external_id='EXT123',
        first_name='Test',
        last_name='User'
    )
    
    created = patient_repo.create(patient)
    retrieved = patient_repo.get_by_external_id('EXT123')
    
    assert retrieved is not None
    assert retrieved.id == created.id


def test_update_patient(patient_repo):
    """Test updating a patient."""
    patient = Patient(
        first_name='Original',
        last_name='Name'
    )
    
    created = patient_repo.create(patient)
    created.first_name = 'Updated'
    
    updated = patient_repo.update(created)
    
    assert updated.first_name == 'Updated'
    
    # Verify persistence
    retrieved = patient_repo.get_by_id(created.id)
    assert retrieved.first_name == 'Updated'


def test_delete_patient(patient_repo):
    """Test deleting a patient."""
    patient = Patient(
        first_name='Delete',
        last_name='Me'
    )
    
    created = patient_repo.create(patient)
    deleted = patient_repo.delete(created.id)
    
    assert deleted is True
    
    # Verify deletion
    retrieved = patient_repo.get_by_id(created.id)
    assert retrieved is None


def test_get_all_patients(patient_repo):
    """Test retrieving all patients."""
    patient1 = Patient(first_name='A', last_name='One')
    patient2 = Patient(first_name='B', last_name='Two')
    
    patient_repo.create(patient1)
    patient_repo.create(patient2)
    
    all_patients = patient_repo.get_all()
    
    assert len(all_patients) == 2


def test_count_patients(patient_repo):
    """Test counting patients."""
    assert patient_repo.count() == 0
    
    patient_repo.create(Patient(first_name='Test', last_name='User'))
    
    assert patient_repo.count() == 1


def test_patient_age_calculation():
    """Test patient age calculation."""
    from datetime import timedelta
    
    # Use 365.25 days per year to account for leap years
    patient = Patient(
        date_of_birth=datetime.utcnow() - timedelta(days=365 * 30 + 7)  # ~30 years
    )
    
    assert patient.age == 30
