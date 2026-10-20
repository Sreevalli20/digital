# Swasthya Twin Architecture

## System Overview

Swasthya Twin is a modular, evidence-oriented Digital Twin system built with Flask, SQLite, and Python standard libraries. The architecture separates concerns into distinct layers for maintainability and testability.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Landing Page │  │  Demo UI     │  │  API Routes  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Flask Routes │  │  Request     │  │  Response    │      │
│  │              │  │  Validation  │  │  Formatting  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Service Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Digital Twin │  │  Prediction  │  │   Scenario   │      │
│  │    Engine    │  │    Engine    │  │    Engine    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    CSV       │  │  Observation │  │  Synthetic   │      │
│  │  Ingestion   │  │   Validator  │  │   Generator  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  FHIR Mapper │  │ Evidence     │                        │
│  │              │  │   Exporter   │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Repository Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Patient    │  │ Observation  │  │   Scenario   │      │
│  │  Repository  │  │  Repository  │  │  Repository  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐                                            │
│  │   Database   │                                            │
│  │   Manager    │                                            │
│  └──────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Persistence Layer                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              SQLite Database                           │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐  │  │
│  │  │ Patients │ │Observ.  │ │Scenarios │ │Proven. │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### Presentation Layer

**Landing Page** (`templates/index.html`)
- Project overview and capabilities
- Architecture explanation
- Research disclaimers
- Team information

**Demo UI** (`templates/demo.html`)
- Patient selection and management
- Observation entry and CSV upload
- Digital Twin state visualization
- Risk assessment display
- Scenario simulation interface
- Data export functionality

**API Routes** (`app.py`)
- RESTful endpoints for all operations
- Health check endpoint for deployment monitoring
- JSON request/response handling

### Application Layer

**Flask Application** (`app.py`)
- WSGI application entry point
- Route definitions and request handling
- Session management and security
- Error handling and response formatting

### Service Layer

**Digital Twin Engine** (`services/digital_twin_engine.py`)
- Computes patient baseline values
- Calculates rolling averages and trends
- Assesses data quality and freshness
- Determines feature states

**Prediction Engine** (`services/prediction_engine.py`)
- Rules-based risk assessment
- Feature contribution analysis
- Confidence scoring
- Limitations documentation

**Scenario Engine** (`services/scenario_engine.py`)
- Hypothetical scenario creation
- Feature modification validation
- Baseline-to-scenario comparison
- Risk change calculation

**CSV Ingestion Service** (`services/csv_ingestion.py`)
- CSV parsing and validation
- Batch observation processing
- Duplicate detection
- Error reporting

**Observation Validator** (`services/observation_validator.py`)
- Value range validation
- Unit validation
- Timestamp validation
- Provenance tracking

**Synthetic Data Generator** (`services/synthetic_data_generator.py`)
- Reproducible patient generation
- Synthetic observation creation
- Fixed-seed determinism
- Risk profile variants

**FHIR Mapper** (`services/fhir_mapper.py`)
- Domain model to FHIR resource mapping
- Simplified FHIR R4 compatibility
- Bundle generation

**Evidence Exporter** (`services/evidence_exporter.py`)
- JSON evidence bundle generation
- CSV observation export
- Human-readable summary reports

### Repository Layer

**Patient Repository** (`repositories/patient_repository.py`)
- CRUD operations for patients
- Query by ID, external ID
- Synthetic patient filtering

**Observation Repository** (`repositories/observation_repository.py`)
- CRUD operations for observations
- Patient-specific queries
- Type filtering and time ranges
- Batch operations

**Scenario Repository** (`repositories/scenario_repository.py`)
- CRUD operations for scenarios
- Patient-specific scenario queries
- Modification persistence

**Database Manager** (`repositories/database.py`)
- SQLite connection management
- Schema initialization
- Index creation
- Backup and restore

### Persistence Layer

**SQLite Database**
- Patients table
- Observations table
- Scenarios table
- Provenance ledger table
- Foreign key constraints
- Performance indexes

## Data Flow

### Observation Ingestion Flow

```
User Input/CSV Upload
        │
        ▼
  Validation
        │
        ▼
  Provenance Recording
        │
        ▼
  Database Storage
        │
        ▼
  Digital Twin State Update
        │
        ▼
  Risk Assessment Update
```

### Scenario Simulation Flow

```
User Creates Scenario
        │
        ▼
  Modification Validation
        │
        ▼
  Load Baseline State
        │
        ▼
  Apply Modifications
        │
        ▼
  Compute New Risk
        │
        ▼
  Compare with Baseline
        │
        ▼
  Return Scenario Results
```

### Risk Assessment Flow

```
Load Patient Observations
        │
        ▼
  Compute Digital Twin State
        │
        ▼
  Check Data Quality
        │
        ▼
  Compute Feature Contributions
        │
        ▼
  Aggregate Risk Score
        │
        ▼
  Determine Risk Level
        │
        ▼
  Generate Explanations
```

## Security Considerations

### Input Validation
- All user inputs validated at service layer
- Range checking for physiological values
- Unit validation
- Timestamp validation (no future dates)

### SQL Injection Prevention
- Parameterized queries throughout
- No string concatenation in SQL
- Foreign key constraints enforced

### File Upload Security
- File type restrictions (CSV only)
- File size limits (16 MB max)
- Secure filename handling
- Upload directory isolation

### Session Security
- CSRF protection for state-changing forms
- Secure session configuration
- Environment-based secret keys

### Data Privacy
- No external API calls
- Local-only data storage
- No credentials in logs
- Synthetic data for demonstration

## Deployment Architecture

### Production Deployment (Render)

```
Internet → Render Load Balancer → Gunicorn WSGI Server
                                            │
                                            ▼
                                    Flask Application
                                            │
                                            ▼
                                    SQLite Database
                                    (Ephemeral Storage)
```

### Deployment Characteristics
- Stateless application design
- Ephemeral filesystem (data resets on redeploy)
- Health check endpoint for monitoring
- Memory-efficient (<512 MB target)
- No background workers
- No external dependencies

## Technology Stack

### Backend
- Python 3.14.6
- Flask 3.0.3
- SQLite (Python standard library)
- Werkzeug (security and password hashing)

### Frontend
- HTML5
- CSS3 (custom styling)
- Vanilla JavaScript
- Jinja2 templating

### Dependencies
- NumPy 1.26.4 (data processing)
- Pandas 2.2.2 (data processing)
- Gunicorn 21.2.0 (production WSGI server)

### Development
- Pytest 8.2.0 (testing)
- pytest-cov 5.0.0 (coverage)

## Scalability Considerations

### Current Limitations
- Single SQLite database instance
- No horizontal scaling
- Ephemeral storage on free tier
- In-memory risk calculations

### Future Enhancements
- PostgreSQL for production scaling
- Redis for caching
- Asynchronous task processing
- Persistent storage layer
- Multi-region deployment

## Monitoring and Observability

### Health Checks
- `/health` endpoint for deployment monitoring
- Database connectivity checks
- Application status reporting

### Logging
- Standard Python logging
- Error tracking
- Request logging (configurable)

### Metrics
- Response time tracking
- Error rate monitoring
- Data quality metrics
- User activity logging

## Testing Strategy

### Unit Tests
- Repository layer tests
- Service layer tests
- Domain model tests
- Validation logic tests

### Integration Tests
- API endpoint tests
- Database operation tests
- End-to-end workflow tests

### Evaluation Tests
- Reproducibility tests
- Determinism verification
- Scenario consistency tests
- Data quality assessment tests

## Backup and Recovery

### Database Backup
- Manual backup API endpoint
- File-based backup copies
- Timestamped backup files

### Recovery
- Restore from backup endpoint
- Database reset functionality
- Demo data regeneration

## Documentation

### Code Documentation
- Docstrings for all modules
- Type hints where applicable
- Inline comments for complex logic

### User Documentation
- README with setup instructions
- Data dictionary for all fields
- Model card for risk assessment
- API documentation (in code)

### Architecture Documentation
- This architecture document
- Component diagrams
- Data flow diagrams
- Security considerations
