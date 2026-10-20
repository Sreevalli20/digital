"""
Prediction engine for risk assessment.
"""
from typing import List, Optional
from domain.digital_twin_state import DigitalTwinState, FeatureState
from domain.risk_assessment import RiskAssessment, RiskLevel, FeatureContribution
import config


class PredictionEngine:
    """
    Rules-based prediction engine for cardiometabolic risk estimation.
    
    This engine uses personalized thresholds based on individual baselines
    and evidence-based clinical guidelines for risk factor assessment.
    """
    
    def __init__(self):
        """Initialize prediction engine."""
        self.model_name = config.MODEL_NAME
        self.model_version = config.MODEL_VERSION
        self.model_type = config.MODEL_TYPE
        self.high_risk_threshold = config.HIGH_RISK_THRESHOLD
        self.moderate_risk_threshold = config.MODERATE_RISK_THRESHOLD
    
    def assess_risk(self, twin_state: DigitalTwinState) -> RiskAssessment:
        """
        Assess cardiometabolic risk based on Digital Twin state.
        
        Args:
            twin_state: Current Digital Twin state for the patient
        
        Returns:
            RiskAssessment with computed risk level and explanations
        """
        assessment = RiskAssessment(
            patient_id=twin_state.patient_id,
            model_name=self.model_name,
            model_version=self.model_version
        )
        
        # Check if sufficient data is available
        if twin_state.overall_data_quality.value in ['insufficient', 'poor']:
            assessment.is_insufficient_data = True
            assessment.insufficient_data_reason = (
                f"Insufficient data quality: {twin_state.overall_data_quality.value}. "
                f"Need at least {config.MIN_OBSERVATIONS_FOR_BASELINE} observations per feature."
            )
            return assessment
        
        # Compute risk score from features
        risk_score, contributions = self._compute_risk_score(twin_state)
        
        assessment.risk_score = risk_score
        assessment.feature_contributions = contributions
        
        # Determine risk level
        if risk_score >= self.high_risk_threshold:
            assessment.risk_level = RiskLevel.HIGH
        elif risk_score >= self.moderate_risk_threshold:
            assessment.risk_level = RiskLevel.MODERATE
        else:
            assessment.risk_level = RiskLevel.LOW
        
        # Set data quality status
        assessment.data_quality_status = twin_state.overall_data_quality.value
        
        # Set confidence based on data quality
        assessment.confidence = self._compute_confidence(twin_state)
        
        # Add limitations
        assessment.limitations = [
            "This is a rules-based screening tool, not a clinical diagnostic.",
            "Risk estimates are based on available observations and may not reflect complete clinical picture.",
            "Individual factors not captured in observations may affect actual risk.",
            "This model has not been validated for clinical diagnosis or treatment decisions.",
            "Consult a healthcare professional for medical advice."
        ]
        
        return assessment
    
    def _compute_risk_score(self, twin_state: DigitalTwinState) -> tuple[float, List[FeatureContribution]]:
        """
        Compute risk score from Digital Twin state features.
        
        Returns:
            Tuple of (risk_score, list_of_feature_contributions)
        """
        contributions = []
        total_risk = 0.0
        max_possible_risk = 0.0
        
        # Blood pressure risk
        bp_risk, bp_contrib = self._assess_blood_pressure_risk(twin_state)
        if bp_contrib:
            contributions.append(bp_contrib)
            total_risk += bp_risk
            max_possible_risk += 0.3  # Max 30% from BP
        
        # Heart rate risk
        hr_risk, hr_contrib = self._assess_heart_rate_risk(twin_state)
        if hr_contrib:
            contributions.append(hr_contrib)
            total_risk += hr_risk
            max_possible_risk += 0.2  # Max 20% from HR
        
        # BMI risk
        bmi_risk, bmi_contrib = self._assess_bmi_risk(twin_state)
        if bmi_contrib:
            contributions.append(bmi_contrib)
            total_risk += bmi_risk
            max_possible_risk += 0.25  # Max 25% from BMI
        
        # Glucose risk
        glucose_risk, glucose_contrib = self._assess_glucose_risk(twin_state)
        if glucose_contrib:
            contributions.append(glucose_contrib)
            total_risk += glucose_risk
            max_possible_risk += 0.25  # Max 25% from glucose
        
        # Normalize to 0-1 range
        if max_possible_risk > 0:
            normalized_score = total_risk / max_possible_risk
        else:
            normalized_score = 0.0
        
        return min(normalized_score, 1.0), contributions
    
    def _assess_blood_pressure_risk(self, twin_state: DigitalTwinState) -> tuple[float, Optional[FeatureContribution]]:
        """Assess blood pressure risk contribution."""
        systolic = twin_state.get_feature('systolic_bp')
        diastolic = twin_state.get_feature('diastolic_bp')
        
        if not systolic or not diastolic:
            return 0.0, None
        
        if systolic.current_value is None or diastolic.current_value is None:
            return 0.0, None
        
        # Evidence-based BP thresholds
        systolic_value = systolic.current_value
        diastolic_value = diastolic.current_value
        
        risk = 0.0
        explanation = ""
        
        # Hypertension staging
        if systolic_value >= 140 or diastolic_value >= 90:
            risk = 0.8
            explanation = "Blood pressure in hypertensive range (Stage 2)"
        elif systolic_value >= 130 or diastolic_value >= 80:
            risk = 0.5
            explanation = "Blood pressure elevated (Stage 1)"
        elif systolic_value >= 120 and diastolic_value < 80:
            risk = 0.3
            explanation = "Blood pressure in elevated range"
        else:
            risk = 0.1
            explanation = "Blood pressure within normal range"
        
        # Adjust based on change from baseline
        if systolic.change_from_baseline and systolic.change_from_baseline > 10:
            risk = min(risk + 0.15, 1.0)
            explanation += f"; increased by {systolic.change_from_baseline:.1f} mmHg from baseline"
        
        contribution = FeatureContribution(
            feature_name='blood_pressure',
            contribution_value=risk,
            direction='increases_risk' if risk > 0.3 else 'decreases_risk',
            baseline_value=systolic.baseline_value,
            current_value=systolic_value,
            explanation=explanation
        )
        
        return risk * 0.3, contribution  # Max 30% contribution
    
    def _assess_heart_rate_risk(self, twin_state: DigitalTwinState) -> tuple[float, Optional[FeatureContribution]]:
        """Assess heart rate risk contribution."""
        hr = twin_state.get_feature('heart_rate')
        
        if not hr or hr.current_value is None:
            return 0.0, None
        
        hr_value = hr.current_value
        risk = 0.0
        explanation = ""
        
        # Resting heart rate thresholds
        if hr_value > 100:
            risk = 0.6
            explanation = "Elevated resting heart rate (tachycardia range)"
        elif hr_value > 85:
            risk = 0.4
            explanation = "Resting heart rate above normal range"
        elif hr_value < 50:
            risk = 0.3
            explanation = "Low resting heart rate (bradycardia range)"
        else:
            risk = 0.1
            explanation = "Resting heart rate within normal range"
        
        # Adjust based on change from baseline
        if hr.change_from_baseline and hr.change_from_baseline > 10:
            risk = min(risk + 0.1, 1.0)
            explanation += f"; increased by {hr.change_from_baseline:.1f} bpm from baseline"
        
        contribution = FeatureContribution(
            feature_name='heart_rate',
            contribution_value=risk,
            direction='increases_risk' if risk > 0.3 else 'decreases_risk',
            baseline_value=hr.baseline_value,
            current_value=hr_value,
            explanation=explanation
        )
        
        return risk * 0.2, contribution  # Max 20% contribution
    
    def _assess_bmi_risk(self, twin_state: DigitalTwinState) -> tuple[float, Optional[FeatureContribution]]:
        """Assess BMI risk contribution."""
        bmi = twin_state.get_feature('bmi')
        
        if not bmi or bmi.current_value is None:
            return 0.0, None
        
        bmi_value = bmi.current_value
        risk = 0.0
        explanation = ""
        
        # BMI categories
        if bmi_value >= 40:
            risk = 0.9
            explanation = "BMI in Class III obesity range"
        elif bmi_value >= 35:
            risk = 0.7
            explanation = "BMI in Class II obesity range"
        elif bmi_value >= 30:
            risk = 0.5
            explanation = "BMI in Class I obesity range"
        elif bmi_value >= 25:
            risk = 0.3
            explanation = "BMI in overweight range"
        elif bmi_value < 18.5:
            risk = 0.2
            explanation = "BMI in underweight range"
        else:
            risk = 0.1
            explanation = "BMI within normal range"
        
        contribution = FeatureContribution(
            feature_name='bmi',
            contribution_value=risk,
            direction='increases_risk' if risk > 0.3 else 'decreases_risk',
            baseline_value=bmi.baseline_value,
            current_value=bmi_value,
            explanation=explanation
        )
        
        return risk * 0.25, contribution  # Max 25% contribution
    
    def _assess_glucose_risk(self, twin_state: DigitalTwinState) -> tuple[float, Optional[FeatureContribution]]:
        """Assess glucose risk contribution."""
        glucose = twin_state.get_feature('glucose')
        
        if not glucose or glucose.current_value is None:
            return 0.0, None
        
        glucose_value = glucose.current_value
        risk = 0.0
        explanation = ""
        
        # Fasting glucose thresholds
        if glucose_value >= 126:
            risk = 0.9
            explanation = "Glucose in diabetic range"
        elif glucose_value >= 100:
            risk = 0.5
            explanation = "Glucose in prediabetic range"
        else:
            risk = 0.1
            explanation = "Glucose within normal range"
        
        contribution = FeatureContribution(
            feature_name='glucose',
            contribution_value=risk,
            direction='increases_risk' if risk > 0.3 else 'decreases_risk',
            baseline_value=glucose.baseline_value,
            current_value=glucose_value,
            explanation=explanation
        )
        
        return risk * 0.25, contribution  # Max 25% contribution
    
    def _compute_confidence(self, twin_state: DigitalTwinState) -> float:
        """
        Compute confidence score based on data quality and completeness.
        
        Returns: Confidence score between 0.0 and 1.0
        """
        quality_scores = {
            'excellent': 0.9,
            'good': 0.7,
            'fair': 0.5,
            'poor': 0.3,
            'insufficient': 0.1
        }
        
        base_confidence = quality_scores.get(twin_state.overall_data_quality.value, 0.5)
        
        # Adjust by completeness
        completeness_adjustment = twin_state.completeness_score * 0.2
        
        return min(base_confidence + completeness_adjustment, 1.0)
