"""
Generate Presentation PDF using ReportLab.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

def create_presentation_pdf(output_path):
    """Generate presentation PDF."""
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.darkblue,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.darkblue,
        spaceAfter=20,
        spaceBefore=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.darkblue,
        spaceAfter=10,
        spaceBefore=15
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        leading=14
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        leftIndent=20,
        bulletIndent=10,
        leading=14
    )
    
    content = []
    
    # Slide 1: Title
    content.append(Paragraph("Swasthya Twin", title_style))
    content.append(Paragraph(
        "Explainable, Adaptive Patient Digital Twin",
        ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, spaceAfter=20)
    ))
    content.append(Paragraph(
        "Understand the change. Explore the possibilities. Act earlier.",
        ParagraphStyle('Tagline', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, spaceAfter=30, textColor=colors.darkblue)
    ))
    
    team_data = [
        ["Team Name", "Brain Catalyst"],
        ["Team Member", "Kommavarapu Kameswari Sreevalli"],
        ["College", "VMTW"],
        ["Competition", "Happiest Health Digital Twin Challenge 2026"]
    ]
    
    team_table = Table(team_data, colWidths=[2*inch, 3*inch])
    team_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    content.append(team_table)
    content.append(PageBreak())
    
    # Slide 2: Problem Statement
    content.append(Paragraph("Problem Statement", slide_title_style))
    content.append(Paragraph(
        "Healthcare decisions often rely on single-point measurements or population averages "
        "that may not reflect an individual's unique health trajectory.",
        normal_style
    ))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Key Challenges:", heading_style))
    content.append(Paragraph("• Lack of longitudinal health tracking", bullet_style))
    content.append(Paragraph("• No tools for personal baseline comparison", bullet_style))
    content.append(Paragraph("• Limited ability to explore hypothetical interventions", bullet_style))
    content.append(Paragraph("• Opaque risk assessments without explanations", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Our Solution:", heading_style))
    content.append(Paragraph(
        "Swasthya Twin creates a patient-specific virtual health model that maintains "
        "longitudinal observations, computes personalized risk assessments, and enables "
        "evidence-based scenario exploration.",
        normal_style
    ))
    content.append(PageBreak())
    
    # Slide 3: Healthcare Use Case
    content.append(Paragraph("Healthcare Use Case", slide_title_style))
    content.append(Paragraph("Initial Clinical Focus: Cardiometabolic Health", heading_style))
    content.append(Spacer(1, 0.1*inch))
    content.append(Paragraph("Key Capabilities:", heading_style))
    content.append(Paragraph("• Baseline establishment from individual observations", bullet_style))
    content.append(Paragraph("• Longitudinal trend tracking with rolling averages", bullet_style))
    content.append(Paragraph("• Personalized risk assessment with explainable contributions", bullet_style))
    content.append(Paragraph("• Hypothetical scenario simulation for intervention exploration", bullet_style))
    content.append(Paragraph("• Data quality assessment and uncertainty communication", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Target Users:", heading_style))
    content.append(Paragraph("• Researchers exploring Digital Twin concepts", bullet_style))
    content.append(Paragraph("• Healthcare technology developers", bullet_style))
    content.append(Paragraph("• Educational demonstrations of personalized health modeling", bullet_style))
    content.append(PageBreak())
    
    # Slide 4: System Architecture
    content.append(Paragraph("System Architecture", slide_title_style))
    content.append(Paragraph("Modular, Layered Design", heading_style))
    
    layers = [
        ("Presentation Layer", "Landing page, Demo UI, API routes"),
        ("Application Layer", "Flask application, request handling, security"),
        ("Service Layer", "Digital Twin Engine, Prediction Engine, Scenario Engine, Validators"),
        ("Repository Layer", "Patient, Observation, Scenario repositories"),
        ("Persistence Layer", "SQLite database with schema and indexes")
    ]
    
    for layer, desc in layers:
        content.append(Paragraph(f"<b>{layer}:</b> {desc}", normal_style))
    
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Technology Stack:", heading_style))
    content.append(Paragraph("• Backend: Python 3.14.6, Flask 3.0.3, SQLite", bullet_style))
    content.append(Paragraph("• Frontend: HTML5, CSS3, Vanilla JavaScript, Jinja2", bullet_style))
    content.append(Paragraph("• Dependencies: NumPy, Pandas, Gunicorn", bullet_style))
    content.append(PageBreak())
    
    # Slide 5: Digital Twin Engine
    content.append(Paragraph("Digital Twin Engine", slide_title_style))
    content.append(Paragraph("Core Functionality", heading_style))
    content.append(Paragraph("Computes patient-specific health state from longitudinal observations", normal_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Key Computations:", heading_style))
    content.append(Paragraph("• Baseline calculation: Average of first N observations (default: 3)", bullet_style))
    content.append(Paragraph("• Rolling averages: Time-weighted averages over configurable windows", bullet_style))
    content.append(Paragraph("• Change from baseline: Current value compared to personal normal", bullet_style))
    content.append(Paragraph("• Trend direction: Increasing, decreasing, or stable patterns", bullet_style))
    content.append(Paragraph("• Data quality assessment: Completeness, freshness, consistency scores", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Supported Features:", heading_style))
    content.append(Paragraph("• Resting Heart Rate, Blood Pressure (systolic/diastolic)", bullet_style))
    content.append(Paragraph("• Body Mass Index, Blood Glucose", bullet_style))
    content.append(Paragraph("• Physical Activity, Sleep Duration", bullet_style))
    content.append(PageBreak())
    
    # Slide 6: Risk Assessment Model
    content.append(Paragraph("Risk Assessment Model", slide_title_style))
    content.append(Paragraph("Cardiometabolic Risk Estimator v1.0.0", heading_style))
    content.append(Paragraph("Rules-based screening with personalization (not a trained ML model)", normal_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Methodology:", heading_style))
    content.append(Paragraph("• Evidence-based clinical thresholds (ACC/AHA, WHO, ADA)", bullet_style))
    content.append(Paragraph("• Feature assessment against personalized baselines", bullet_style))
    content.append(Paragraph("• Weighted sum of feature contributions", bullet_style))
    content.append(Paragraph("• Confidence scoring based on data quality", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Output:", heading_style))
    content.append(Paragraph("• Risk Score: 0.0 to 1.0", bullet_style))
    content.append(Paragraph("• Risk Level: LOW, MODERATE, HIGH", bullet_style))
    content.append(Paragraph("• Feature Contributions: Per-feature analysis with explanations", bullet_style))
    content.append(Paragraph("• Confidence Score: Based on data quality", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Limitations Documented:", heading_style))
    content.append(Paragraph("• Not validated for clinical use", bullet_style))
    content.append(Paragraph("• Does not account for medications, comorbidities, family history", bullet_style))
    content.append(PageBreak())
    
    # Slide 7: Scenario Simulation
    content.append(Paragraph("Scenario Simulation", slide_title_style))
    content.append(Paragraph("Hypothetical Intervention Exploration", heading_style))
    content.append(Paragraph(
        "Users can modify health variables within reasonable bounds and see how "
        "hypothetical changes affect risk assessments without modifying historical data.",
        normal_style
    ))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Workflow:", heading_style))
    content.append(Paragraph("1. User creates scenario with feature modifications", bullet_style))
    content.append(Paragraph("2. System validates modifications are within safe ranges", bullet_style))
    content.append(Paragraph("3. Load baseline Digital Twin state and risk", bullet_style))
    content.append(Paragraph("4. Apply modifications and compute new risk", bullet_style))
    content.append(Paragraph("5. Compare baseline vs scenario with risk change quantification", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Key Innovation:", heading_style))
    content.append(Paragraph(
        "Non-destructive testing enables evidence-based exploration of interventions "
        "with clear baseline-to-scenario comparison.",
        normal_style
    ))
    content.append(PageBreak())
    
    # Slide 8: Key Innovations
    content.append(Paragraph("Key Innovations", slide_title_style))
    content.append(Paragraph("Baseline-to-Scenario Evidence Chain", heading_style))
    content.append(Paragraph(
        "Every meaningful change shows a traceable chain: Observed data → validated features → "
        "comparison with personal baseline → algorithm output → explanation → hypothetical scenario comparison",
        normal_style
    ))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Reproducible Calculations", heading_style))
    content.append(Paragraph("• Fixed random seeds for synthetic data generation", bullet_style))
    content.append(Paragraph("• Deterministic state computations", bullet_style))
    content.append(Paragraph("• Versioned model parameters", bullet_style))
    content.append(Paragraph("• Stored calculation metadata", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Explainable Risk Assessment", heading_style))
    content.append(Paragraph("• Per-feature contribution analysis", bullet_style))
    content.append(Paragraph("• Evidence-based clinical thresholds", bullet_style))
    content.append(Paragraph("• Clear uncertainty communication", bullet_style))
    content.append(Paragraph("• Explicit limitations documentation", bullet_style))
    content.append(PageBreak())
    
    # Slide 9: Security and Privacy
    content.append(Paragraph("Security and Privacy", slide_title_style))
    content.append(Paragraph("Implemented Measures", heading_style))
    content.append(Paragraph("• Input validation for all user inputs", bullet_style))
    content.append(Paragraph("• Parameterized SQL queries (SQL injection prevention)", bullet_style))
    content.append(Paragraph("• Secure file upload handling (CSV only, 16 MB limit)", bullet_style))
    content.append(Paragraph("• CSRF protection for state-changing forms", bullet_style))
    content.append(Paragraph("• Environment-based secret keys", bullet_style))
    content.append(Paragraph("• No sensitive data in logs", bullet_style))
    content.append(Paragraph("• No external API calls", bullet_style))
    content.append(Paragraph("• Local-only data storage", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Limitations", heading_style))
    content.append(Paragraph("• Ephemeral storage on free deployment tier", bullet_style))
    content.append(Paragraph("• No authentication system (demo mode)", bullet_style))
    content.append(Paragraph("• No encryption at rest (SQLite)", bullet_style))
    content.append(PageBreak())
    
    # Slide 10: Evaluation Results
    content.append(Paragraph("Evaluation Results", slide_title_style))
    content.append(Paragraph("Functional Testing", heading_style))
    content.append(Paragraph("✓ Database initialization", bullet_style))
    content.append(Paragraph("✓ Patient CRUD operations", bullet_style))
    content.append(Paragraph("✓ Observation validation", bullet_style))
    content.append(Paragraph("✓ CSV import/export", bullet_style))
    content.append(Paragraph("✓ Digital Twin state computation", bullet_style))
    content.append(Paragraph("✓ Risk assessment", bullet_style))
    content.append(Paragraph("✓ Scenario simulation", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Reproducibility Testing", heading_style))
    content.append(Paragraph("✓ Synthetic data generation with fixed seed", bullet_style))
    content.append(Paragraph("✓ State computation determinism", bullet_style))
    content.append(Paragraph("✓ Risk assessment reproducibility", bullet_style))
    content.append(Paragraph("✓ Scenario consistency", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Performance", heading_style))
    content.append(Paragraph("• Startup time: <2 seconds", bullet_style))
    content.append(Paragraph("• Memory footprint: ~100-200 MB typical", bullet_style))
    content.append(Paragraph("• API response time: <500ms for typical operations", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph(
        "<b>Note:</b> This prototype has not been validated on clinical datasets. Results are for demonstration only.",
        normal_style
    ))
    content.append(PageBreak())
    
    # Slide 11: Limitations
    content.append(Paragraph("Limitations", slide_title_style))
    content.append(Paragraph("Technical Limitations", heading_style))
    content.append(Paragraph("• Ephemeral storage on free deployment tier", bullet_style))
    content.append(Paragraph("• No horizontal scaling", bullet_style))
    content.append(Paragraph("• SQLite not suitable for high-concurrency production", bullet_style))
    content.append(Paragraph("• No real-time wearable integration", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Clinical Limitations", heading_style))
    content.append(Paragraph("<b>NOT a clinical diagnostic tool</b>", bullet_style))
    content.append(Paragraph("<b>NOT validated for medical use</b>", bullet_style))
    content.append(Paragraph("• Does not account for medications, comorbidities, or family history", bullet_style))
    content.append(Paragraph("• Population-based guidelines may not apply to all demographics", bullet_style))
    content.append(Paragraph("• No clinical outcome validation", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Data Limitations", heading_style))
    content.append(Paragraph("• Limited to supported observation types", bullet_style))
    content.append(Paragraph("• Requires sufficient historical data for baseline", bullet_style))
    content.append(Paragraph("• Missing data handling is conservative", bullet_style))
    content.append(Paragraph("• No external dataset integration", bullet_style))
    content.append(PageBreak())
    
    # Slide 12: Deployment
    content.append(Paragraph("Deployment", slide_title_style))
    content.append(Paragraph("Render Free Tier Configuration", heading_style))
    content.append(Paragraph("• Runtime: Python 3.14.6", bullet_style))
    content.append(Paragraph("• WSGI Server: Gunicorn (1 worker, 4 threads)", bullet_style))
    content.append(Paragraph("• Target Memory: <512 MB RAM", bullet_style))
    content.append(Paragraph("• Health Check: /health endpoint", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Deployment Characteristics", heading_style))
    content.append(Paragraph("• Stateless application design", bullet_style))
    content.append(Paragraph("• Ephemeral filesystem (data resets on redeploy)", bullet_style))
    content.append(Paragraph("• No external dependencies or paid services", bullet_style))
    content.append(Paragraph("• Manual backup/reset endpoints for demo data management", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Local Development", heading_style))
    content.append(Paragraph("• Python virtual environment", bullet_style))
    content.append(Paragraph("• SQLite database in instance/ directory", bullet_style))
    content.append(Paragraph("• Flask development server for testing", bullet_style))
    content.append(PageBreak())
    
    # Slide 13: Future Work
    content.append(Paragraph("Future Work", slide_title_style))
    content.append(Paragraph("Clinical Validation", heading_style))
    content.append(Paragraph("• Validation on clinical datasets", bullet_style))
    content.append(Paragraph("• Collaboration with healthcare institutions", bullet_style))
    content.append(Paragraph("• Regulatory compliance assessment", bullet_style))
    content.append(Paragraph("• Clinical trial evaluation", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Technical Enhancements", heading_style))
    content.append(Paragraph("• PostgreSQL for production scaling", bullet_style))
    content.append(Paragraph("• Persistent storage layer", bullet_style))
    content.append(Paragraph("• Real wearable device integration", bullet_style))
    content.append(Paragraph("• Asynchronous task processing", bullet_style))
    content.append(Paragraph("• Multi-region deployment", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Feature Expansion", heading_style))
    content.append(Paragraph("• Additional health domains", bullet_style))
    content.append(Paragraph("• Medication tracking", bullet_style))
    content.append(Paragraph("• Comorbidity modeling", bullet_style))
    content.append(Paragraph("• Family history integration", bullet_style))
    content.append(PageBreak())
    
    # Slide 14: Conclusion
    content.append(Paragraph("Conclusion", slide_title_style))
    content.append(Paragraph("Summary", heading_style))
    content.append(Paragraph(
        "Swasthya Twin demonstrates how Digital Twin concepts can be applied to personalized "
        "health monitoring with transparent, explainable, and reproducible computations.",
        normal_style
    ))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Key Strengths", heading_style))
    content.append(Paragraph("• Evidence-oriented design with traceable data chains", bullet_style))
    content.append(Paragraph("• Explainable risk assessments with feature contributions", bullet_style))
    content.append(Paragraph("• Scenario simulation for intervention exploration", bullet_style))
    content.append(Paragraph("• Reproducible and deterministic calculations", bullet_style))
    content.append(Paragraph("• Comprehensive security and privacy measures", bullet_style))
    content.append(Paragraph("• Open-source with MIT license", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph("Resources", heading_style))
    content.append(Paragraph("• GitHub: https://github.com/Sreevalli20/digital.git", bullet_style))
    content.append(Paragraph("• License: MIT", bullet_style))
    content.append(Paragraph("• Team: Brain Catalyst, VMTW", bullet_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(Paragraph(
        "<b>Thank you for reviewing our submission to the Happiest Health Digital Twin Challenge 2026.</b>",
        ParagraphStyle('ThankYou', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=colors.darkblue)
    ))
    
    doc.build(content)
    print(f"Presentation PDF generated: {output_path}")

if __name__ == "__main__":
    import os
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'docs', 'presentation')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'presentation.pdf')
    create_presentation_pdf(output_path)
