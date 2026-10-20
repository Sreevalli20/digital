"""
CSV ingestion service for importing observation data.
"""
import csv
import io
from typing import List, Tuple, Optional
from datetime import datetime
from domain.observation import Observation, ProvenanceType, DataSource
from services.observation_validator import ObservationValidator
import config


class CSVIngestionService:
    """Service for ingesting observation data from CSV files."""
    
    REQUIRED_COLUMNS = ['patient_id', 'observation_type', 'value', 'unit', 'timestamp']
    OPTIONAL_COLUMNS = ['notes']
    
    def __init__(self, validator: Optional[ObservationValidator] = None):
        """Initialize ingestion service with validator."""
        self.validator = validator or ObservationValidator()
    
    def parse_csv(self, csv_content: str, patient_id: Optional[int] = None) -> Tuple[List[Observation], List[str]]:
        """
        Parse CSV content into observations.
        
        Args:
            csv_content: CSV file content as string
            patient_id: Optional patient ID to override CSV patient_id column
        
        Returns:
            Tuple of (observations, error_messages)
        """
        observations = []
        errors = []
        
        try:
            csv_file = io.StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            # Validate columns
            if not all(col in reader.fieldnames for col in self.REQUIRED_COLUMNS):
                missing = [col for col in self.REQUIRED_COLUMNS if col not in reader.fieldnames]
                errors.append(f"Missing required columns: {', '.join(missing)}")
                return observations, errors
            
            row_num = 0
            for row in reader:
                row_num += 1
                
                try:
                    # Parse timestamp
                    timestamp = self._parse_timestamp(row['timestamp'])
                    if not timestamp:
                        errors.append(f"Row {row_num}: Invalid timestamp format")
                        continue
                    
                    # Parse value
                    try:
                        value = float(row['value']) if row['value'] else None
                    except ValueError:
                        errors.append(f"Row {row_num}: Invalid value format")
                        continue
                    
                    # Use provided patient_id or CSV patient_id
                    pid = patient_id or int(row['patient_id'])
                    
                    observation = Observation(
                        patient_id=pid,
                        observation_type=row['observation_type'],
                        value=value,
                        unit=row['unit'],
                        timestamp=timestamp,
                        provenance=ProvenanceType.CSV_IMPORT,
                        data_source=DataSource.IMPORTED,
                        notes=row.get('notes')
                    )
                    
                    observations.append(observation)
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                    continue
            
        except Exception as e:
            errors.append(f"CSV parsing error: {str(e)}")
        
        return observations, errors
    
    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """Parse timestamp string into datetime object."""
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d',
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y',
            '%m/%d/%Y %H:%M:%S',
            '%m/%d/%Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def validate_and_ingest(self, observations: List[Observation]) -> Tuple[List[Observation], List[str]]:
        """
        Validate observations and return valid ones with error messages.
        
        Returns:
            Tuple of (valid_observations, error_messages)
        """
        validated = self.validator.validate_batch(observations)
        
        valid = [obs for obs in validated if obs.is_valid]
        invalid_errors = [
            f"Observation {i}: {obs.validation_error}" 
            for i, obs in enumerate(validated) 
            if not obs.is_valid
        ]
        
        return valid, invalid_errors
    
    def check_duplicates_in_batch(self, observations: List[Observation]) -> List[Tuple[int, int]]:
        """Check for duplicate observations within the batch."""
        return self.validator.check_duplicates(observations)
    
    def generate_example_csv(self) -> str:
        """Generate an example CSV template."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.REQUIRED_COLUMNS + self.OPTIONAL_COLUMNS)
        writer.writeheader()
        
        # Add example rows
        examples = [
            {
                'patient_id': '1',
                'observation_type': 'heart_rate',
                'value': '72',
                'unit': 'bpm',
                'timestamp': '2024-01-15 08:00:00',
                'notes': 'Morning measurement'
            },
            {
                'patient_id': '1',
                'observation_type': 'systolic_bp',
                'value': '120',
                'unit': 'mmHg',
                'timestamp': '2024-01-15 08:00:00',
                'notes': ''
            },
            {
                'patient_id': '1',
                'observation_type': 'diastolic_bp',
                'value': '80',
                'unit': 'mmHg',
                'timestamp': '2024-01-15 08:00:00',
                'notes': ''
            }
        ]
        
        for example in examples:
            writer.writerow(example)
        
        return output.getvalue()
