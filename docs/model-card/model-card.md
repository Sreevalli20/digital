# Swasthya Twin Model Card

## Model Details

**Model Name:** Cardiometabolic Risk Estimator  
**Model Version:** 1.0.0  
**Model Type:** Rules-based with personalization  
**Date Created:** 2026-10-20  
**Model Purpose:** Screening-level cardiometabolic risk assessment for Digital Twin simulation

## Intended Use

### Primary Use Case
This model is designed to provide explainable, personalized risk assessments for cardiometabolic health deterioration within the Swasthya Twin Digital Twin system. It supports scenario simulation and longitudinal health monitoring.

### Target Users
- Researchers exploring Digital Twin concepts
- Healthcare technology developers
- Educational demonstrations of personalized health modeling
- Patients interested in understanding longitudinal health trends (with appropriate disclaimers)

### Intended Context
- Research prototype and demonstration software
- Scenario simulation for hypothetical interventions
- Longitudinal trend monitoring and baseline comparison
- Evidence generation for health discussions with healthcare providers

### Out of Scope Uses
- Clinical diagnosis
- Treatment decision-making
- Emergency medical assessment
- Regulatory-approved medical device functionality
- Replacement for professional medical judgment

## Model Architecture

### Algorithm Type
Rules-based screening with personalized baseline comparison

### Input Features
- Resting Heart Rate (bpm)
- Systolic Blood Pressure (mmHg)
- Diastolic Blood Pressure (mmHg)
- Body Mass Index (kg/m²)
- Blood Glucose (mg/dL)
- Physical Activity (minutes)
- Sleep Duration (hours)

### Feature Processing
1. **Baseline Calculation:** Average of first N observations (default: 3)
2. **Current Value:** Most recent valid observation
3. **Change Detection:** Difference from personal baseline
4. **Rolling Average:** 30-day rolling window for recent trends
5. **Trend Analysis:** Linear regression slope on time-series data

### Risk Computation
Risk is computed as a weighted sum of feature-specific risk contributions:

- Blood Pressure: Up to 30% contribution
- Heart Rate: Up to 20% contribution
- BMI: Up to 25% contribution
- Glucose: Up to 25% contribution

Each feature's contribution is based on evidence-based clinical thresholds:
- Hypertension staging (ACC/AHA guidelines)
- Resting heart rate ranges
- BMI categories (WHO standards)
- Fasting glucose thresholds (ADA guidelines)

### Output
- Risk Score: 0.0 to 1.0 (normalized)
- Risk Level: LOW (<0.4), MODERATE (0.4-0.7), HIGH (>0.7)
- Feature Contributions: Per-feature risk contribution with explanations
- Confidence Score: Based on data quality and completeness
- Data Quality Status: Overall assessment of input data quality

## Training Data

**Dataset Source:** None (rules-based model, not trained on data)

This model does not use machine learning training. Risk thresholds are based on:
- American College of Cardiology/American Heart Association (ACC/AHA) blood pressure guidelines
- World Health Organization (WHO) BMI classifications
- American Diabetes Association (ADA) glucose thresholds
- Established clinical reference ranges for vital signs

## Evaluation

### Methodology
Evaluation focuses on:
- Reproducibility of calculations
- Deterministic behavior across runs
- Appropriate risk level classification for test cases
- Feature contribution explanation accuracy

### Metrics
- **Reproducibility:** Risk scores identical for identical inputs (verified)
- **Coverage:** All supported observation types generate contributions
- **Data Quality Handling:** Appropriate responses for insufficient data
- **Scenario Consistency:** Hypothetical modifications produce expected directional changes

### Limitations
- No clinical validation on real patient populations
- No external dataset evaluation
- No calibration against clinical outcomes
- Thresholds based on population guidelines, not personalized clinical factors
- Does not account for medications, comorbidities, or family history

## Ethical Considerations

### Bias and Fairness
- Population-based guidelines may not apply equally to all demographic groups
- BMI thresholds have known limitations across ethnicities
- No adjustment for age, gender, or ethnicity in current implementation

### Privacy
- All patient data stored locally in SQLite
- No external API calls or data transmission
- Synthetic data only for demonstration
- User responsible for anonymizing real patient data

### Transparency
- All risk calculations are explainable
- Feature contributions provided for every assessment
- Clear documentation of limitations
- Explicit disclaimers about non-clinical use

## Safety and Security

### Validation
- Input validation for all observations
- Range checking for physiological values
- Unit validation
- Timestamp validation (no future dates)

### Error Handling
- Graceful degradation with insufficient data
- Clear error messages for invalid inputs
- No silent failures or default risk scores

### Deployment
- Stateless operation suitable for ephemeral deployments
- No persistent model artifacts
- No external dependencies at runtime
- Memory-efficient (<512 MB RAM target)

## Maintenance

### Version Control
- Model version tracked in risk assessments
- Configuration externalized for threshold adjustments
- Evaluation scripts for regression testing

### Update Process
- Threshold changes require version increment
- Documentation updates required for any algorithmic changes
- Re-evaluation required after modifications

## References

1. Whelton PK, et al. 2017 ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA Guideline for the Prevention, Detection, Evaluation, and Management of High Blood Pressure in Adults. J Am Coll Cardiol. 2017.
2. World Health Organization. Body Mass Index (BMI) classification.
3. American Diabetes Association. Standards of Medical Care in Diabetes.
4. American Heart Association. Normal resting heart rate ranges.

## Contact

**Project:** Swasthya Twin  
**Team:** Brain Catalyst  
**Competition:** Happiest Health Digital Twin Challenge 2026  
**Repository:** https://github.com/Sreevalli20/digital.git

## Disclaimer

This model is a research prototype for demonstration purposes only. It is NOT a clinical diagnostic tool, has NOT been validated for medical use, and should NOT be used for medical decision-making. Always consult qualified healthcare professionals for health-related decisions.
