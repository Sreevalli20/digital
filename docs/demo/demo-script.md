# Swasthya Twin Demo Script

## Video Information

**Title:** Swasthya Twin - Explainable, Adaptive Patient Digital Twin  
**Duration:** 15-20 minutes  
**Presenter:** Kommavarapu Kameswari Sreevalli  
**Team:** Brain Catalyst  
**Competition:** Happiest Health Digital Twin Challenge 2026

**Note:** This is a demo script and storyboard. The actual unlisted YouTube video URL will be added after recording and upload.

---

## Scene-by-Scene Storyboard

### Scene 1: Introduction (2 minutes)

**Visual:** Presenter on camera, or screen with project title and team information

**Narration:**
"Hello, I'm Kommavarapu Kameswari Sreevalli from the Brain Catalyst team at VMTW. Welcome to our submission for the Happiest Health Digital Twin Challenge 2026.

Today, I'll be demonstrating Swasthya Twin – an explainable, adaptive patient Digital Twin designed to help understand health changes, explore possibilities, and act earlier through personalized health modeling."

**Screen Text:**
- Project Name: Swasthya Twin
- Tagline: Understand the change. Explore the possibilities. Act earlier.
- Team: Brain Catalyst
- Competition: Happiest Health Digital Twin Challenge 2026

---

### Scene 2: Problem Statement (2 minutes)

**Visual:** Landing page showing problem statement and capabilities

**Narration:**
"Healthcare decisions often rely on single-point measurements or population averages that may not reflect an individual's unique health trajectory. Patients and clinicians lack tools to understand how personal baselines evolve over time and how hypothetical interventions might affect health outcomes.

Swasthya Twin addresses this by creating a patient-specific virtual health model that maintains longitudinal observations, computes personalized risk assessments, and enables evidence-based scenario exploration."

**Actions:**
- Scroll to problem statement section
- Highlight key capabilities
- Show architecture overview

---

### Scene 3: System Architecture (2 minutes)

**Visual:** Architecture diagram or system overview

**Narration:**
"Our system is built with a modular, evidence-oriented architecture. We use Flask for the web framework, SQLite for persistence, and Python standard libraries for deterministic calculations.

The architecture separates concerns into distinct layers: presentation, application, service, repository, and persistence. This ensures maintainability, testability, and clear separation of business logic from data access."

**Actions:**
- Show architecture diagram
- Explain each layer briefly
- Highlight technology choices

---

### Scene 4: Landing Page Tour (1 minute)

**Visual:** Full landing page walkthrough

**Narration:**
"Let me show you the landing page. It provides a clear overview of the project, our key capabilities, the problem we're addressing, and transparent research disclaimers. Users can enter the interactive demo from here."

**Actions:**
- Scroll through landing page
- Point out key sections
- Click "Try Interactive Demo" button

---

### Scene 5: Patient Workspace Overview (2 minutes)

**Visual:** Demo interface with patient selection

**Narration:**
"This is the patient workspace. Users can select existing patients or create new ones. For demonstration purposes, I'll generate a synthetic patient with realistic health data."

**Actions:**
- Show patient grid
- Click "Generate Synthetic Patient"
- Show generated patient profile

---

### Scene 6: Observation Ingestion (2 minutes)

**Visual:** Observation entry form and CSV upload

**Narration:**
"Swasthya Twin supports multiple data ingestion methods. Users can manually enter observations, upload CSV files with validated schemas, or use our synthetic data generator. All observations are validated for range, units, and timestamps before storage."

**Actions:**
- Add a manual observation (heart rate: 72 bpm)
- Show observation validation
- Display recent observations list

---

### Scene 7: Digital Twin State (2 minutes)

**Visual:** Overview tab with feature states

**Narration:**
"The Digital Twin state engine computes personalized baselines, current values, rolling averages, and trends. For each feature, we show the change from personal baseline, trend direction, and data quality assessment."

**Actions:**
- Switch to Overview tab
- Show feature states
- Explain baseline calculation
- Highlight trend indicators

---

### Scene 8: Risk Assessment (2 minutes)

**Visual:** Risk assessment tab with feature contributions

**Narration:**
"Our prediction engine uses a rules-based approach with explainable feature contributions. We assess cardiometabolic risk based on blood pressure, heart rate, BMI, and glucose. Each feature's contribution is explained with evidence-based clinical thresholds."

**Actions:**
- Switch to Risk Assessment tab
- Show risk level and score
- Explain feature contributions
- Highlight limitations section

---

### Scene 9: Scenario Simulation (2 minutes)

**Visual:** Scenario creation and results

**Narration:**
"One of our key innovations is the scenario simulator. Users can modify health variables within reasonable bounds and see how hypothetical changes affect risk assessments. This enables evidence-based exploration of interventions without modifying historical data."

**Actions:**
- Switch to Scenarios tab
- Create a scenario (increase heart rate to 95 bpm)
- Run the scenario
- Show baseline vs scenario risk comparison
- Explain risk change

---

### Scene 10: Data Export (1 minute)

**Visual:** Export tab with download options

**Narration:**
"Users can export patient data in multiple formats: JSON evidence bundles with FHIR-compatible mappings, CSV observation files, or human-readable summary reports. All exports include provenance information and model metadata."

**Actions:**
- Switch to Export tab
- Show export options
- Explain evidence bundle structure

---

### Scene 11: Technical Innovation (1 minute)

**Visual:** Highlight key innovations

**Narration:**
"Our signature innovation is the Baseline-to-Scenario Evidence Chain. Every meaningful change shows a traceable chain from observed data through validation, baseline comparison, algorithm output, explanation, and hypothetical scenario comparison. This ensures reproducibility and transparency."

**Actions:**
- Show evidence chain diagram
- Explain provenance tracking
- Highlight reproducibility features

---

### Scene 12: Security and Privacy (1 minute)

**Visual:** Security considerations

**Narration:**
"We've implemented comprehensive security measures including input validation, parameterized SQL queries, secure file upload handling, and no external API calls. All data is stored locally with SQLite, and we use only synthetic data for demonstration."

**Actions:**
- Show security documentation
- Explain privacy measures
- Highlight no-external-dependencies design

---

### Scene 13: Evaluation and Limitations (1 minute)

**Visual:** Evaluation results and limitations

**Narration:**
"Our evaluation shows reproducible calculations, deterministic behavior, and appropriate risk classifications. However, this is a research prototype, not a clinical tool. It has not been validated on clinical datasets and should not be used for medical decision-making."

**Actions:**
- Show evaluation metrics
- List known limitations
- Emphasize research prototype status

---

### Scene 14: Deployment and Future Work (1 minute)

**Visual:** Deployment information and roadmap

**Narration:**
"The application is designed for Render free tier deployment with a target memory under 512 MB. Future work includes clinical validation, integration with real wearables, persistent storage for production, and expansion to additional health domains."

**Actions:**
- Show deployment configuration
- List future enhancements
- Explain scalability considerations

---

### Scene 15: Conclusion and Call to Action (1 minute)

**Visual:** Presenter on camera or summary screen

**Narration:**
"Swasthya Twin demonstrates how Digital Twin concepts can be applied to personalized health monitoring with transparent, explainable, and reproducible computations. Thank you for watching our demonstration.

The complete source code, documentation, and evaluation results are available on our GitHub repository. We welcome feedback and contributions from the research community."

**Screen Text:**
- GitHub Repository: https://github.com/Sreevalli20/digital.git
- License: MIT
- Contact: brain-catalyst@example.com

---

## Recording Checklist

### Pre-Recording
- [ ] Test all demo workflows
- [ ] Verify synthetic data generation works
- [ ] Ensure landing page loads correctly
- [ ] Test scenario simulation
- [ ] Verify export functionality
- [ ] Check microphone and camera quality
- [ ] Prepare screen recording software
- [ ] Test internet connection

### During Recording
- [ ] Speak clearly and at moderate pace
- [ ] Keep mouse movements smooth
- [ ] Allow time for screen elements to load
- [ ] Explain technical terms clearly
- [ ] Maintain consistent energy throughout
- [ ] Follow scene-by-scene storyboard
- [ ] Stay within 15-20 minute duration

### Post-Recording
- [ ] Review video for audio quality
- [ ] Check visual clarity
- [ ] Verify all features demonstrated
- [ ] Edit out any mistakes or pauses
- [ ] Add captions if desired
- [ ] Upload to YouTube as unlisted
- [ ] Add video URL to this document
- [ ] Update README with video link

---

## Video URL

**Status:** PENDING recording and upload

**Actual URL:** [PENDING - To be added after upload]

---

## Alternative Script for Live Presentation

If presenting live at the summit:

1. **Introduction** (1 minute) - Introduce self and project
2. **Problem & Solution** (2 minutes) - Explain the healthcare challenge
3. **Live Demo** (8 minutes) - Real-time demonstration of key features
4. **Technical Deep Dive** (3 minutes) - Architecture and innovation
5. **Evaluation & Limitations** (2 minutes) - Honest assessment
6. **Q&A** (4 minutes) - Address questions from judges

**Total:** 20 minutes

---

## Key Demo Points to Emphasize

1. **Reproducibility:** Fixed seed generates identical synthetic data
2. **Explainability:** Every risk output includes feature contributions
3. **Transparency:** Clear distinction between observed, synthetic, and hypothetical data
4. **Evidence Chain:** Traceable path from input to output
5. **Safety:** Explicit disclaimers and limitations
6. **Scientific Rigor:** Deterministic calculations, not random risk scores
7. **User Experience:** Clean, professional interface
8. **Technical Credibility:** Proper architecture, testing, and documentation

---

## Common Questions and Answers

**Q: Is this clinically validated?**
A: No, this is a research prototype. It has not been validated on clinical datasets and should not be used for medical decision-making.

**Q: How do you ensure reproducibility?**
A: We use fixed random seeds for synthetic data generation, deterministic calculations for all state computations, and store all parameters in risk assessments.

**Q: What's the difference between this and a chatbot?**
A: This is a computational Digital Twin that maintains structured patient state, runs actual algorithms, and provides reproducible simulations. It's not a conversational AI pretending to be a medical expert.

**Q: Can this predict heart attacks?**
A: No. We do not claim to predict emergencies or diagnose specific conditions. We provide screening-level risk assessments based on available observations with clear limitations.

**Q: How would this work in production?**
A: For production, we would need clinical validation, persistent storage, integration with electronic health records, regulatory compliance, and professional medical oversight.

---

## Technical Terms Explained

- **Digital Twin:** A virtual representation of a physical entity that maintains state and enables simulation
- **Baseline:** A patient's personal normal values computed from their historical data
- **Provenance:** The origin and processing history of data
- **Longitudinal:** Data collected over time to track changes
- **FHIR:** Fast Healthcare Interoperability Resources - a healthcare data standard
- **Rules-based:** Using explicit rules rather than machine learning for predictions
- **Explainable AI:** AI systems that can explain their outputs in human-understandable terms
