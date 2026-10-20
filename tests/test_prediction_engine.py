"""
Tests for prediction engine.
"""
import pytest
from services.prediction_engine import PredictionEngine
from domain.digital_twin_state import DigitalTwinState, FeatureState, DataQuality


@pytest.fixture
def prediction_engine():
    """Create prediction engine fixture."""
    return PredictionEngine()


def test_assess_risk_insufficient_data(prediction_engine):
    """Test risk assessment with insufficient data."""
    state = DigitalTwinState(patient_id=1)
    state.overall_data_quality = DataQuality.INSUFFICIENT
    
    risk = prediction_engine.assess_risk(state)
    
    assert risk.is_insufficient_data is True
    assert risk.insufficient_data_reason is not None


def test_assess_risk_with_data(prediction_engine):
    """Test risk assessment with sufficient data."""
    state = DigitalTwinState(patient_id=1)
    state.overall_data_quality = DataQuality.GOOD
    
    # Add feature states
    hr_state = FeatureState(
        feature_name='heart_rate',
        current_value=72.0,
        baseline_value=70.0,
        data_quality=DataQuality.GOOD
    )
    state.add_feature(hr_state)
    
    bp_state = FeatureState(
        feature_name='systolic_bp',
        current_value=120.0,
        baseline_value=118.0,
        data_quality=DataQuality.GOOD
    )
    state.add_feature(bp_state)
    
    risk = prediction_engine.assess_risk(state)
    
    assert risk.is_insufficient_data is False
    assert risk.risk_score is not None
    assert risk.risk_level is not None
    assert len(risk.feature_contributions) > 0


def test_high_risk_detection(prediction_engine):
    """Test detection of high risk factors."""
    state = DigitalTwinState(patient_id=1)
    state.overall_data_quality = DataQuality.GOOD
    
    # Add high-risk feature states
    hr_state = FeatureState(
        feature_name='heart_rate',
        current_value=95.0,  # Elevated
        baseline_value=70.0,
        data_quality=DataQuality.GOOD
    )
    state.add_feature(hr_state)
    
    bp_state = FeatureState(
        feature_name='systolic_bp',
        current_value=150.0,  # High
        baseline_value=120.0,
        data_quality=DataQuality.GOOD
    )
    state.add_feature(bp_state)
    
    risk = prediction_engine.assess_risk(state)
    
    assert risk.risk_score is not None
    # High BP and HR should contribute to risk


def test_low_risk_detection(prediction_engine):
    """Test detection of low risk factors."""
    state = DigitalTwinState(patient_id=1)
    state.overall_data_quality = DataQuality.GOOD
    
    # Add healthy feature states
    hr_state = FeatureState(
        feature_name='heart_rate',
        current_value=65.0,
        baseline_value=65.0,
        data_quality=DataQuality.GOOD
    )
    state.add_feature(hr_state)
    
    bp_state = FeatureState(
        feature_name='systolic_bp',
        current_value=115.0,
        baseline_value=115.0,
        data_quality=DataQuality.GOOD
    )
    state.add_feature(bp_state)
    
    risk = prediction_engine.assess_risk(state)
    
    assert risk.risk_score is not None
    assert risk.risk_score < 0.5  # Should be relatively low


def test_feature_contributions(prediction_engine):
    """Test that feature contributions are generated."""
    state = DigitalTwinState(patient_id=1)
    state.overall_data_quality = DataQuality.GOOD
    
    hr_state = FeatureState(
        feature_name='heart_rate',
        current_value=72.0,
        baseline_value=70.0,
        data_quality=DataQuality.GOOD
    )
    state.add_feature(hr_state)
    
    risk = prediction_engine.assess_risk(state)
    
    assert len(risk.feature_contributions) > 0
    
    for contrib in risk.feature_contributions:
        assert contrib.feature_name is not None
        assert contrib.contribution_value is not None
        assert contrib.direction in ['increases_risk', 'decreases_risk']
        assert contrib.explanation is not None


def test_confidence_calculation(prediction_engine):
    """Test confidence score calculation."""
    state = DigitalTwinState(patient_id=1)
    state.overall_data_quality = DataQuality.EXCELLENT
    state.completeness_score = 1.0
    
    risk = prediction_engine.assess_risk(state)
    
    assert risk.confidence is not None
    assert 0.0 <= risk.confidence <= 1.0


def test_limitations_included(prediction_engine):
    """Test that limitations are included in risk assessment."""
    state = DigitalTwinState(patient_id=1)
    state.overall_data_quality = DataQuality.GOOD
    
    hr_state = FeatureState(
        feature_name='heart_rate',
        current_value=72.0,
        data_quality=DataQuality.GOOD
    )
    state.add_feature(hr_state)
    
    risk = prediction_engine.assess_risk(state)
    
    assert len(risk.limitations) > 0
    assert any('clinical' in limitation.lower() for limitation in risk.limitations)


def test_model_metadata(prediction_engine):
    """Test that model metadata is included."""
    state = DigitalTwinState(patient_id=1)
    state.overall_data_quality = DataQuality.GOOD
    
    hr_state = FeatureState(
        feature_name='heart_rate',
        current_value=72.0,
        data_quality=DataQuality.GOOD
    )
    state.add_feature(hr_state)
    
    risk = prediction_engine.assess_risk(state)
    
    assert risk.model_name is not None
    assert risk.model_version is not None
    assert risk.target_condition is not None
