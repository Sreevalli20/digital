"""
Evidence exporter for creating downloadable evidence bundles.
"""
import json
import csv
import io
from typing import Dict, Any, Optional
from datetime import datetime
from domain.patient import Patient
from domain.digital_twin_state import DigitalTwinState
from domain.risk_assessment import RiskAssessment
from services.fhir_mapper import FHIRMapper


class EvidenceExporter:
    """Exports patient data and analysis results as evidence bundles."""
    
    def __init__(self):
        """Initialize evidence exporter."""
        self.fhir_mapper = FHIRMapper()
    
    def export_evidence_bundle(self, patient: Patient,
                               twin_state: DigitalTwinState,
                               risk_assessment: RiskAssessment,
                               observations: list) -> Dict[str, Any]:
        """
        Create a comprehensive evidence bundle for a patient.
        
        Returns:
            Dictionary containing all evidence components
        """
        bundle = {
            "bundle_type": "patient_evidence",
            "generated_at": datetime.utcnow().isoformat(),
            "swasthya_twin_version": "1.0.0",
            "patient": patient.to_dict(),
            "digital_twin_state": twin_state.to_dict(),
            "risk_assessment": risk_assessment.to_dict(),
            "observations": [obs.to_dict() for obs in observations],
            "fhir_resources": {
                "patient": self.fhir_mapper.patient_to_fhir(patient),
                "observations": [
                    self.fhir_mapper.observation_to_fhir(obs) 
                    for obs in observations
                ],
                "risk_assessment": self.fhir_mapper.risk_assessment_to_fhir(risk_assessment)
            },
            "metadata": {
                "patient_id": patient.id,
                "external_id": patient.external_id,
                "total_observations": len(observations),
                "data_quality": twin_state.overall_data_quality.value,
                "risk_level": risk_assessment.risk_level.value if risk_assessment.risk_level else None,
                "model_version": risk_assessment.model_version
            }
        }
        
        return bundle
    
    def export_json(self, bundle: Dict[str, Any]) -> str:
        """Export evidence bundle as JSON string."""
        return json.dumps(bundle, indent=2, default=str)
    
    def export_csv(self, observations: list) -> str:
        """Export observations as CSV string."""
        output = io.StringIO()
        
        if not observations:
            return ""
        
        fieldnames = [
            'id', 'patient_id', 'observation_type', 'value', 'unit',
            'timestamp', 'provenance', 'data_source', 'notes', 'is_valid'
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for obs in observations:
            writer.writerow({
                'id': obs.id,
                'patient_id': obs.patient_id,
                'observation_type': obs.observation_type,
                'value': obs.value,
                'unit': obs.unit,
                'timestamp': obs.timestamp.isoformat() if obs.timestamp else '',
                'provenance': obs.provenance.value if obs.provenance else '',
                'data_source': obs.data_source.value if obs.data_source else '',
                'notes': obs.notes or '',
                'is_valid': obs.is_valid
            })
        
        return output.getvalue()
    
    def export_summary_report(self, patient: Patient,
                              twin_state: DigitalTwinState,
                              risk_assessment: RiskAssessment) -> str:
        """Generate a human-readable summary report."""
        lines = [
            "=" * 60,
            "SWASTHYA TWIN - PATIENT EVIDENCE REPORT",
            "=" * 60,
            f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "PATIENT INFORMATION",
            "-" * 60,
            f"Name: {patient.full_name}",
            f"Patient ID: {patient.id}",
            f"External ID: {patient.external_id}",
            f"Age: {patient.age}" if patient.age else "Age: Not specified",
            f"Gender: {patient.gender.value if patient.gender else 'Unknown'}",
            f"Data Source: {'Synthetic' if patient.is_synthetic else 'Real'}",
            "",
            "DIGITAL TWIN STATE",
            "-" * 60,
            f"Total Observations: {twin_state.total_observations}",
            f"Overall Data Quality: {twin_state.overall_data_quality.value.upper()}",
            f"Data Freshness: {twin_state.data_freshness_days} days ago" if twin_state.data_freshness_days else "Data Freshness: Unknown",
            f"Completeness Score: {twin_state.completeness_score:.1%}",
            "",
            "FEATURE STATES",
            "-" * 60
        ]
        
        for feature_name, feature_state in twin_state.features.items():
            lines.append(f"\n{feature_name.upper().replace('_', ' ')}:")
            lines.append(f"  Current Value: {feature_state.current_value} {feature_state.baseline_value}")
            lines.append(f"  Baseline Value: {feature_state.baseline_value}")
            lines.append(f"  Change: {feature_state.change_from_baseline:+.1f} ({feature_state.percent_change:+.1f}%)" if feature_state.change_from_baseline else "  Change: N/A")
            lines.append(f"  Trend: {feature_state.trend}")
            lines.append(f"  Data Quality: {feature_state.data_quality.value}")
            lines.append(f"  Observations: {feature_state.observation_count}")
        
        lines.extend([
            "",
            "RISK ASSESSMENT",
            "-" * 60,
            f"Model: {risk_assessment.model_name} v{risk_assessment.model_version}",
            f"Risk Level: {risk_assessment.risk_level.value.upper() if risk_assessment.risk_level else 'UNKNOWN'}",
            f"Risk Score: {risk_assessment.risk_score:.2f}" if risk_assessment.risk_score else "Risk Score: N/A",
            f"Confidence: {risk_assessment.confidence:.1%}" if risk_assessment.confidence else "Confidence: N/A",
            f"Data Quality Status: {risk_assessment.data_quality_status}",
            "",
            "FEATURE CONTRIBUTIONS",
            "-" * 60
        ])
        
        for contrib in risk_assessment.feature_contributions:
            lines.append(f"\n{contrib.feature_name.upper().replace('_', ' ')}:")
            lines.append(f"  Contribution: {contrib.contribution_value:.2f}")
            lines.append(f"  Direction: {contrib.direction}")
            lines.append(f"  Explanation: {contrib.explanation}")
        
        if risk_assessment.is_insufficient_data:
            lines.extend([
                "",
                "INSUFFICIENT DATA WARNING",
                "-" * 60,
                risk_assessment.insufficient_data_reason
            ])
        
        lines.extend([
            "",
            "LIMITATIONS",
            "-" * 60
        ])
        
        for limitation in risk_assessment.limitations:
            lines.append(f"  - {limitation}")
        
        lines.extend([
            "",
            "=" * 60,
            "END OF REPORT",
            "=" * 60
        ])
        
        return "\n".join(lines)
