"""
FHIR-compatible mapping module for patient and observation data.
"""
from typing import Dict, Any, Optional
from datetime import datetime
from domain.patient import Patient
from domain.observation import Observation


class FHIRMapper:
    """
    Maps local data models to FHIR-compatible JSON structures.
    
    Note: This provides simplified FHIR-compatible mappings for supported fields.
    It does not claim complete FHIR R4 compliance but follows FHIR resource patterns.
    """
    
    FHIR_VERSION = "4.0.1"
    
    @staticmethod
    def patient_to_fhir(patient: Patient) -> Dict[str, Any]:
        """
        Map Patient domain model to FHIR Patient resource.
        
        Returns: FHIR-compatible JSON structure
        """
        resource = {
            "resourceType": "Patient",
            "id": str(patient.id) if patient.id else None,
            "identifier": [
                {
                    "system": "https://swasthya-twin.org/patient-id",
                    "value": patient.external_id
                }
            ] if patient.external_id else [],
            "name": [
                {
                    "family": patient.last_name,
                    "given": [patient.first_name] if patient.first_name else []
                }
            ],
            "birthDate": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            "gender": patient.gender.value if patient.gender else "unknown",
            "meta": {
                "tag": [
                    {
                        "system": "https://swasthya-twin.org/data-source",
                        "code": "synthetic" if patient.is_synthetic else "real"
                    }
                ]
            }
        }
        
        # Remove None values
        return FHIRMapper._remove_none_values(resource)
    
    @staticmethod
    def observation_to_fhir(observation: Observation) -> Dict[str, Any]:
        """
        Map Observation domain model to FHIR Observation resource.
        
        Returns: FHIR-compatible JSON structure
        """
        # Map observation type to LOINC-like codes
        loinc_codes = {
            'heart_rate': '8867-4',
            'systolic_bp': '8480-6',
            'diastolic_bp': '8462-4',
            'bmi': '39156-5',
            'glucose': '2345-7',
            'activity_minutes': '41950-7',
            'sleep_hours': '93832-4'
        }
        
        loinc_code = loinc_codes.get(observation.observation_type, 'unknown')
        
        resource = {
            "resourceType": "Observation",
            "id": str(observation.id) if observation.id else None,
            "status": "final" if observation.is_valid else "cancelled",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                            "code": "vital-signs",
                            "display": "Vital Signs"
                        }
                    ]
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": loinc_code,
                        "display": observation.observation_type
                    }
                ],
                "text": observation.observation_type
            },
            "subject": {
                "reference": f"Patient/{observation.patient_id}"
            },
            "effectiveDateTime": observation.timestamp.isoformat() if observation.timestamp else None,
            "valueQuantity": {
                "value": observation.value,
                "unit": observation.unit,
                "system": "http://unitsofmeasure.org"
            } if observation.value is not None else None,
            "note": [
                {
                    "text": observation.notes
                }
            ] if observation.notes else [],
            "meta": {
                "tag": [
                    {
                        "system": "https://swasthya-twin.org/provenance",
                        "code": observation.provenance.value if observation.provenance else "manual"
                    },
                    {
                        "system": "https://swasthya-twin.org/data-source",
                        "code": observation.data_source.value if observation.data_source else "real"
                    }
                ]
            }
        }
        
        return FHIRMapper._remove_none_values(resource)
    
    @staticmethod
    def risk_assessment_to_fhir(risk_assessment) -> Dict[str, Any]:
        """
        Map RiskAssessment to FHIR RiskAssessment resource.
        
        Returns: FHIR-compatible JSON structure
        """
        resource = {
            "resourceType": "RiskAssessment",
            "status": "final",
            "subject": {
                "reference": f"Patient/{risk_assessment.patient_id}"
            },
            "condition": [
                {
                    "text": risk_assessment.target_condition
                }
            ],
            "prediction": [
                {
                    "outcome": {
                        "text": risk_assessment.target_condition
                    },
                    "probabilityDecimal": risk_assessment.risk_score,
                    "qualitativeRisk": {
                        "coding": [
                            {
                                "system": "https://swasthya-twin.org/risk-level",
                                "code": risk_assessment.risk_level.value if risk_assessment.risk_level else "unknown"
                            }
                        ]
                    }
                }
            ],
            "note": [
                {
                    "text": f"Model: {risk_assessment.model_name} v{risk_assessment.model_version}"
                }
            ]
        }
        
        return FHIRMapper._remove_none_values(resource)
    
    @staticmethod
    def create_bundle(resources: list, bundle_type: str = "collection") -> Dict[str, Any]:
        """
        Create a FHIR Bundle containing multiple resources.
        
        Args:
            resources: List of FHIR resource dictionaries
            bundle_type: Type of FHIR bundle (collection, document, message, etc.)
        
        Returns: FHIR Bundle resource
        """
        return {
            "resourceType": "Bundle",
            "type": bundle_type,
            "entry": [
                {
                    "resource": resource
                }
                for resource in resources
            ]
        }
    
    @staticmethod
    def _remove_none_values(obj: Any) -> Any:
        """Remove None values from dictionary recursively."""
        if not isinstance(obj, dict):
            return obj
        
        cleaned = {}
        for key, value in obj.items():
            if value is None:
                continue
            elif isinstance(value, dict):
                cleaned[key] = FHIRMapper._remove_none_values(value)
            elif isinstance(value, list):
                cleaned[key] = [
                    FHIRMapper._remove_none_values(item) if isinstance(item, dict) else item
                    for item in value
                    if item is not None
                ]
            else:
                cleaned[key] = value
        
        return cleaned
