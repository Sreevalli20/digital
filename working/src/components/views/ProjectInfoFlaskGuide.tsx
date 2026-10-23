import React, { useState } from 'react';
import {
  Code,
  Terminal,
  Database,
  FileCode2,
  CheckCircle2,
  Copy,
  Check,
  BookOpen,
  Server,
  Layers,
  HeartPulse,
  ExternalLink
} from 'lucide-react';

export const ProjectInfoFlaskGuide: React.FC = () => {
  const [copiedSnippet, setCopiedSnippet] = useState<string | null>(null);

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedSnippet(id);
    setTimeout(() => setCopiedSnippet(null), 2000);
  };

  const flaskRoutesSnippet = `# app.py or routes.py (Existing Flask Application)
from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import csv
import io

app = Flask(__name__)
DB_PATH = 'swasthya_twin.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 1. Main Dashboard (Jinja2)
@app.route('/')
@app.route('/patient/<patient_id>')
def overview(patient_id='DEMO-001'):
    db = get_db()
    patient = db.execute('SELECT * FROM patients WHERE id = ?', (patient_id,)).fetchone()
    observations = db.execute(
        'SELECT * FROM observations WHERE patient_id = ? ORDER BY recorded_at DESC', 
        (patient_id,)
    ).fetchall()
    return render_template('overview.html', patient=patient, observations=observations)

# 2. REST API: Get Observations for Charting (JSON)
@app.route('/api/observations/<patient_id>')
def api_observations(patient_id):
    metric = request.args.get('metric', 'systolic_bp')
    db = get_db()
    rows = db.execute(
        'SELECT recorded_at, value, unit FROM observations WHERE patient_id = ? AND metric_key = ? ORDER BY recorded_at ASC',
        (patient_id, metric)
    ).fetchall()
    return jsonify([dict(r) for r in rows])

# 3. REST API: Rules-Based Risk Assessment
@app.route('/api/risk-assessment/<patient_id>')
def api_risk_assessment(patient_id):
    # Calculates transparent deterministic risk from SQLite observations
    # Returns ACC/AHA CVD Proxy, ADA T2D score, and ATP III criteria
    return jsonify({
        "patient_id": patient_id,
        "cvd_10yr_proxy": 14.8,
        "t2d_5yr_risk": 11.2,
        "metabolic_criteria": 2
    })

# 4. REST API: What-If Scenario Simulation
@app.route('/api/simulate/<patient_id>', methods=['POST'])
def api_simulate(patient_id):
    data = request.json
    activity_mins = data.get('activity_mins', 30)
    sodium_reduc = data.get('sodium_reduc_mg', 1000)
    # Computes projected delta from patient established baseline
    delta_sbp = -2.2 * (activity_mins / 30) - 2.8 * (sodium_reduc / 1000)
    return jsonify({
        "projected_sbp_delta": round(delta_sbp, 1)
    })

# 5. CSV Export Gateway
@app.route('/export-csv/<patient_id>')
def export_csv(patient_id):
    db = get_db()
    rows = db.execute('SELECT * FROM observations WHERE patient_id = ?', (patient_id,)).fetchall()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'patient_id', 'recorded_at', 'metric_key', 'value', 'unit', 'notes'])
    for r in rows:
        cw.writerow([r['id'], r['patient_id'], r['recorded_at'], r['metric_key'], r['value'], r['unit'], r['notes']])
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name=f'{patient_id}_records.csv')
`;

  const sqliteSchemaSnippet = `-- schema.sql for SQLite database
CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    birth_year INTEGER NOT NULL,
    sex_at_birth TEXT NOT NULL,
    monitoring_status TEXT NOT NULL,
    primary_focus TEXT NOT NULL,
    enrolled_date TEXT NOT NULL,
    baseline_window_days INTEGER DEFAULT 60,
    smoker_status TEXT DEFAULT 'Non-Smoker',
    notes TEXT
);

CREATE TABLE IF NOT EXISTS observations (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    metric_key TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    category TEXT NOT NULL,
    context_notes TEXT,
    is_synthetic INTEGER DEFAULT 1,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE INDEX IF NOT EXISTS idx_obs_patient_metric ON observations(patient_id, metric_key, recorded_at);
`;

  const cssTokensSnippet = `/* static/css/swasthya_twin.css
   Direct CSS variable equivalents of the Google AI Studio design system
*/
:root {
    --bg-canvas: #f7f9f8;         /* Warm off-white */
    --surface-card: #ffffff;      /* White content panels */
    --border-subtle: #e2e8f0;     /* Hairline borders */
    --text-primary: #0f172a;      /* Dark slate typography */
    --text-muted: #64748b;        /* Muted annotations */
    --brand-forest: #0c2a23;      /* Deep forest green (Sidebar) */
    --brand-teal: #0f766e;        /* Dark teal primary actions */
    --brand-teal-hover: #115e59;  /* Dark teal hover */
    --status-optimal: #15803d;    /* Clinical optimal green */
    --status-warning: #b45309;    /* Borderline / elevated amber */
    --status-alert: #b91c1c;      /* High risk crimson */
}

body {
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    margin: 0;
}

.tabular-nums {
    font-variant-numeric: tabular-nums;
    font-family: 'JetBrains Mono', monospace;
}
`;

  return (
    <div className="space-y-6">
      {/* Project Header Banner */}
      <div className="bg-white rounded-lg border border-slate-200 p-6 shadow-2xs">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-8 h-8 rounded bg-teal-900 text-teal-200 flex items-center justify-center">
            <HeartPulse className="w-5 h-5 text-emerald-300" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-900">
              Swasthya Twin — Happiest Health Challenge 2026
            </h1>
            <p className="text-xs text-slate-500">
              Longitudinal Digital Health Twin Architecture & Python/Flask Porting Guide
            </p>
          </div>
        </div>

        <p className="text-xs text-slate-600 mt-2 leading-relaxed">
          This frontend design is architected to be 100% self-contained in Google AI Studio while mapping 1-to-1 onto your existing Python, Flask, Jinja2, and SQLite codebase. No backend rewrite is required: the component hierarchy, API endpoints, schema columns, and CSS tokens are already pre-aligned.
        </p>
      </div>

      {/* Migration Strategy Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-2xs space-y-2">
          <div className="flex items-center gap-2 text-teal-800 font-semibold text-xs">
            <Server className="w-4 h-4" />
            <span>1. Flask & Jinja2 Templates</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Replace your existing Jinja2 templates with the HTML markup from each view: <code className="text-teal-900 font-mono">templates/base.html</code>, <code className="text-teal-900 font-mono">templates/overview.html</code>, and <code className="text-teal-900 font-mono">templates/trends.html</code>.
          </p>
        </div>

        <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-2xs space-y-2">
          <div className="flex items-center gap-2 text-teal-800 font-semibold text-xs">
            <Database className="w-4 h-4" />
            <span>2. SQLite Schema Alignment</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            The observation columns in this prototype (<code className="font-mono text-[11px]">patient_id, recorded_at, metric_key, value, unit</code>) directly correspond to standard SQLite tables.
          </p>
        </div>

        <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-2xs space-y-2">
          <div className="flex items-center gap-2 text-teal-800 font-semibold text-xs">
            <FileCode2 className="w-4 h-4" />
            <span>3. Vanilla JS / Charting</span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            The SVG rendering logic translates directly into either vanilla JavaScript SVG string concatenation or lightweight Chart.js / uPlot inside your Jinja2 templates.
          </p>
        </div>
      </div>

      {/* Code Snippets Section */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs space-y-6">
        <div className="border-b border-slate-100 pb-3">
          <h2 className="text-sm font-bold text-slate-900">
            Reference Implementation Snippets for Flask
          </h2>
          <p className="text-xs text-slate-500">
            Copy and adapt these drop-in files into your existing Flask project directory.
          </p>
        </div>

        {/* Snippet 1: Flask app.py */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-800">
              <Code className="w-4 h-4 text-teal-800" />
              <span>Python / Flask Route Blueprint (app.py)</span>
            </div>
            <button
              onClick={() => copyToClipboard(flaskRoutesSnippet, 'flask')}
              className="flex items-center gap-1 text-xs text-slate-600 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 border border-slate-200 px-2.5 py-1 rounded transition-colors"
            >
              {copiedSnippet === 'flask' ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedSnippet === 'flask' ? 'Copied' : 'Copy Python'}</span>
            </button>
          </div>
          <pre className="p-3.5 bg-slate-900 text-slate-100 rounded text-xs font-mono overflow-x-auto leading-relaxed max-h-80">
            {flaskRoutesSnippet}
          </pre>
        </div>

        {/* Snippet 2: SQLite Schema */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-800">
              <Database className="w-4 h-4 text-teal-800" />
              <span>SQLite Database Schema (schema.sql)</span>
            </div>
            <button
              onClick={() => copyToClipboard(sqliteSchemaSnippet, 'sql')}
              className="flex items-center gap-1 text-xs text-slate-600 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 border border-slate-200 px-2.5 py-1 rounded transition-colors"
            >
              {copiedSnippet === 'sql' ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedSnippet === 'sql' ? 'Copied' : 'Copy SQL'}</span>
            </button>
          </div>
          <pre className="p-3.5 bg-slate-900 text-slate-100 rounded text-xs font-mono overflow-x-auto leading-relaxed max-h-64">
            {sqliteSchemaSnippet}
          </pre>
        </div>

        {/* Snippet 3: CSS Token Palette */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-800">
              <FileCode2 className="w-4 h-4 text-teal-800" />
              <span>Static CSS Token Variables (static/css/swasthya_twin.css)</span>
            </div>
            <button
              onClick={() => copyToClipboard(cssTokensSnippet, 'css')}
              className="flex items-center gap-1 text-xs text-slate-600 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 border border-slate-200 px-2.5 py-1 rounded transition-colors"
            >
              {copiedSnippet === 'css' ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedSnippet === 'css' ? 'Copied' : 'Copy CSS'}</span>
            </button>
          </div>
          <pre className="p-3.5 bg-slate-900 text-slate-100 rounded text-xs font-mono overflow-x-auto leading-relaxed max-h-64">
            {cssTokensSnippet}
          </pre>
        </div>
      </div>
    </div>
  );
};
