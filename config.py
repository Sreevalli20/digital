"""
Application configuration for Swasthya Twin Digital Twin.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Database
DATABASE_PATH = os.environ.get('DATABASE_PATH', str(BASE_DIR / 'instance' / 'swasthya.db'))
DATABASE_DIR = os.path.dirname(DATABASE_PATH)

# Ensure database directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
TESTING = os.environ.get('TESTING', 'False').lower() == 'true'

# Upload configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', str(BASE_DIR / 'uploads'))
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
ALLOWED_EXTENSIONS = {'csv'}

# Data quality thresholds
MIN_OBSERVATIONS_FOR_BASELINE = 3
MIN_OBSERVATIONS_FOR_TREND = 5
ROLLING_WINDOW_DAYS = 30

# Risk thresholds
HIGH_RISK_THRESHOLD = 0.7
MODERATE_RISK_THRESHOLD = 0.4

# Supported observation types with units and ranges
OBSERVATION_TYPES = {
    'heart_rate': {
        'name': 'Resting Heart Rate',
        'unit': 'bpm',
        'min': 30,
        'max': 200,
        'display_precision': 0
    },
    'systolic_bp': {
        'name': 'Systolic Blood Pressure',
        'unit': 'mmHg',
        'min': 70,
        'max': 250,
        'display_precision': 0
    },
    'diastolic_bp': {
        'name': 'Diastolic Blood Pressure',
        'unit': 'mmHg',
        'min': 40,
        'max': 150,
        'display_precision': 0
    },
    'bmi': {
        'name': 'Body Mass Index',
        'unit': 'kg/m²',
        'min': 10,
        'max': 60,
        'display_precision': 1
    },
    'glucose': {
        'name': 'Blood Glucose',
        'unit': 'mg/dL',
        'min': 30,
        'max': 600,
        'display_precision': 0
    },
    'activity_minutes': {
        'name': 'Physical Activity',
        'unit': 'minutes',
        'min': 0,
        'max': 300,
        'display_precision': 0
    },
    'sleep_hours': {
        'name': 'Sleep Duration',
        'unit': 'hours',
        'min': 0,
        'max': 24,
        'display_precision': 1
    }
}

# Provenance types
PROVENANCE_MANUAL = 'manual'
PROVENANCE_CSV_IMPORT = 'csv_import'
PROVENANCE_SYNTHETIC = 'synthetic'
PROVENANCE_WEARABLE = 'wearable'
PROVENANCE_SCENARIO = 'scenario'

# Data source types
DATA_SOURCE_REAL = 'real'
DATA_SOURCE_SYNTHETIC = 'synthetic'
DATA_SOURCE_IMPORTED = 'imported'

# Model configuration
MODEL_VERSION = '1.0.0'
MODEL_NAME = 'Cardiometabolic Risk Estimator'
MODEL_TYPE = 'rules_based_with_personalization'

# Export configuration
EXPORT_FORMATS = ['json', 'csv']
