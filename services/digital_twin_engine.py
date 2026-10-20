"""
Digital Twin state engine for computing patient state.
"""
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from statistics import mean, stdev
from domain.observation import Observation
from domain.digital_twin_state import DigitalTwinState, FeatureState, DataQuality
from repositories.observation_repository import ObservationRepository
import config


class DigitalTwinEngine:
    """Engine for computing Digital Twin state from observations."""
    
    def __init__(self, observation_repo: ObservationRepository):
        """Initialize engine with observation repository."""
        self.obs_repo = observation_repo
        self.min_observations_for_baseline = config.MIN_OBSERVATIONS_FOR_BASELINE
        self.min_observations_for_trend = config.MIN_OBSERVATIONS_FOR_TREND
        self.rolling_window_days = config.ROLLING_WINDOW_DAYS
    
    def compute_state(self, patient_id: int) -> DigitalTwinState:
        """
        Compute the complete Digital Twin state for a patient.
        
        Args:
            patient_id: Patient ID to compute state for
        
        Returns:
            DigitalTwinState object with computed features
        """
        state = DigitalTwinState(patient_id=patient_id)
        
        # Get all observations for patient
        observations = self.obs_repo.get_by_patient(patient_id)
        valid_observations = [obs for obs in observations if obs.is_valid]
        
        state.total_observations = len(valid_observations)
        
        # Group observations by type
        obs_by_type = self._group_by_type(valid_observations)
        
        # Compute state for each feature
        for obs_type, type_observations in obs_by_type.items():
            feature_state = self._compute_feature_state(obs_type, type_observations)
            state.add_feature(feature_state)
        
        # Compute overall metrics
        state.overall_data_quality = self._compute_overall_quality(state.features)
        state.data_freshness_days = self._compute_data_freshness(valid_observations)
        state.completeness_score = self._compute_completeness_score(state.features)
        
        return state
    
    def _group_by_type(self, observations: List[Observation]) -> Dict[str, List[Observation]]:
        """Group observations by observation type."""
        grouped = {}
        for obs in observations:
            if obs.observation_type not in grouped:
                grouped[obs.observation_type] = []
            grouped[obs.observation_type].append(obs)
        return grouped
    
    def _compute_feature_state(self, feature_name: str, 
                              observations: List[Observation]) -> FeatureState:
        """Compute state for a single feature."""
        # Sort by timestamp
        sorted_obs = sorted(observations, key=lambda o: o.timestamp)
        
        state = FeatureState(feature_name=feature_name)
        state.observation_count = len(sorted_obs)
        
        if not sorted_obs:
            return state
        
        # Most recent value
        latest = sorted_obs[-1]
        state.current_value = latest.value
        state.last_observation = latest.timestamp
        
        # Calculate days since last observation
        if state.last_observation:
            state.days_since_last_observation = (datetime.utcnow() - state.last_observation).days
        
        # Baseline: average of first N observations
        if len(sorted_obs) >= self.min_observations_for_baseline:
            baseline_obs = sorted_obs[:self.min_observations_for_baseline]
            baseline_values = [o.value for o in baseline_obs if o.value is not None]
            if baseline_values:
                state.baseline_value = mean(baseline_values)
        
        # Rolling average (last 30 days)
        if state.last_observation:
            cutoff_date = state.last_observation - timedelta(days=self.rolling_window_days)
            recent_obs = [o for o in sorted_obs if o.timestamp >= cutoff_date]
            recent_values = [o.value for o in recent_obs if o.value is not None]
            if recent_values:
                state.rolling_avg = mean(recent_values)
        
        # Change from baseline
        if state.baseline_value is not None and state.current_value is not None:
            state.change_from_baseline = state.current_value - state.baseline_value
            if state.baseline_value != 0:
                state.percent_change = (state.change_from_baseline / state.baseline_value) * 100
        
        # Trend analysis
        if len(sorted_obs) >= self.min_observations_for_trend:
            state.trend = self._compute_trend(sorted_obs)
        
        # Data quality assessment
        state.data_quality = self._assess_feature_quality(state)
        
        return state
    
    def _compute_trend(self, observations: List[Observation]) -> str:
        """
        Compute trend direction from observations.
        
        Returns: 'increasing', 'decreasing', 'stable', or 'unknown'
        """
        values = [o.value for o in observations if o.value is not None]
        
        if len(values) < 3:
            return 'unknown'
        
        # Simple linear regression slope
        n = len(values)
        x = list(range(n))
        
        # Calculate slope
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(xi * yi for xi, yi in zip(x, values))
        sum_x2 = sum(xi * xi for xi in x)
        
        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            return 'unknown'
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        
        # Determine trend based on slope
        if abs(slope) < 0.01:
            return 'stable'
        elif slope > 0:
            return 'increasing'
        else:
            return 'decreasing'
    
    def _assess_feature_quality(self, state: FeatureState) -> DataQuality:
        """Assess data quality for a feature."""
        if state.observation_count == 0:
            return DataQuality.INSUFFICIENT
        
        if state.observation_count < self.min_observations_for_baseline:
            return DataQuality.POOR
        
        if state.days_since_last_observation is None:
            return DataQuality.FAIR
        
        if state.days_since_last_observation > 90:
            return DataQuality.POOR
        elif state.days_since_last_observation > 30:
            return DataQuality.FAIR
        elif state.days_since_last_observation > 7:
            return DataQuality.GOOD
        else:
            return DataQuality.EXCELLENT
    
    def _compute_overall_quality(self, features: Dict[str, FeatureState]) -> DataQuality:
        """Compute overall data quality from all features."""
        if not features:
            return DataQuality.INSUFFICIENT
        
        quality_scores = {
            DataQuality.EXCELLENT: 4,
            DataQuality.GOOD: 3,
            DataQuality.FAIR: 2,
            DataQuality.POOR: 1,
            DataQuality.INSUFFICIENT: 0
        }
        
        total_score = sum(quality_scores.get(f.data_quality, 0) for f in features.values())
        avg_score = total_score / len(features)
        
        if avg_score >= 3.5:
            return DataQuality.EXCELLENT
        elif avg_score >= 2.5:
            return DataQuality.GOOD
        elif avg_score >= 1.5:
            return DataQuality.FAIR
        elif avg_score >= 0.5:
            return DataQuality.POOR
        else:
            return DataQuality.INSUFFICIENT
    
    def _compute_data_freshness(self, observations: List[Observation]) -> Optional[int]:
        """Compute days since most recent observation."""
        if not observations:
            return None
        
        latest = max(observations, key=lambda o: o.timestamp)
        return (datetime.utcnow() - latest.timestamp).days
    
    def _compute_completeness_score(self, features: Dict[str, FeatureState]) -> float:
        """
        Compute completeness score (0.0 to 1.0).
        
        Based on how many observation types have sufficient data.
        """
        if not features:
            return 0.0
        
        sufficient_count = sum(
            1 for f in features.values() 
            if f.observation_count >= self.min_observations_for_baseline
        )
        
        return sufficient_count / len(features)
