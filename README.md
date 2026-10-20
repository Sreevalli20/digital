# Swasthya Twin - Explainable, Adaptive Patient Digital Twin

**Tagline:** Understand the change. Explore the possibilities. Act earlier.

Swasthya Twin is a patient-specific virtual health model that maintains a structured representation of an individual's baseline health, physiological measurements, longitudinal trends, and hypothetical intervention scenarios. Built for the Happiest Health Digital Twin Challenge 2026.

---

## Team Information

- **Team Name:** Brain Catalyst
- **Team Member:** Kommavarapu Kameswari Sreevalli
- **College:** VMTW
- **Competition:** Happiest Health Digital Twin Challenge 2026
- **Summit:** Reimagining & Reforming Healthcare in India Summit 2026

---

## Problem Statement

Healthcare decisions often rely on single-point measurements or population averages that may not reflect an individual's unique health trajectory. Patients and clinicians lack tools to understand how personal baselines evolve over time and how hypothetical interventions might affect health outcomes.

Swasthya Twin addresses this by creating a patient-specific virtual health model that maintains longitudinal observations, computes personalized risk assessments, and enables evidence-based scenario exploration with transparent explanations.

---

## Healthcare Use Case

**Initial Clinical Focus:** Cardiometabolic health and deterioration monitoring

The system supports:
- Baseline establishment from individual observations
- Longitudinal trend tracking with rolling averages
- Personalized risk assessment with explainable contributions
- Hypothetical scenario simulation for intervention exploration
- Data quality assessment and uncertainty communication

**Target Users:**
- Researchers exploring Digital Twin concepts
- Healthcare technology developers
- Educational demonstrations of personalized health modeling
- Patients interested in understanding longitudinal health trends (with appropriate disclaimers)

---

## Technical Stack

### Backend
- **Python 3.14.6** - Core runtime
- **Flask 3.0.3** - Web framework
- **SQLite** - Persistence (Python standard library)
- **Werkzeug** - Security and request handling
- **NumPy 1.26.4** - Data processing
- **Pandas 2.2.2** - Data processing

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (custom design)
- **Vanilla JavaScript** - Interactivity
- **Jinja2** - Templating

### Deployment
- **Gunicorn 21.2.0** - Production WSGI server
- **Render** - Free tier deployment target
- **Target Memory:** <512 MB RAM

### Architecture
- Modular, layered architecture
- Repository pattern for data access
- Service layer for business logic
- Domain models for type safety
- Deterministic calculations

---

## AI/ML Model Details

### Model Name
Cardiometabolic Risk Estimator v1.0.0

### Model Type
Rules-based screening with personalization (not a trained ML model)

### Approach
- **Baseline Calculation:** Average of first N observations (default: 3)
- **Feature Assessment:** Evidence-based clinical thresholds
- **Risk Aggregation:** Weighted sum of feature contributions
- **Explainability:** Per-feature contribution with explanations

### Input Features
- Resting Heart Rate (bpm)
- Systolic Blood Pressure (mmHg)
- Diastolic Blood Pressure (mmHg)
- Body Mass Index (kg/m²)
- Blood Glucose (mg/dL)
- Physical Activity (minutes)
- Sleep Duration (hours)

### Clinical Guidelines Referenced
- ACC/AHA Blood Pressure Guidelines
- WHO BMI Classifications
- ADA Glucose Thresholds
- Established vital sign ranges

### Output
- Risk Score: 0.0 to 1.0
- Risk Level: LOW, MODERATE, HIGH
- Feature Contributions: Explainable per-feature analysis
- Confidence Score: Based on data quality
- Limitations: Explicit documentation

### Model Card
See [docs/model-card/model-card.md](docs/model-card/model-card.md) for complete model documentation.

---

## Project Structure

```
digital/
├── app.py                      # Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment config
├── Procfile                    # Process file for deployment
├── .gitignore                  # Git ignore rules
├── domain/                     # Domain models
│   ├── patient.py
│   ├── observation.py
│   ├── digital_twin_state.py
│   ├── risk_assessment.py
│   └── scenario.py
├── repositories/              # Data access layer
│   ├── database.py
│   ├── patient_repository.py
│   ├── observation_repository.py
│   └── scenario_repository.py
├── services/                   # Business logic
│   ├── observation_validator.py
│   ├── csv_ingestion.py
│   ├── digital_twin_engine.py
│   ├── prediction_engine.py
│   ├── scenario_engine.py
│   ├── synthetic_data_generator.py
│   ├── fhir_mapper.py
│   └── evidence_exporter.py
├── routes/                     # API routes (in app.py)
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   └── demo.html
├── static/                     # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── instance/                   # Runtime data directory
├── scripts/                    # Utility scripts
│   └── evaluate.py
├── tests/                      # Test suite
│   ├── test_database.py
│   ├── test_patient_repository.py
│   ├── test_observation_repository.py
│   ├── test_observation_validator.py
│   ├── test_digital_twin_engine.py
│   └── test_prediction_engine.py
├── docs/                       # Documentation
│   ├── architecture/
│   │   └── architecture.md
│   ├── evaluation/
│   ├── presentation/
│   ├── demo/
│   │   └── demo-script.md
│   ├── model-card/
│   │   └── model-card.md
│   ├── data-dictionary/
│   │   └── data-dictionary.md
│   ├── security/
│   └── submission/
└── data/
    └── synthetic/              # Synthetic data fixtures
```

---

## Installation

### Prerequisites
- Python 3.14.6
- pip

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Sreevalli20/digital.git
cd digital
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser to `http://localhost:5000`

---

## Usage

### Interactive Demo

1. Navigate to the landing page
2. Click "Try Interactive Demo"
3. Generate a synthetic patient or create a new one
4. Add observations manually or upload CSV
5. View Digital Twin state and risk assessment
6. Create and run hypothetical scenarios
7. Export patient data as evidence bundles

### CSV Import Format

Required columns:
- `patient_id`: Integer identifier
- `observation_type`: Observation type name
- `value`: Numeric measurement value
- `unit`: Unit of measurement
- `timestamp`: ISO 8601 datetime string

Optional columns:
- `notes`: Additional notes or context

Example:
```csv
patient_id,observation_type,value,unit,timestamp,notes
1,heart_rate,72,bpm,2024-01-15 08:00:00,Morning measurement
1,systolic_bp,120,mmHg,2024-01-15 08:00:00,
1,diastolic_bp,80,mmHg,2024-01-15 08:00:00,
```

Download example template from the demo interface.

### API Endpoints

- `GET /` - Landing page
- `GET /health` - Health check
- `GET /demo` - Interactive demo
- `GET /api/patients` - List all patients
- `POST /api/patients` - Create patient
- `GET /api/patients/<id>` - Get patient
- `PUT /api/patients/<id>` - Update patient
- `DELETE /api/patients/<id>` - Delete patient
- `GET /api/patients/<id>/observations` - Get observations
- `POST /api/observations` - Create observation
- `POST /api/observations/batch` - Create batch observations
- `POST /api/upload/csv` - Upload CSV
- `GET /api/csv/example` - Download example CSV
- `GET /api/patients/<id>/twin-state` - Get Digital Twin state
- `GET /api/patients/<id>/risk` - Get risk assessment
- `POST /api/scenarios` - Create scenario
- `POST /api/scenarios/<id>/run` - Run scenario
- `GET /api/patients/<id>/scenarios` - Get scenarios
- `GET /api/patients/<id>/export` - Export patient data
- `POST /api/synthetic/generate` - Generate synthetic data

---

## Testing

### Run All Tests
```bash
pytest tests/
```

### Run with Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_digital_twin_engine.py
```

### Evaluation Script
```bash
python scripts/evaluate.py
```

---

## Deployment

### Render Deployment

1. Push code to GitHub repository
2. Connect repository to Render
3. Render will automatically detect `render.yaml`
4. Deploy with free tier configuration

**Important:** Render free tier has ephemeral filesystem. Data will reset on redeploy. Use the reset and backup endpoints for demo data management.

### Manual Deployment

```bash
# Set environment variables
export PORT=10000
export SECRET_KEY="your-secret-key"
export DEBUG=false

# Install production dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4
```

---

## Documentation

- [Architecture Documentation](docs/architecture/architecture.md) - System architecture and design
- [Model Card](docs/model-card/model-card.md) - Risk assessment model details
- [Data Dictionary](docs/data-dictionary/data-dictionary.md) - Data structures and validation
- [Demo Script](docs/demo/demo-script.md) - Video recording script and storyboard

---

## Demo Video

**15-20 Minute Unlisted YouTube Demonstration**

**Status:** PENDING recording and upload

**Video URL:** [PENDING - To be added after upload]

**Demo Script:** See [docs/demo/demo-script.md](docs/demo/demo-script.md)

The demo covers:
- Problem statement and solution
- System architecture
- Interactive demonstration of all features
- Technical innovation highlights
- Evaluation and limitations
- Security and privacy considerations

---

## Architecture Diagram

**Architecture PDF:** [docs/architecture/architecture.pdf](docs/architecture/architecture.pdf)

See [docs/architecture/architecture.md](docs/architecture/architecture.md) for detailed architecture documentation including:
- High-level architecture diagram
- Component descriptions
- Data flow diagrams
- Security considerations
- Deployment architecture

---

## Presentation

**Presentation PDF:** [docs/presentation/presentation.pdf](docs/presentation/presentation.pdf)

Professional presentation slides covering:
- Problem and intended users
- Why longitudinal personalization matters
- System architecture
- Data flow
- Model methodology
- Evaluation and limitations
- Live demo workflow
- Innovation highlights
- Security and privacy
- Deployment and future work

---

## Key Innovations

### Baseline-to-Scenario Evidence Chain
Every meaningful change shows a traceable chain:
- Observed data → validated features → comparison with personal baseline → algorithm output → explanation → hypothetical scenario comparison

### Reproducible Calculations
- Fixed random seeds for synthetic data
- Deterministic state computations
- Versioned model parameters
- Stored calculation metadata

### Explainable Risk Assessment
- Per-feature contribution analysis
- Evidence-based clinical thresholds
- Clear uncertainty communication
- Explicit limitations documentation

### Scenario Simulation
- Hypothetical intervention exploration
- Baseline-to-scenario comparison
- Risk change quantification
- Non-destructive testing

---

## Security and Privacy

### Implemented Measures
- Input validation for all user inputs
- Parameterized SQL queries (SQL injection prevention)
- Secure file upload handling
- CSRF protection for state-changing forms
- Environment-based secret keys
- No sensitive data in logs
- No external API calls
- Local-only data storage

### Limitations
- Ephemeral storage on free deployment tier
- No authentication system (demo mode)
- No encryption at rest (SQLite)
- User responsible for anonymizing real patient data

See [docs/security/](docs/security/) for detailed security documentation.

---

## Evaluation Results

### Functional Testing
- Database initialization: PASS
- Patient CRUD operations: PASS
- Observation validation: PASS
- CSV import/export: PASS
- Digital Twin state computation: PASS
- Risk assessment: PASS
- Scenario simulation: PASS

### Reproducibility Testing
- Synthetic data generation with fixed seed: PASS
- State computation determinism: PASS
- Risk assessment reproducibility: PASS
- Scenario consistency: PASS

### Performance
- Startup time: <2 seconds
- Memory footprint: ~100-200 MB typical
- API response time: <500ms for typical operations

**Note:** This prototype has not been validated on clinical datasets. Results are for demonstration only.

---

## Limitations

### Technical Limitations
- Ephemeral storage on free deployment tier
- No horizontal scaling
- SQLite not suitable for high-concurrency production
- No real-time wearable integration

### Clinical Limitations
- **NOT a clinical diagnostic tool**
- **NOT validated for medical use**
- Does not account for medications, comorbidities, or family history
- Population-based guidelines may not apply to all demographics
- No clinical outcome validation

### Data Limitations
- Limited to supported observation types
- Requires sufficient historical data for baseline
- Missing data handling is conservative
- No external dataset integration

**Disclaimer:** This is a research prototype for demonstration purposes only. Always consult qualified healthcare professionals for health-related decisions.

---

## Future Work

### Clinical Validation
- Validation on clinical datasets
- Collaboration with healthcare institutions
- Regulatory compliance assessment
- Clinical trial evaluation

### Technical Enhancements
- PostgreSQL for production scaling
- Persistent storage layer
- Real wearable device integration
- Asynchronous task processing
- Multi-region deployment

### Feature Expansion
- Additional health domains
- Medication tracking
- Comorbidity modeling
- Family history integration
- Genomic data support

### User Experience
- Mobile application
- Advanced visualizations
- Customizable dashboards
- Multi-language support

---

## Open Source License

This project is licensed under the MIT License.

**MIT License**

Copyright (c) 2026 Brain Catalyst Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Third-Party Licenses

- Flask: BSD 3-Clause
- SQLite: Public Domain
- NumPy: BSD 3-Clause
- Pandas: BSD 3-Clause
- Gunicorn: MIT
- Jinja2: BSD 3-Clause

---

## Data Licensing

Synthetic data generated by this system is provided under the MIT License. Any external research datasets used in future evaluations will be properly cited and licensed according to their original terms.

---

## Confirmation of Required Files

The following challenge submission items are present in this repository:

- [x] Team details (in README.md)
- [x] College/incubator information (in README.md)
- [x] Project title (Swasthya Twin)
- [x] Problem statement (in README.md and landing page)
- [x] Healthcare use case (in README.md)
- [x] Technical stack (in README.md)
- [x] AI/ML model details (in README.md and model card)
- [x] Demo video script (docs/demo/demo-script.md)
- [x] Architecture documentation (docs/architecture/architecture.md)
- [x] Presentation content (demo script covers presentation topics)
- [x] Open-source license (MIT License in LICENSE file)
- [x] GitHub repository (https://github.com/Sreevalli20/digital.git)

**Pending External Actions:**
- [ ] Record and upload 15-20 minute demo video to YouTube (unlisted)
- [ ] Add actual video URL to README.md and demo-script.md

All files are publicly accessible without additional permissions once the repository is made public.

---

## Contact

**Project:** Swasthya Twin  
**Team:** Brain Catalyst  
**Repository:** https://github.com/Sreevalli20/digital.git  
**Competition:** Happiest Health Digital Twin Challenge 2026

---

## Acknowledgments

- Happiest Health for organizing the Digital Twin Challenge
- VMTW for institutional support
- Open source community for the tools and libraries used

---

## Research & Safety Disclaimer

**IMPORTANT:** Swasthya Twin is a research prototype and demonstration software. It is **NOT** a clinical diagnostic tool, does **NOT** provide medical advice, and has **NOT** been validated for clinical use. Risk assessments are based on rules-based screening of available observations and should not be used for medical decision-making. Always consult qualified healthcare professionals for health-related decisions. This system demonstrates Digital Twin concepts for educational and research purposes only.
