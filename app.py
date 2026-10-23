"""
Swasthya Twin - Explainable, Adaptive Patient Digital Twin
Main Flask application.
"""
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import io
import config
from repositories import Database, PatientRepository, ObservationRepository, ScenarioRepository
from services import (
    ObservationValidator, CSVIngestionService, DigitalTwinEngine,
    PredictionEngine, ScenarioEngine, SyntheticDataGenerator,
    EvidenceExporter, APIAdapter
)
from domain import Patient, Observation, Scenario


app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database and repositories
db = Database()
db.initialize_schema()

patient_repo = PatientRepository(db)
observation_repo = ObservationRepository(db)
scenario_repo = ScenarioRepository(db)

# Initialize services
validator = ObservationValidator()
csv_service = CSVIngestionService(validator)
twin_engine = DigitalTwinEngine(observation_repo)
prediction_engine = PredictionEngine()
scenario_engine = ScenarioEngine(prediction_engine)
synthetic_generator = SyntheticDataGenerator()
evidence_exporter = EvidenceExporter()


# Helper functions
def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


# Routes

@app.route('/app')
def react_app():
    """Serve the React SPA."""
    return send_from_directory('static', 'index.html')

@app.route('/app/<path:path>')
def react_static(path):
    """Serve React static assets."""
    return send_from_directory('static', path)

@app.route('/')
def index():
    """Main dashboard - auto-initialize demo if database is empty."""
    # Check if database is empty (no patients)
    patients = patient_repo.get_all()
    if len(patients) == 0:
        # Auto-initialize demo with synthetic patient
        patient = synthetic_generator.generate_patient(is_synthetic=True, use_demo_name=True, external_id="DEMO-001")
        observations = synthetic_generator.generate_observations(None, days_back=90, daily=True)

        # Save to database
        created_patient = patient_repo.create(patient)

        # Set patient_id for observations
        for obs in observations:
            obs.patient_id = created_patient.id

        created_observations = observation_repo.create_batch(observations)

    return render_template('dashboard.html')


@app.route('/landing')
def landing():
    """Landing page."""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint for deployment monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/demo')
def demo():
    """Enter the interactive demo."""
    return render_template('demo.html')


@app.route('/patients')
def patients():
    """Patient profiles page."""
    return render_template('dashboard.html')


@app.route('/trends')
def trends():
    """Health trends page."""
    return render_template('dashboard.html')


@app.route('/risk')
def risk():
    """Risk insights page."""
    return render_template('dashboard.html')


@app.route('/scenarios')
def scenarios():
    """Scenario simulator page."""
    return render_template('dashboard.html')


@app.route('/data')
def data():
    """Data and imports page."""
    return render_template('dashboard.html')


@app.route('/about')
def about():
    """About page."""
    return render_template('index.html')


@app.route('/api/patients', methods=['GET'])
def list_patients():
    """Get list of all patients."""
    patients = patient_repo.get_all()
    return jsonify([p.to_dict() for p in patients])


@app.route('/api/patients', methods=['POST'])
def create_patient():
    """Create a new patient."""
    data = request.get_json()
    
    patient = Patient(
        external_id=data.get('external_id'),
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        date_of_birth=datetime.fromisoformat(data['date_of_birth']) if data.get('date_of_birth') else None,
        gender=data.get('gender'),
        is_synthetic=data.get('is_synthetic', False)
    )
    
    created = patient_repo.create(patient)
    return jsonify(created.to_dict()), 201


@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a specific patient."""
    patient = patient_repo.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    return jsonify(patient.to_dict())


@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update a patient."""
    patient = patient_repo.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    data = request.get_json()
    
    if 'first_name' in data:
        patient.first_name = data['first_name']
    if 'last_name' in data:
        patient.last_name = data['last_name']
    if 'date_of_birth' in data:
        patient.date_of_birth = datetime.fromisoformat(data['date_of_birth'])
    if 'gender' in data:
        patient.gender = data['gender']
    
    updated = patient_repo.update(patient)
    return jsonify(updated.to_dict())


@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient and all associated data."""
    patient = patient_repo.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Delete associated observations and scenarios
    observation_repo.delete_by_patient(patient_id)
    scenario_repo.delete_by_patient(patient_id)
    patient_repo.delete(patient_id)
    
    return jsonify({'message': 'Patient deleted successfully'})


@app.route('/api/patients/<int:patient_id>/observations', methods=['GET'])
def get_observations(patient_id):
    """Get observations for a patient."""
    observation_type = request.args.get('type')
    limit = request.args.get('limit', type=int)
    
    observations = observation_repo.get_by_patient(patient_id, observation_type, limit)
    return jsonify([obs.to_dict() for obs in observations])


@app.route('/api/observations', methods=['POST'])
def create_observation():
    """Create a new observation."""
    data = request.get_json()
    
    observation = Observation(
        patient_id=data['patient_id'],
        observation_type=data['observation_type'],
        value=data.get('value'),
        unit=data['unit'],
        timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else datetime.utcnow(),
        notes=data.get('notes')
    )
    
    # Validate
    is_valid, error = validator.validate(observation)
    observation.is_valid = is_valid
    observation.validation_error = error
    
    created = observation_repo.create(observation)
    return jsonify(created.to_dict()), 201


@app.route('/api/observations/batch', methods=['POST'])
def create_observations_batch():
    """Create multiple observations in a batch."""
    data = request.get_json()
    observations_data = data.get('observations', [])
    
    observations = []
    for obs_data in observations_data:
        obs = Observation(
            patient_id=obs_data['patient_id'],
            observation_type=obs_data['observation_type'],
            value=obs_data.get('value'),
            unit=obs_data['unit'],
            timestamp=datetime.fromisoformat(obs_data['timestamp']) if obs_data.get('timestamp') else datetime.utcnow(),
            notes=obs_data.get('notes')
        )
        observations.append(obs)
    
    # Validate batch
    validated = validator.validate_batch(observations)
    created = observation_repo.create_batch(validated)
    
    return jsonify({
        'created': len(created),
        'observations': [obs.to_dict() for obs in created]
    }), 201


@app.route('/api/upload/csv', methods=['POST'])
def upload_csv():
    """Upload and process CSV file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    patient_id = request.form.get('patient_id', type=int)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400
    
    try:
        csv_content = file.read().decode('utf-8')
        observations, errors = csv_service.parse_csv(csv_content, patient_id)
        
        if errors:
            return jsonify({'errors': errors}), 400
        
        # Validate and ingest
        valid_obs, validation_errors = csv_service.validate_and_ingest(observations)
        
        if validation_errors:
            return jsonify({'validation_errors': validation_errors}), 400
        
        # Create in database
        created = observation_repo.create_batch(valid_obs)
        
        return jsonify({
            'message': f'Successfully imported {len(created)} observations',
            'created': len(created),
            'observations': [obs.to_dict() for obs in created]
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/csv/example', methods=['GET'])
def get_csv_example():
    """Get example CSV template."""
    csv_content = csv_service.generate_example_csv()
    return send_file(
        io.BytesIO(csv_content.encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='example_observations.csv'
    )


@app.route('/api/patients/<int:patient_id>/twin-state', methods=['GET'])
def get_twin_state(patient_id):
    """Get Digital Twin state for a patient."""
    patient = patient_repo.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    state = twin_engine.compute_state(patient_id)
    return jsonify(state.to_dict())


@app.route('/api/patients/<int:patient_id>/risk', methods=['GET'])
def get_risk_assessment(patient_id):
    """Get risk assessment for a patient."""
    patient = patient_repo.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    state = twin_engine.compute_state(patient_id)
    risk = prediction_engine.assess_risk(state)
    
    return jsonify(risk.to_dict())


@app.route('/api/scenarios', methods=['POST'])
def create_scenario():
    """Create a new scenario."""
    data = request.get_json()
    
    scenario = Scenario(
        patient_id=data['patient_id'],
        name=data['name'],
        description=data.get('description', '')
    )
    
    # Add modifications
    for mod in data.get('modifications', []):
        scenario.add_modification(
            feature_name=mod['feature_name'],
            original_value=mod.get('original_value'),
            modified_value=mod['modified_value'],
            unit=mod['unit']
        )
    
    # Validate modifications
    for feature_name, mod in scenario.modifications.items():
        is_valid, error = scenario_engine.validate_modification(
            feature_name, mod.modified_value
        )
        if not is_valid:
            return jsonify({'error': error}), 400
    
    created = scenario_repo.create(scenario)
    return jsonify(created.to_dict()), 201


@app.route('/api/scenarios/<int:scenario_id>/run', methods=['POST'])
def run_scenario(scenario_id):
    """Run a scenario simulation."""
    scenario = scenario_repo.get_by_id(scenario_id)
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    # Get baseline state and risk
    baseline_state = twin_engine.compute_state(scenario.patient_id)
    baseline_risk = prediction_engine.assess_risk(baseline_state)
    
    # Run scenario
    result = scenario_engine.run_scenario(scenario, baseline_state, baseline_risk)
    
    # Update in database
    scenario_repo.update(result)
    
    return jsonify(result.to_dict())


@app.route('/api/patients/<int:patient_id>/scenarios', methods=['GET'])
def get_scenarios(patient_id):
    """Get scenarios for a patient."""
    scenarios = scenario_repo.get_by_patient(patient_id)
    return jsonify([s.to_dict() for s in scenarios])


@app.route('/api/patients/<int:patient_id>/export', methods=['GET'])
def export_patient_data(patient_id):
    """Export patient data as evidence bundle."""
    patient = patient_repo.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    state = twin_engine.compute_state(patient_id)
    risk = prediction_engine.assess_risk(state)
    observations = observation_repo.get_by_patient(patient_id)
    
    format_type = request.args.get('format', 'json')
    
    if format_type == 'json':
        bundle = evidence_exporter.export_evidence_bundle(patient, state, risk, observations)
        json_content = evidence_exporter.export_json(bundle)
        return send_file(
            io.BytesIO(json_content.encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'patient_{patient_id}_evidence.json'
        )
    elif format_type == 'csv':
        csv_content = evidence_exporter.export_csv(observations)
        return send_file(
            io.BytesIO(csv_content.encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'patient_{patient_id}_observations.csv'
        )
    elif format_type == 'report':
        report = evidence_exporter.export_summary_report(patient, state, risk)
        return send_file(
            io.BytesIO(report.encode('utf-8')),
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'patient_{patient_id}_report.txt'
        )
    else:
        return jsonify({'error': 'Invalid format. Use json, csv, or report.'}), 400


@app.route('/api/synthetic/generate', methods=['POST'])
def generate_synthetic_data():
    """Generate synthetic patient data."""
    data = request.get_json()
    patient_type = data.get('type', 'normal')  # 'normal', 'high_risk', 'low_risk'
    use_demo_name = data.get('use_demo_name', True)  # Use DEMO-001 by default

    if patient_type == 'high_risk':
        patient, observations = synthetic_generator.generate_high_risk_patient(None)
    elif patient_type == 'low_risk':
        patient, observations = synthetic_generator.generate_low_risk_patient(None)
    else:
        patient = synthetic_generator.generate_patient(is_synthetic=True, use_demo_name=use_demo_name)
        observations = synthetic_generator.generate_observations(None, days_back=90)

    # Save to database
    created_patient = patient_repo.create(patient)

    # Set patient_id for observations
    for obs in observations:
        obs.patient_id = created_patient.id

    created_observations = observation_repo.create_batch(observations)

    return jsonify({
        'patient': created_patient.to_dict(),
        'observations_count': len(created_observations),
        'patient_id': created_patient.id
    }), 201


@app.route('/api/demo/initialize', methods=['POST'])
def initialize_demo():
    """Initialize demo workspace with synthetic patient if database is empty."""
    # Check if any patients exist
    patients = patient_repo.get_all()

    if len(patients) > 0:
        # Return existing patients without creating new ones
        return jsonify({
            'message': 'Demo already initialized',
            'patients': [p.to_dict() for p in patients],
            'created': False
        }), 200

    # Generate demo patient with DEMO-001 identifier
    patient = synthetic_generator.generate_patient(is_synthetic=True, use_demo_name=True, external_id="DEMO-001")
    observations = synthetic_generator.generate_observations(None, days_back=90, daily=True)

    # Save to database
    created_patient = patient_repo.create(patient)

    # Set patient_id for observations
    for obs in observations:
        obs.patient_id = created_patient.id

    created_observations = observation_repo.create_batch(observations)

    return jsonify({
        'message': 'Demo initialized successfully',
        'patient': created_patient.to_dict(),
        'observations_count': len(created_observations),
        'patient_id': created_patient.id,
        'created': True
    }), 201


@app.route('/api/database/reset', methods=['POST'])
def reset_database():
    """Reset database (demo mode only)."""
    if not config.DEBUG:
        return jsonify({'error': 'Database reset only available in debug mode'}), 403
    
    db.reset_database()
    return jsonify({'message': 'Database reset successfully'})


@app.route('/api/database/backup', methods=['POST'])
def backup_database():
    """Create database backup."""
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(config.DATABASE_DIR, f'backup_{timestamp}.db')
    db.backup_database(backup_path)
    return jsonify({'message': 'Backup created', 'path': backup_path})


# React UI API Endpoints
@app.route('/api/react/patients', methods=['GET'])
def react_list_patients():
    """Get list of all patients in React format."""
    patients = patient_repo.get_all()
    react_patients = [APIAdapter.patient_to_react_format(p) for p in patients]
    return jsonify(react_patients)


@app.route('/api/react/patients/<external_id>/observations', methods=['GET'])
def react_get_observations(external_id):
    """Get observations for a patient in React format."""
    # Find patient by external_id
    patients = patient_repo.get_all()
    patient = next((p for p in patients if p.external_id == external_id), None)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    observations = observation_repo.get_by_patient(patient.id)
    react_observations = [APIAdapter.observation_to_react_format(obs, external_id) for obs in observations]
    return jsonify(react_observations)


@app.route('/api/react/patients/<external_id>/risk', methods=['GET'])
def react_get_risk_assessment(external_id):
    """Get risk assessment for a patient in React format."""
    # Find patient by external_id
    patients = patient_repo.get_all()
    patient = next((p for p in patients if p.external_id == external_id), None)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    # Get risk assessment
    state = twin_engine.compute_state(patient.id)
    risk = prediction_engine.assess_risk(state)

    react_risk = APIAdapter.risk_assessment_to_react_format(risk, external_id)
    return jsonify([react_risk])  # Return as array for React


@app.route('/api/react/metrics', methods=['GET'])
def react_get_metrics():
    """Get metric definitions in React format."""
    return jsonify(APIAdapter.get_metric_definitions())


@app.route('/api/react/demo/initialize', methods=['POST'])
def react_initialize_demo():
    """Initialize demo workspace for React UI."""
    # Check if any patients exist
    patients = patient_repo.get_all()

    if len(patients) > 0:
        # Return existing patients without creating new ones
        react_patients = [APIAdapter.patient_to_react_format(p) for p in patients]
        return jsonify({
            'message': 'Demo already initialized',
            'patients': react_patients,
            'created': False
        }), 200

    # Generate demo patient with DEMO-001 identifier
    patient = synthetic_generator.generate_patient(is_synthetic=True, use_demo_name=True, external_id="DEMO-001")
    observations = synthetic_generator.generate_observations(None, days_back=90, daily=True)

    # Save to database
    created_patient = patient_repo.create(patient)

    # Set patient_id for observations
    for obs in observations:
        obs.patient_id = created_patient.id

    created_observations = observation_repo.create_batch(observations)

    react_patient = APIAdapter.patient_to_react_format(created_patient)
    react_observations = [APIAdapter.observation_to_react_format(obs, created_patient.external_id) for obs in created_observations]

    return jsonify({
        'message': 'Demo initialized successfully',
        'patient': react_patient,
        'observations': react_observations,
        'observations_count': len(created_observations),
        'patient_id': created_patient.external_id,
        'created': True
    }), 201


@app.route('/api/react/patients/<external_id>/observations', methods=['POST'])
def react_create_observation(external_id):
    """Create a new observation for a patient in React format."""
    # Find patient by external_id
    patients = patient_repo.get_all()
    patient = next((p for p in patients if p.external_id == external_id), None)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    data = request.get_json()

    # Map React metric_key to Flask observation_type
    metric_key_map = {
        'systolic_bp': 'systolic_bp',
        'diastolic_bp': 'diastolic_bp',
        'fasting_glucose': 'glucose',
        'hba1c': 'hba1c',
        'resting_heart_rate': 'heart_rate',
        'ldl_cholesterol': 'ldl_cholesterol',
        'hdl_cholesterol': 'hdl_cholesterol',
        'total_cholesterol': 'total_cholesterol',
        'bmi': 'bmi',
        'egfr': 'egfr'
    }

    metric_key = data.get('metricKey')
    observation_type = metric_key_map.get(metric_key, metric_key)

    observation = Observation(
        patient_id=patient.id,
        observation_type=observation_type,
        value=data.get('value'),
        unit=data.get('unit'),
        timestamp=datetime.fromisoformat(data.get('recordedAt')) if data.get('recordedAt') else datetime.utcnow(),
        notes=data.get('contextNotes')
    )

    # Validate
    is_valid, error = validator.validate(observation)
    observation.is_valid = is_valid
    observation.validation_error = error

    if not is_valid:
        return jsonify({'error': error}), 400

    created = observation_repo.create(observation)
    react_observation = APIAdapter.observation_to_react_format(created, external_id)

    return jsonify(react_observation), 201


@app.route('/api/react/patients/<external_id>/scenarios', methods=['POST'])
def react_create_scenario(external_id):
    """Create and run a scenario simulation for a patient in React format."""
    # Find patient by external_id
    patients = patient_repo.get_all()
    patient = next((p for p in patients if p.external_id == external_id), None)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    data = request.get_json()

    # Get baseline state and risk
    baseline_state = twin_engine.compute_state(patient.id)
    baseline_risk = prediction_engine.assess_risk(baseline_state)

    # Create scenario
    scenario = Scenario(
        patient_id=patient.id,
        name=data.get('scenarioName', 'Lifestyle Intervention'),
        description=data.get('description', 'Simulated lifestyle intervention')
    )

    # Translate React lifestyle adjustments to Flask scenario modifications
    adjustments = data.get('adjustments', {})
    modifications = APIAdapter.lifestyle_adjustments_to_scenario_modifications(
        adjustments, baseline_state
    )

    # Apply modifications to scenario
    for feature_name, mod in modifications.items():
        scenario.add_modification(
            feature_name=feature_name,
            original_value=mod['current'],
            modified_value=mod['suggested'],
            unit=mod['unit']
        )

    # Run scenario
    result = scenario_engine.run_scenario(scenario, baseline_state, baseline_risk)

    # Convert to React format
    react_result = APIAdapter.scenario_to_react_format(result, external_id, baseline_risk)

    return jsonify(react_result), 201


@app.route('/api/react/patients/<external_id>/export', methods=['GET'])
def react_export_patient_data(external_id):
    """Export patient data in React format."""
    # Find patient by external_id
    patients = patient_repo.get_all()
    patient = next((p for p in patients if p.external_id == external_id), None)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    format_type = request.args.get('format', 'csv')

    if format_type == 'csv':
        observations = observation_repo.get_by_patient(patient.id)
        csv_content = evidence_exporter.export_csv(observations)
        return send_file(
            io.BytesIO(csv_content.encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{external_id}_observations.csv'
        )
    else:
        return jsonify({'error': 'Invalid format. Use csv.'}), 400


@app.route('/api/react/patients/<external_id>/import/csv', methods=['POST'])
def react_import_csv(external_id):
    """Import CSV data for a patient in React format."""
    # Find patient by external_id
    patients = patient_repo.get_all()
    patient = next((p for p in patients if p.external_id == external_id), None)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400

    try:
        csv_content = file.read().decode('utf-8')
        observations, errors = csv_service.parse_csv(csv_content, patient.id)

        if errors:
            return jsonify({'errors': errors}), 400

        # Validate and ingest
        valid_obs, validation_errors = csv_service.validate_and_ingest(observations)

        if validation_errors:
            return jsonify({'validation_errors': validation_errors}), 400

        # Create in database
        created = observation_repo.create_batch(valid_obs)

        # Convert to React format
        react_observations = [APIAdapter.observation_to_react_format(obs, external_id) for obs in created]

        return jsonify({
            'message': f'Successfully imported {len(created)} observations',
            'created': len(created),
            'observations': react_observations
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)
