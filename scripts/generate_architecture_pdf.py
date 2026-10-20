"""
Generate Architecture Diagram PDF using ReportLab.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def create_architecture_pdf(output_path):
    """Generate architecture diagram PDF."""
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.darkblue,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.darkblue,
        spaceAfter=12,
        spaceBefore=20
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        leading=14
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        spaceAfter=12,
        leading=12
    )
    
    content = []
    
    # Title
    content.append(Paragraph("Swasthya Twin - System Architecture", title_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Overview
    content.append(Paragraph("System Overview", heading_style))
    content.append(Paragraph(
        "Swasthya Twin is a modular, evidence-oriented Digital Twin system built with Flask, SQLite, "
        "and Python standard libraries. The architecture separates concerns into distinct layers "
        "for maintainability and testability.",
        normal_style
    ))
    
    # High-Level Architecture
    content.append(Paragraph("High-Level Architecture", heading_style))
    
    arch_diagram = """
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
"""
    content.append(Paragraph(arch_diagram, code_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Component Descriptions
    content.append(Paragraph("Component Descriptions", heading_style))
    
    components = [
        ("Presentation Layer", [
            "Landing Page (templates/index.html): Project overview, capabilities, architecture, disclaimers",
            "Demo UI (templates/demo.html): Patient management, observation entry, twin state, risk assessment, scenarios",
            "API Routes (app.py): RESTful endpoints, health check, JSON handling"
        ]),
        ("Application Layer", [
            "Flask Application (app.py): WSGI entry point, route definitions, request handling, security, error handling"
        ]),
        ("Service Layer", [
            "Digital Twin Engine: Computes baselines, rolling averages, trends, data quality",
            "Prediction Engine: Rules-based risk assessment, feature contributions, confidence scoring",
            "Scenario Engine: Hypothetical scenarios, modification validation, baseline comparison",
            "CSV Ingestion Service: CSV parsing, validation, batch processing, duplicate detection",
            "Observation Validator: Range, unit, timestamp validation, provenance tracking",
            "Synthetic Data Generator: Reproducible patient generation, fixed-seed determinism",
            "FHIR Mapper: Domain to FHIR resource mapping, bundle generation",
            "Evidence Exporter: JSON bundles, CSV export, summary reports"
        ]),
        ("Repository Layer", [
            "Patient Repository: CRUD operations, ID queries, synthetic filtering",
            "Observation Repository: CRUD, patient queries, type filtering, batch operations",
            "Scenario Repository: CRUD, patient queries, modification persistence",
            "Database Manager: SQLite connections, schema initialization, indexes, backup"
        ]),
        ("Persistence Layer", [
            "SQLite Database: Patients, Observations, Scenarios, Provenance tables with constraints and indexes"
        ])
    ]
    
    for section_name, items in components:
        content.append(Paragraph(section_name, heading_style))
        for item in items:
            content.append(Paragraph(f"• {item}", normal_style))
        content.append(Spacer(1, 0.1*inch))
    
    content.append(PageBreak())
    
    # Data Flow
    content.append(Paragraph("Data Flow", heading_style))
    
    content.append(Paragraph("Observation Ingestion Flow", heading_style))
    obs_flow = """
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
"""
    content.append(Paragraph(obs_flow, code_style))
    content.append(Spacer(1, 0.2*inch))
    
    content.append(Paragraph("Scenario Simulation Flow", heading_style))
    scenario_flow = """
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
"""
    content.append(Paragraph(scenario_flow, code_style))
    content.append(Spacer(1, 0.2*inch))
    
    content.append(Paragraph("Risk Assessment Flow", heading_style))
    risk_flow = """
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
"""
    content.append(Paragraph(risk_flow, code_style))
    content.append(Spacer(1, 0.2*inch))
    
    content.append(PageBreak())
    
    # Security
    content.append(Paragraph("Security Considerations", heading_style))
    
    security_items = [
        ("Input Validation", "All user inputs validated at service layer, range checking, unit validation, timestamp validation"),
        ("SQL Injection Prevention", "Parameterized queries throughout, no string concatenation, foreign key constraints"),
        ("File Upload Security", "File type restrictions (CSV only), 16 MB size limits, secure filename handling, upload isolation"),
        ("Session Security", "CSRF protection, secure session configuration, environment-based secret keys"),
        ("Data Privacy", "No external API calls, local-only storage, no credentials in logs, synthetic data for demo")
    ]
    
    for title, desc in security_items:
        content.append(Paragraph(f"<b>{title}:</b> {desc}", normal_style))
    
    content.append(Spacer(1, 0.2*inch))
    
    # Technology Stack
    content.append(Paragraph("Technology Stack", heading_style))
    
    tech_data = [
        ["Component", "Technology"],
        ["Backend", "Python 3.14.6, Flask 3.0.3, SQLite"],
        ["Frontend", "HTML5, CSS3, Vanilla JavaScript, Jinja2"],
        ["Dependencies", "NumPy 1.26.4, Pandas 2.2.2, Gunicorn 21.2.0"],
        ["Development", "Pytest 8.2.0, pytest-cov 5.0.0"]
    ]
    
    tech_table = Table(tech_data, colWidths=[2*inch, 4*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    content.append(tech_table)
    content.append(Spacer(1, 0.2*inch))
    
    # Deployment
    content.append(Paragraph("Deployment Architecture", heading_style))
    content.append(Paragraph(
        "Production deployment on Render: Internet → Render Load Balancer → Gunicorn WSGI Server → "
        "Flask Application → SQLite Database (Ephemeral Storage)",
        normal_style
    ))
    
    deployment_features = [
        "Stateless application design",
        "Ephemeral filesystem (data resets on redeploy)",
        "Health check endpoint for monitoring",
        "Memory-efficient (<512 MB target)",
        "No background workers",
        "No external dependencies"
    ]
    
    for feature in deployment_features:
        content.append(Paragraph(f"• {feature}", normal_style))
    
    content.append(Spacer(1, 0.2*inch))
    
    # Footer
    content.append(Paragraph(
        "Generated for Swasthya Twin - Happiest Health Digital Twin Challenge 2026",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER, textColor=colors.grey)
    ))
    
    doc.build(content)
    print(f"Architecture PDF generated: {output_path}")

if __name__ == "__main__":
    import os
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'docs', 'architecture')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'architecture.pdf')
    create_architecture_pdf(output_path)
