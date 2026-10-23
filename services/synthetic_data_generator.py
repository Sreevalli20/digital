"""
Synthetic data generator for demo and testing.
"""
import random
from datetime import datetime, timedelta
from typing import List, Optional
from domain.patient import Patient, Gender
from domain.observation import Observation, ProvenanceType, DataSource
import config


class SyntheticDataGenerator:
    """Generates synthetic patient data for demonstration and testing."""
    
    FIRST_NAMES = ['Arjun', 'Priya', 'Rahul', 'Anita', 'Vikram', 'Meera', 'Aditya', 'Kavita', 
                   'Rajesh', 'Sunita', 'Amit', 'Neha', 'Vijay', 'Lakshmi', 'Sanjay', 'Deepa']
    LAST_NAMES = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Verma', 'Malhotra', 'Reddy',
                  'Nair', 'Iyer', 'Chopra', 'Kapoor', 'Mehta', 'Jain', 'Saxena', 'Das']
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize generator with optional random seed for reproducibility."""
        if seed is not None:
            random.seed(seed)
    
    def generate_patient(self, is_synthetic: bool = True,
                        external_id: Optional[str] = None,
                        use_demo_name: bool = False) -> Patient:
        """Generate a synthetic patient.

        Args:
            is_synthetic: Whether this is synthetic data
            external_id: Optional external identifier
            use_demo_name: If True, use DEMO-001 style identifier instead of personal names
        """
        if use_demo_name:
            patient = Patient(
                external_id=external_id or "DEMO-001",
                first_name="",
                last_name="",
                gender=random.choice(list(Gender)),
                is_synthetic=is_synthetic
            )
        else:
            patient = Patient(
                external_id=external_id or f"synthetic_{random.randint(1000, 9999)}",
                first_name=random.choice(self.FIRST_NAMES),
                last_name=random.choice(self.LAST_NAMES),
                gender=random.choice(list(Gender)),
                is_synthetic=is_synthetic
            )
        
        # Random date of birth (20-70 years old)
        age = random.randint(20, 70)
        dob = datetime.utcnow() - timedelta(days=age * 365)
        patient.date_of_birth = dob
        
        return patient
    
    def generate_observations(self, patient_id: int, 
                               days_back: int = 90,
                               daily: bool = False) -> List[Observation]:
        """
        Generate synthetic observations for a patient.
        
        Args:
            patient_id: Patient ID to generate observations for
            days_back: Number of days of historical data to generate
            daily: If True, generate daily observations; if False, generate weekly
        
        Returns:
            List of synthetic observations
        """
        observations = []
        
        # Generate baseline health profile
        base_heart_rate = random.randint(60, 85)
        base_systolic_bp = random.randint(110, 140)
        base_diastolic_bp = random.randint(70, 90)
        base_bmi = random.uniform(18.5, 32.0)
        base_glucose = random.uniform(85, 110)
        base_activity = random.randint(30, 90)
        base_sleep = random.uniform(6.5, 8.5)
        
        # Determine observation frequency
        interval_days = 1 if daily else 7
        num_observations = days_back // interval_days
        
        for i in range(num_observations):
            timestamp = datetime.utcnow() - timedelta(days=i * interval_days)
            
            # Add some variation to measurements
            heart_rate = base_heart_rate + random.randint(-5, 10)
            systolic_bp = base_systolic_bp + random.randint(-5, 10)
            diastolic_bp = base_diastolic_bp + random.randint(-5, 8)
            bmi = base_bmi + random.uniform(-0.5, 0.5)
            glucose = base_glucose + random.uniform(-10, 15)
            activity = base_activity + random.randint(-15, 30)
            sleep = base_sleep + random.uniform(-1.0, 1.0)
            
            # Create observations for each type
            obs_types = [
                ('heart_rate', heart_rate, 'bpm'),
                ('systolic_bp', systolic_bp, 'mmHg'),
                ('diastolic_bp', diastolic_bp, 'mmHg'),
                ('bmi', round(bmi, 1), 'kg/m²'),
                ('glucose', round(glucose, 0), 'mg/dL'),
                ('activity_minutes', max(0, activity), 'minutes'),
                ('sleep_hours', max(0, round(sleep, 1)), 'hours')
            ]
            
            for obs_type, value, unit in obs_types:
                observation = Observation(
                    patient_id=patient_id,
                    observation_type=obs_type,
                    value=value,
                    unit=unit,
                    timestamp=timestamp,
                    provenance=ProvenanceType.SYNTHETIC,
                    data_source=DataSource.SYNTHETIC,
                    is_valid=True
                )
                observations.append(observation)
        
        # Sort by timestamp
        observations.sort(key=lambda o: o.timestamp)
        
        return observations
    
    def generate_high_risk_patient(self, patient_id: int) -> tuple[Patient, List[Observation]]:
        """Generate a synthetic patient with elevated risk factors."""
        patient = self.generate_patient(is_synthetic=True, external_id="high_risk_demo")
        
        # Elevated risk profile
        base_heart_rate = random.randint(85, 100)
        base_systolic_bp = random.randint(140, 160)
        base_diastolic_bp = random.randint(90, 100)
        base_bmi = random.uniform(30.0, 38.0)
        base_glucose = random.uniform(110, 140)
        
        observations = []
        for i in range(60):  # 60 days of data
            timestamp = datetime.utcnow() - timedelta(days=i)
            
            heart_rate = base_heart_rate + random.randint(-3, 8)
            systolic_bp = base_systolic_bp + random.randint(-5, 10)
            diastolic_bp = base_diastolic_bp + random.randint(-5, 8)
            bmi = base_bmi + random.uniform(-0.3, 0.5)
            glucose = base_glucose + random.uniform(-8, 12)
            
            obs_types = [
                ('heart_rate', heart_rate, 'bpm'),
                ('systolic_bp', systolic_bp, 'mmHg'),
                ('diastolic_bp', diastolic_bp, 'mmHg'),
                ('bmi', round(bmi, 1), 'kg/m²'),
                ('glucose', round(glucose, 0), 'mg/dL')
            ]
            
            for obs_type, value, unit in obs_types:
                observation = Observation(
                    patient_id=patient_id,
                    observation_type=obs_type,
                    value=value,
                    unit=unit,
                    timestamp=timestamp,
                    provenance=ProvenanceType.SYNTHETIC,
                    data_source=DataSource.SYNTHETIC,
                    is_valid=True
                )
                observations.append(observation)
        
        observations.sort(key=lambda o: o.timestamp)
        return patient, observations
    
    def generate_low_risk_patient(self, patient_id: int) -> tuple[Patient, List[Observation]]:
        """Generate a synthetic patient with healthy metrics."""
        patient = self.generate_patient(is_synthetic=True, external_id="low_risk_demo")
        
        # Healthy profile
        base_heart_rate = random.randint(58, 72)
        base_systolic_bp = random.randint(105, 120)
        base_diastolic_bp = random.randint(65, 75)
        base_bmi = random.uniform(20.0, 24.0)
        base_glucose = random.uniform(80, 95)
        
        observations = []
        for i in range(60):
            timestamp = datetime.utcnow() - timedelta(days=i)
            
            heart_rate = base_heart_rate + random.randint(-4, 6)
            systolic_bp = base_systolic_bp + random.randint(-5, 8)
            diastolic_bp = base_diastolic_bp + random.randint(-4, 6)
            bmi = base_bmi + random.uniform(-0.4, 0.4)
            glucose = base_glucose + random.uniform(-6, 10)
            
            obs_types = [
                ('heart_rate', heart_rate, 'bpm'),
                ('systolic_bp', systolic_bp, 'mmHg'),
                ('diastolic_bp', diastolic_bp, 'mmHg'),
                ('bmi', round(bmi, 1), 'kg/m²'),
                ('glucose', round(glucose, 0), 'mg/dL')
            ]
            
            for obs_type, value, unit in obs_types:
                observation = Observation(
                    patient_id=patient_id,
                    observation_type=obs_type,
                    value=value,
                    unit=unit,
                    timestamp=timestamp,
                    provenance=ProvenanceType.SYNTHETIC,
                    data_source=DataSource.SYNTHETIC,
                    is_valid=True
                )
                observations.append(observation)
        
        observations.sort(key=lambda o: o.timestamp)
        return patient, observations
