# Swasthya Twin Data Dictionary

## Overview

This document describes the data structures, fields, and validation rules used in the Swasthya Twin Digital Twin system.

## Patient Data

### Patient Entity

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | Integer | Auto | Unique patient identifier | Auto-incremented |
| external_id | String | No | External patient identifier | Unique if provided |
| first_name | String | Yes | Patient first name | Max 255 characters |
| last_name | String | Yes | Patient last name | Max 255 characters |
| date_of_birth | DateTime | No | Patient date of birth | ISO 8601 format |
| gender | Enum | No | Patient gender | 'male', 'female', 'other', 'unknown' |
| created_at | DateTime | Auto | Record creation timestamp | Auto-generated |
| updated_at | DateTime | Auto | Record update timestamp | Auto-generated |
| is_synthetic | Boolean | No | Synthetic data flag | Default: false |

### Supported Observation Types

| Observation Type | Unit | Min Value | Max Value | Precision | Description |
|------------------|------|-----------|-----------|-----------|-------------|
| heart_rate | bpm | 30 | 200 | 0 | Resting heart rate |
| systolic_bp | mmHg | 70 | 250 | 0 | Systolic blood pressure |
| diastolic_bp | mmHg | 40 | 150 | 0 | Diastolic blood pressure |
| bmi | kg/m² | 10 | 60 | 1 | Body mass index |
| glucose | mg/dL | 30 | 600 | 0 | Blood glucose level |
| activity_minutes | minutes | 0 | 300 | 0 | Physical activity duration |
| sleep_hours | hours | 0 | 24 | 1 | Sleep duration |

## Observation Data

### Observation Entity

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| id | Integer | Auto | Unique observation identifier | Auto-incremented |
| patient_id | Integer | Yes | Foreign key to patient | Must exist in patients table |
| observation_type | String | Yes | Type of observation | Must be in supported types |
| value | Float | No | Measured value | Within type-specific range |
| unit | String | Yes | Unit of measurement | Must match observation type |
| timestamp | DateTime | Yes | Observation timestamp | ISO 8601, not in future |
| provenance | Enum | Yes | Data source | 'manual', 'csv_import', 'synthetic', 'wearable', 'scenario' |
| data_source | Enum | Yes | Data classification | 'real', 'synthetic', 'imported' |
| notes | String | No | Additional notes | Max 1000 characters |
| is_valid | Boolean | Yes | Validation status | Default: true |
| validation_error | String | No | Validation error message | Max 500 characters |
| created_at | DateTime | Auto | Record creation timestamp | Auto-generated |

### Provenance Types

| Type | Description | Use Case |
|------|-------------|----------|
| manual | Manually entered by user | User input via form |
| csv_import | Imported from CSV file | Bulk data upload |
| synthetic | Generated synthetically | Demo and testing |
| wearable | From wearable device | Future integration |
| scenario | Hypothetical simulation | Scenario simulations |

## Digital Twin State

### Feature State

| Field | Type | Description |
|-------|------|-------------|
| feature_name | String | Name of the feature |
| baseline_value | Float | Calculated baseline (average of first N observations) |
| current_value | Float | Most recent valid observation value |
| rolling_avg | Float | 30-day rolling average |
| change_from_baseline | Float | Current value minus baseline |
| percent_change | Float | Percentage change from baseline |
| trend | String | 'increasing', 'decreasing', 'stable', 'unknown' |
| data_quality | Enum | 'excellent', 'good', 'fair', 'poor', 'insufficient' |
| last_observation | DateTime | Timestamp of most recent observation |
| observation_count | Integer | Total number of observations for this feature |
| days_since_last_observation | Integer | Days since most recent observation |

### Digital Twin State

| Field | Type | Description |
|-------|------|-------------|
| patient_id | Integer | Patient identifier |
| generated_at | DateTime | State computation timestamp |
| features | Dict | Feature name to FeatureState mapping |
| overall_data_quality | Enum | Aggregate data quality assessment |
| total_observations | Integer | Total observations across all features |
| data_freshness_days | Integer | Days since most recent observation |
| completeness_score | Float | 0.0 to 1.0, proportion of features with sufficient data |

## Risk Assessment

### Risk Assessment Entity

| Field | Type | Description |
|-------|------|-------------|
| patient_id | Integer | Patient identifier |
| model_name | String | Name of the risk model |
| model_version | String | Version of the risk model |
| risk_level | Enum | 'low', 'moderate', 'high', 'unknown' |
| risk_score | Float | 0.0 to 1.0, normalized risk score |
| target_condition | String | Condition being assessed |
| generated_at | DateTime | Assessment timestamp |
| feature_contributions | List | List of FeatureContribution objects |
| data_quality_status | String | Data quality at time of assessment |
| confidence | Float | 0.0 to 1.0, confidence in assessment |
| limitations | List | List of limitation descriptions |
| is_insufficient_data | Boolean | Whether data was insufficient |
| insufficient_data_reason | String | Explanation if insufficient |

### Feature Contribution

| Field | Type | Description |
|-------|------|-------------|
| feature_name | String | Name of the feature |
| contribution_value | Float | Contribution to overall risk (0.0 to 1.0) |
| direction | String | 'increases_risk' or 'decreases_risk' |
| baseline_value | Float | Baseline value for comparison |
| current_value | Float | Current value for comparison |
| explanation | String | Human-readable explanation |

## Scenario Data

### Scenario Entity

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique scenario identifier |
| patient_id | Integer | Patient identifier |
| name | String | Scenario name |
| description | String | Scenario description |
| modifications | Dict | Feature name to ScenarioModification mapping |
| baseline_risk_score | Float | Risk score before scenario |
| scenario_risk_score | Float | Risk score after scenario |
| baseline_risk_level | String | Risk level before scenario |
| scenario_risk_level | String | Risk level after scenario |
| status | Enum | 'pending', 'completed', 'failed' |
| created_at | DateTime | Scenario creation timestamp |
| notes | String | Additional notes |

### Scenario Modification

| Field | Type | Description |
|-------|------|-------------|
| feature_name | String | Name of feature to modify |
| original_value | Float | Original value before modification |
| modified_value | Float | New value for simulation |
| unit | String | Unit of measurement |

## Configuration Constants

### Data Quality Thresholds

| Constant | Value | Description |
|----------|-------|-------------|
| MIN_OBSERVATIONS_FOR_BASELINE | 3 | Minimum observations to calculate baseline |
| MIN_OBSERVATIONS_FOR_TREND | 5 | Minimum observations to calculate trend |
| ROLLING_WINDOW_DAYS | 30 | Days for rolling average window |

### Risk Thresholds

| Constant | Value | Description |
|----------|-------|-------------|
| HIGH_RISK_THRESHOLD | 0.7 | Risk score threshold for high risk |
| MODERATE_RISK_THRESHOLD | 0.4 | Risk score threshold for moderate risk |

## Data Quality Levels

| Level | Description | Criteria |
|-------|-------------|----------|
| excellent | High quality, recent data | Observations >= baseline, last obs < 7 days |
| good | Good quality, reasonably recent | Observations >= baseline, last obs < 30 days |
| fair | Acceptable quality, somewhat stale | Observations >= baseline, last obs < 90 days |
| poor | Low quality or very stale | Observations < baseline or last obs > 90 days |
| insufficient | Not enough data | No observations or insufficient for calculations |

## CSV Import Schema

### Required Columns

- `patient_id`: Integer identifier
- `observation_type`: Observation type name
- `value`: Numeric measurement value
- `unit`: Unit of measurement
- `timestamp`: ISO 8601 datetime string

### Optional Columns

- `notes`: Additional notes or context

### Supported Timestamp Formats

- `YYYY-MM-DD HH:MM:SS`
- `YYYY-MM-DDTHH:MM:SS`
- `YYYY-MM-DD`
- `DD/MM/YYYY HH:MM:SS`
- `DD/MM/YYYY`
- `MM/DD/YYYY HH:MM:SS`
- `MM/DD/YYYY`

## FHIR Mapping

### FHIR Resources Supported

- **Patient**: Basic patient demographics
- **Observation**: Vital signs and measurements
- **RiskAssessment**: Risk assessment results

### FHIR Version

FHIR R4 (4.0.1) compatible structures where implemented.

Note: This is a simplified FHIR-compatible mapping, not complete FHIR R4 compliance.
