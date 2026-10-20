"""
Scenario engine for hypothetical simulations.
"""
from typing import Dict, Optional
from domain.scenario import Scenario
from domain.digital_twin_state import DigitalTwinState, FeatureState
from domain.risk_assessment import RiskAssessment
from services.prediction_engine import PredictionEngine
import config


class ScenarioEngine:
    """Engine for running hypothetical scenario simulations."""
    
    def __init__(self, prediction_engine: Optional[PredictionEngine] = None):
        """Initialize scenario engine with prediction engine."""
        self.prediction_engine = prediction_engine or PredictionEngine()
    
    def run_scenario(self, scenario: Scenario, 
                    baseline_state: DigitalTwinState,
                    baseline_risk: RiskAssessment) -> Scenario:
        """
        Run a scenario simulation by modifying features and recomputing risk.
        
        Args:
            scenario: Scenario object with modifications
            baseline_state: Original Digital Twin state
            baseline_risk: Original risk assessment
        
        Returns:
            Updated scenario with computed results
        """
        # Store baseline values
        scenario.baseline_risk_score = baseline_risk.risk_score
        scenario.baseline_risk_level = baseline_risk.risk_level.value if baseline_risk.risk_level else None
        
        # Create modified state
        modified_state = self._apply_modifications(scenario, baseline_state)
        
        # Compute new risk assessment
        scenario_risk = self.prediction_engine.assess_risk(modified_state)
        
        scenario.scenario_risk_score = scenario_risk.risk_score
        scenario.scenario_risk_level = scenario_risk.risk_level.value if scenario_risk.risk_level else None
        scenario.status = scenario.status.__class__.COMPLETED
        
        return scenario
    
    def _apply_modifications(self, scenario: Scenario, 
                            baseline_state: DigitalTwinState) -> DigitalTwinState:
        """
        Apply scenario modifications to create a hypothetical state.
        
        This creates a new Digital Twin state with modified feature values
        while preserving baseline and trend information.
        """
        # Create a copy of the baseline state
        modified_state = DigitalTwinState(
            patient_id=baseline_state.patient_id,
            generated_at=baseline_state.generated_at
        )
        
        # Copy and modify features
        for feature_name, baseline_feature in baseline_state.features.items():
            # Create a copy of the feature state
            modified_feature = FeatureState(
                feature_name=feature_name,
                baseline_value=baseline_feature.baseline_value,
                current_value=baseline_feature.current_value,
                rolling_avg=baseline_feature.rolling_avg,
                change_from_baseline=baseline_feature.change_from_baseline,
                percent_change=baseline_feature.percent_change,
                trend=baseline_feature.trend,
                data_quality=baseline_feature.data_quality,
                last_observation=baseline_feature.last_observation,
                observation_count=baseline_feature.observation_count,
                days_since_last_observation=baseline_feature.days_since_last_observation
            )
            
            # Apply modification if exists for this feature
            if feature_name in scenario.modifications:
                modification = scenario.modifications[feature_name]
                modified_feature.current_value = modification.modified_value
                
                # Recalculate change from baseline
                if modified_feature.baseline_value is not None:
                    modified_feature.change_from_baseline = (
                        modification.modified_value - modified_feature.baseline_value
                    )
                    if modified_feature.baseline_value != 0:
                        modified_feature.percent_change = (
                            (modified_feature.change_from_baseline / modified_feature.baseline_value) * 100
                        )
            
            modified_state.add_feature(modified_feature)
        
        # Copy overall state metrics
        modified_state.overall_data_quality = baseline_state.overall_data_quality
        modified_state.total_observations = baseline_state.total_observations
        modified_state.data_freshness_days = baseline_state.data_freshness_days
        modified_state.completeness_score = baseline_state.completeness_score
        
        return modified_state
    
    def validate_modification(self, feature_name: str, value: float) -> tuple[bool, Optional[str]]:
        """
        Validate a scenario modification value.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if feature_name not in config.OBSERVATION_TYPES:
            return False, f"Unsupported feature: {feature_name}"
        
        type_config = config.OBSERVATION_TYPES[feature_name]
        
        if value < type_config['min'] or value > type_config['max']:
            return False, (
                f"Value {value} out of valid range "
                f"[{type_config['min']}, {type_config['max']}] for {feature_name}"
            )
        
        return True, None
    
    def suggest_improvements(self, baseline_state: DigitalTwinState,
                            baseline_risk: RiskAssessment) -> Dict[str, dict]:
        """
        Suggest hypothetical improvements based on current state.
        
        Returns:
            Dictionary of feature_name -> suggested_value dict
        """
        suggestions = {}
        
        # Suggest BP improvements if elevated
        systolic = baseline_state.get_feature('systolic_bp')
        if systolic and systolic.current_value and systolic.current_value > 120:
            suggestions['systolic_bp'] = {
                'current': systolic.current_value,
                'suggested': 120,
                'unit': 'mmHg',
                'reason': 'Reduce to normal range'
            }
        
        # Suggest heart rate improvements if elevated
        hr = baseline_state.get_feature('heart_rate')
        if hr and hr.current_value and hr.current_value > 85:
            suggestions['heart_rate'] = {
                'current': hr.current_value,
                'suggested': 70,
                'unit': 'bpm',
                'reason': 'Reduce to normal resting range'
            }
        
        # Suggest BMI improvements if overweight
        bmi = baseline_state.get_feature('bmi')
        if bmi and bmi.current_value and bmi.current_value > 25:
            suggestions['bmi'] = {
                'current': bmi.current_value,
                'suggested': 24.9,
                'unit': 'kg/m²',
                'reason': 'Reduce to normal weight range'
            }
        
        return suggestions
