"""
API Adapter Service - Transforms Flask domain models to React UI format.
This service bridges the gap between the existing Flask backend and the React frontend.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from domain import Patient, Observation, RiskAssessment
from domain.risk_assessment import FeatureContribution
from repositories import PatientRepository, ObservationRepository


class APIAdapter:
    """Adapts Flask backend responses to React UI expected format."""

    @staticmethod
    def patient_to_react_format(patient: Patient) -> Dict[str, Any]:
        """Transform Flask Patient to React PatientProfile format."""
        birth_year = patient.date_of_birth.year if patient.date_of_birth else 1980
        sex_at_birth = 'Male' if patient.gender.value == 'male' else 'Female' if patient.gender.value == 'female' else 'Other'

        # Map monitoring status based on observation count and age
        monitoring_status = 'Baseline Established'
        if patient.is_synthetic:
            monitoring_status = 'Baseline Established'

        return {
            'id': patient.external_id or f'DEMO-{str(patient.id).zfill(3)}',
            'birthYear': birth_year,
            'sexAtBirth': sex_at_birth,
            'monitoringStatus': monitoring_status,
            'primaryFocus': 'Cardiometabolic & Blood Pressure Modulation',
            'enrolledDate': patient.created_at.strftime('%Y-%m-%d') if patient.created_at else '2026-01-15',
            'baselineWindowDays': 60,
            'smokerStatus': 'Non-Smoker',
            'notes': f'Synthetic demonstration patient. {patient.full_name}'
        }

    @staticmethod
    def observation_to_react_format(observation: Observation, patient_external_id: str) -> Dict[str, Any]:
        """Transform Flask Observation to React Observation format."""
        # Map observation_type to metricKey
        metric_key_map = {
            'heart_rate': 'resting_heart_rate',
            'systolic_bp': 'systolic_bp',
            'diastolic_bp': 'diastolic_bp',
            'bmi': 'bmi',
            'glucose': 'fasting_glucose',
            'hba1c': 'hba1c',
            'ldl_cholesterol': 'ldl_cholesterol',
            'hdl_cholesterol': 'hdl_cholesterol',
            'total_cholesterol': 'total_cholesterol',
            'egfr': 'egfr'
        }

        metric_key = metric_key_map.get(observation.observation_type, observation.observation_type)

        # Determine category
        category_map = {
            'heart_rate': 'cardiovascular',
            'systolic_bp': 'cardiovascular',
            'diastolic_bp': 'cardiovascular',
            'bmi': 'anthropometric',
            'glucose': 'metabolic',
            'hba1c': 'metabolic',
            'ldl_cholesterol': 'metabolic',
            'hdl_cholesterol': 'metabolic',
            'total_cholesterol': 'metabolic',
            'egfr': 'metabolic'
        }
        category = category_map.get(observation.observation_type, 'telemetry')

        return {
            'id': f'obs-{patient_external_id}-{observation.id}',
            'patientId': patient_external_id,
            'recordedAt': observation.timestamp.strftime('%Y-%m-%d') if observation.timestamp else datetime.utcnow().strftime('%Y-%m-%d'),
            'metricKey': metric_key,
            'value': observation.value if observation.value is not None else 0,
            'unit': observation.unit,
            'category': category,
            'contextNotes': observation.notes or 'Routine observation',
            'isSynthetic': observation.is_synthetic
        }

    @staticmethod
    def risk_assessment_to_react_format(risk: RiskAssessment, patient_external_id: str) -> Dict[str, Any]:
        """Transform Flask RiskAssessment to React RiskAssessment format."""
        # Map risk level to classification
        classification_map = {
            'low': 'Low Risk',
            'moderate': 'Elevated',
            'high': 'High Risk',
            'unknown': 'Insufficient Data'
        }
        classification = classification_map.get(risk.risk_level.value, 'Unknown')

        # Convert feature contributions
        contributing_factors = []
        for fc in risk.feature_contributions:
            contributing_factors.append({
                'factor': fc.feature_name.replace('_', ' ').title(),
                'contributionPercent': int(abs(fc.contribution_value) * 100),
                'observedValue': f"{fc.current_value:.1f}" if fc.current_value else 'N/A',
                'baselineComparison': f"Baseline: {fc.baseline_value:.1f}" if fc.baseline_value else 'N/A',
                'impactLevel': 'high' if abs(fc.contribution_value) > 0.5 else 'moderate' if abs(fc.contribution_value) > 0.2 else 'low'
            })

        # Determine assessment type
        assessment_type = 'cardiovascular_10yr'
        if 'glucose' in [fc.feature_name for fc in risk.feature_contributions]:
            assessment_type = 'diabetes_progression'
        else:
            assessment_type = 'metabolic_burden'

        return {
            'id': f'risk-{patient_external_id}-{assessment_type}',
            'patientId': patient_external_id,
            'assessmentType': assessment_type,
            'title': f'{assessment_type.replace("_", " ").title()} Risk Screening',
            'category': 'Cardiovascular' if 'cardiovascular' in assessment_type else 'Metabolic',
            'scorePercent': int((risk.risk_score or 0) * 100),
            'classification': classification,
            'methodologyDescription': f'Rules-based screening using {risk.model_name} v{risk.model_version}',
            'contributingFactors': contributing_factors,
            'missingInputs': [],
            'dataCompletenessPercent': int(risk.confidence * 100) if risk.confidence else 70,
            'clinicalDisclaimer': 'This is a research prototype, not a clinical diagnostic tool.'
        }

    @staticmethod
    def get_metric_definitions() -> Dict[str, Dict[str, Any]]:
        """Return metric definitions matching React UI format."""
        return {
            'systolic_bp': {
                'key': 'systolic_bp',
                'label': 'Systolic Blood Pressure',
                'shortLabel': 'Systolic BP',
                'unit': 'mmHg',
                'category': 'cardiovascular',
                'normalMin': 90,
                'normalMax': 120,
                'optimalTarget': '< 120 mmHg',
                'decimals': 0,
                'description': 'Pressure in blood vessels during cardiac contraction.',
                'clinicalRelevance': 'Primary marker for hypertension stage and stroke risk screening.'
            },
            'diastolic_bp': {
                'key': 'diastolic_bp',
                'label': 'Diastolic Blood Pressure',
                'shortLabel': 'Diastolic BP',
                'unit': 'mmHg',
                'category': 'cardiovascular',
                'normalMin': 60,
                'normalMax': 80,
                'optimalTarget': '< 80 mmHg',
                'decimals': 0,
                'description': 'Pressure in arteries between heartbeats.',
                'clinicalRelevance': 'Indicates vascular tone and peripheral vascular resistance.'
            },
            'fasting_glucose': {
                'key': 'fasting_glucose',
                'label': 'Fasting Blood Glucose',
                'shortLabel': 'Fasting Glucose',
                'unit': 'mg/dL',
                'category': 'metabolic',
                'normalMin': 70,
                'normalMax': 99,
                'optimalTarget': '70–99 mg/dL',
                'decimals': 0,
                'description': 'Blood sugar level after an overnight minimum 8-hour fast.',
                'clinicalRelevance': 'Screening index for impaired fasting glucose and insulin sensitivity.'
            },
            'hba1c': {
                'key': 'hba1c',
                'label': 'Glycated Hemoglobin',
                'shortLabel': 'HbA1c',
                'unit': '%',
                'category': 'metabolic',
                'normalMin': 4.0,
                'normalMax': 5.6,
                'optimalTarget': '< 5.7 %',
                'decimals': 1,
                'description': 'Average blood sugar concentration over the past 90 days.',
                'clinicalRelevance': 'Standard diagnostic biomarker for glycemic control.'
            },
            'resting_heart_rate': {
                'key': 'resting_heart_rate',
                'label': 'Resting Heart Rate',
                'shortLabel': 'Resting HR',
                'unit': 'bpm',
                'category': 'cardiovascular',
                'normalMin': 60,
                'normalMax': 80,
                'optimalTarget': '60–75 bpm',
                'decimals': 0,
                'description': 'Beats per minute while in a relaxed, awake state.',
                'clinicalRelevance': 'Inverse indicator of autonomic fitness and cardiovascular stress.'
            },
            'ldl_cholesterol': {
                'key': 'ldl_cholesterol',
                'label': 'LDL Cholesterol',
                'shortLabel': 'LDL-C',
                'unit': 'mg/dL',
                'category': 'metabolic',
                'normalMin': 50,
                'normalMax': 99,
                'optimalTarget': '< 100 mg/dL',
                'decimals': 0,
                'description': 'Low-density lipoprotein cholesterol fraction.',
                'clinicalRelevance': 'Primary atherogenic lipoprotein contributing to arterial plaque.'
            },
            'hdl_cholesterol': {
                'key': 'hdl_cholesterol',
                'label': 'HDL Cholesterol',
                'shortLabel': 'HDL-C',
                'unit': 'mg/dL',
                'category': 'metabolic',
                'normalMin': 40,
                'normalMax': 70,
                'optimalTarget': '> 50 mg/dL',
                'decimals': 0,
                'description': 'High-density lipoprotein involved in reverse cholesterol transport.',
                'clinicalRelevance': 'Protective lipid fraction against cardiovascular event recurrence.'
            },
            'total_cholesterol': {
                'key': 'total_cholesterol',
                'label': 'Total Serum Cholesterol',
                'shortLabel': 'Total Chol',
                'unit': 'mg/dL',
                'category': 'metabolic',
                'normalMin': 125,
                'normalMax': 199,
                'optimalTarget': '< 200 mg/dL',
                'decimals': 0,
                'description': 'Total concentration of circulating lipoproteins.',
                'clinicalRelevance': 'Used in composite cardiovascular 10-year risk calculators.'
            },
            'bmi': {
                'key': 'bmi',
                'label': 'Body Mass Index',
                'shortLabel': 'BMI',
                'unit': 'kg/m²',
                'category': 'anthropometric',
                'normalMin': 18.5,
                'normalMax': 24.9,
                'optimalTarget': '18.5–24.9',
                'decimals': 1,
                'description': 'Anthropometric ratio of body mass to square of stature.',
                'clinicalRelevance': 'Surrogate indicator of adiposity and metabolic burden.'
            },
            'egfr': {
                'key': 'egfr',
                'label': 'Estimated Glomerular Filtration Rate',
                'shortLabel': 'eGFR',
                'unit': 'mL/min/1.73m²',
                'category': 'metabolic',
                'normalMin': 90,
                'normalMax': 120,
                'optimalTarget': '> 90 mL/min',
                'decimals': 0,
                'description': 'Calculated index of renal filtration capacity from serum creatinine.',
                'clinicalRelevance': 'Critical for staging renal health and monitoring microvascular strain.'
            }
        }
