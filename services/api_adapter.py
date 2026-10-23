"""
API Adapter Service - Transforms Flask domain models to React UI format.
This service bridges the gap between the existing Flask backend and the React frontend.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from domain import Patient, Observation, RiskAssessment
from domain.risk_assessment import FeatureContribution
from domain.scenario import Scenario
from repositories import PatientRepository, ObservationRepository

if TYPE_CHECKING:
    from domain.digital_twin_state import DigitalTwinState


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
        # Map risk level to classification - match React TypeScript types exactly
        # React types: 'Low Risk' | 'Borderline' | 'Moderate' | 'Elevated' | 'High Risk'
        # However, the actual UI uses: 'Low Risk' | 'Borderline' | 'Elevated' | 'High Risk'
        classification_map = {
            'low': 'Low Risk',
            'moderate': 'Elevated',  # Map moderate to Elevated (common in clinical risk stratification)
            'high': 'High Risk',
            'unknown': 'Low Risk'  # Default to Low Risk for unknown
        }
        classification = classification_map.get(risk.risk_level.value, 'Low Risk')

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

    @staticmethod
    def lifestyle_adjustments_to_scenario_modifications(
        adjustments: Dict[str, Any],
        baseline_state: 'DigitalTwinState'
    ) -> Dict[str, Dict[str, Any]]:
        """
        Translate React lifestyle adjustments to Flask scenario modifications.
        
        This uses clinical trial coefficients to estimate the impact of lifestyle
        interventions on physiological metrics, similar to the React mock calculations
        but server-side for consistency.
        
        Args:
            adjustments: Dict with keys like physicalActivityMinutesPerDay, sodiumReductionMg, etc.
            baseline_state: DigitalTwinState with current feature values
        
        Returns:
            Dict mapping feature names to modification dicts
        """
        modifications = {}
        
        # Get baseline values
        systolic_feature = baseline_state.get_feature('systolic_bp')
        glucose_feature = baseline_state.get_feature('glucose')
        hr_feature = baseline_state.get_feature('heart_rate')
        bmi_feature = baseline_state.get_feature('bmi')
        
        current_sbp = systolic_feature.current_value if systolic_feature else 130
        current_glucose = glucose_feature.current_value if glucose_feature else 105
        current_hr = hr_feature.current_value if hr_feature else 75
        current_bmi = bmi_feature.current_value if bmi_feature else 27.5
        
        # Extract adjustments with defaults
        activity_minutes = adjustments.get('physicalActivityMinutesPerDay', 0)
        sodium_reduction = adjustments.get('sodiumReductionMg', 0)
        sleep_hours = adjustments.get('sleepHours', 6.5)
        weight_reduction = adjustments.get('weightReductionKg', 0)
        diet_shift = adjustments.get('dietaryGlycemicIndexShift', 'none')
        
        # Calculate deltas based on clinical trial coefficients
        # (DASH, DPP, Look AHEAD meta-analyses)
        
        # 1. Aerobic activity effect (30 min/day yields ~4-6 mmHg SBP drop, -4-6 bpm RHR, -4-8 mg/dL glucose)
        activity_hours_ratio = activity_minutes / 30  # normalized to 30m increments
        delta_sbp_activity = -2.2 * min(2.5, activity_hours_ratio)
        delta_glucose_activity = -3.5 * min(2.5, activity_hours_ratio)
        delta_hr_activity = -2.0 * min(2.5, activity_hours_ratio)
        
        # 2. Sodium reduction effect (-1000mg Na -> -3 to -5 mmHg SBP)
        sodium_grams_reduced = sodium_reduction / 1000
        delta_sbp_sodium = -2.8 * sodium_grams_reduced
        
        # 3. Sleep optimization effect
        sleep_delta = sleep_hours - 6.5  # deviation from 6.5h deficit
        delta_sbp_sleep = -1.2 * min(2, sleep_delta) if sleep_delta > 0 else 1.5 * abs(sleep_delta)
        delta_glucose_sleep = -2.0 * min(2, sleep_delta) if sleep_delta > 0 else 3.0 * abs(sleep_delta)
        delta_hr_sleep = -1.5 * min(2, sleep_delta) if sleep_delta > 0 else 2.0
        
        # 4. Weight reduction effect (1kg loss -> ~1 mmHg SBP, ~1.5 mg/dL glucose)
        delta_sbp_weight = -1.1 * weight_reduction
        delta_glucose_weight = -1.6 * weight_reduction
        delta_bmi = -(weight_reduction / (1.75 * 1.75))  # approximate height 1.75m
        
        # 5. Dietary Glycemic Load shift
        delta_glucose_diet = 0
        if diet_shift == 'moderate_reduction':
            delta_glucose_diet = -4.0
        elif diet_shift == 'strict_low_gi':
            delta_glucose_diet = -8.5
        
        # Total projected shifts
        total_sbp_delta = round(delta_sbp_activity + delta_sbp_sodium + delta_sbp_sleep + delta_sbp_weight, 1)
        total_glucose_delta = round(delta_glucose_activity + delta_glucose_sleep + delta_glucose_weight + delta_glucose_diet, 1)
        total_hr_delta = round(delta_hr_activity + delta_hr_sleep, 1)
        total_bmi_delta = round(delta_bmi, 1)
        
        # Calculate simulated values
        simulated_sbp = max(95, round(current_sbp + total_sbp_delta))
        simulated_glucose = max(70, round(current_glucose + total_glucose_delta))
        simulated_hr = max(50, round(current_hr + total_hr_delta))
        simulated_bmi = max(19, round(current_bmi + total_bmi_delta, 1))
        
        # Build modifications dict
        modifications['systolic_bp'] = {
            'current': current_sbp,
            'suggested': simulated_sbp,
            'unit': 'mmHg',
            'delta': total_sbp_delta
        }
        
        modifications['glucose'] = {
            'current': current_glucose,
            'suggested': simulated_glucose,
            'unit': 'mg/dL',
            'delta': total_glucose_delta
        }
        
        modifications['heart_rate'] = {
            'current': current_hr,
            'suggested': simulated_hr,
            'unit': 'bpm',
            'delta': total_hr_delta
        }
        
        modifications['bmi'] = {
            'current': current_bmi,
            'suggested': simulated_bmi,
            'unit': 'kg/m²',
            'delta': total_bmi_delta
        }
        
        return modifications

    @staticmethod
    def scenario_to_react_format(scenario: Scenario, patient_external_id: str, baseline_risk: RiskAssessment) -> Dict[str, Any]:
        """Transform Flask Scenario to React ScenarioSimulationResult format."""
        # Build projected metrics from scenario modifications
        projected_metrics = []
        for feature_name, mod in scenario.modifications.items():
            # Map Flask feature names to React metric keys
            metric_key_map = {
                'systolic_bp': 'systolic_bp',
                'diastolic_bp': 'diastolic_bp',
                'heart_rate': 'resting_heart_rate',
                'glucose': 'fasting_glucose',
                'hba1c': 'hba1c',
                'ldl_cholesterol': 'ldl_cholesterol',
                'hdl_cholesterol': 'hdl_cholesterol',
                'total_cholesterol': 'total_cholesterol',
                'bmi': 'bmi',
                'egfr': 'egfr'
            }

            metric_key = metric_key_map.get(feature_name, feature_name)

            if mod.original_value is not None and mod.modified_value is not None:
                absolute_delta = mod.modified_value - mod.original_value
                percent_delta = (absolute_delta / mod.original_value * 100) if mod.original_value != 0 else 0

                projected_metrics.append({
                    'metricKey': metric_key,
                    'baselineValue': mod.original_value,
                    'simulatedValue': mod.modified_value,
                    'absoluteDelta': round(absolute_delta, 1),
                    'percentDelta': round(percent_delta, 1),
                    'unit': mod.unit,
                    'clinicalSignificance': 'Hypothetical projection based on Flask scenario engine using clinical trial coefficients (DASH, DPP, Look AHEAD).'
                })

        # Build projected risk changes
        baseline_score = baseline_risk.risk_score or 0
        scenario_score = scenario.scenario_risk_score or 0
        percent_reduction = ((baseline_score - scenario_score) / baseline_score * 100) if baseline_score > 0 else 0

        projected_risk_changes = [
            {
                'assessmentType': 'Cardiovascular Risk',
                'baselineScore': round(baseline_score * 100, 1),
                'projectedScore': round(scenario_score * 100, 1),
                'percentReduction': round(percent_reduction, 1)
            }
        ]

        return {
            'scenarioName': scenario.name,
            'patientId': patient_external_id,
            'projectedMetrics': projected_metrics,
            'projectedRiskChanges': projected_risk_changes,
            'evidenceCitations': [
                {
                    'study': 'Flask Scenario Engine with Clinical Trial Coefficients',
                    'finding': 'Server-side simulation using patient baseline data and lifestyle intervention coefficients derived from DASH-Sodium, Diabetes Prevention Program, and Look AHEAD trial meta-analyses.'
                }
            ]
        }
