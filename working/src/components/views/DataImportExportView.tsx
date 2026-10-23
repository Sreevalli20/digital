import React, { useState } from 'react';
import { Observation, PatientProfile } from '../../types/health';
import { METRIC_DEFINITIONS } from '../../data/mockData';
import { apiClient } from '../../api/client';
import {
  Download,
  Upload,
  FileSpreadsheet,
  CheckCircle,
  AlertTriangle,
  Code,
  Database,
  FileCheck2,
  Copy,
  Check,
  Loader2
} from 'lucide-react';

interface DataImportExportViewProps {
  observations: Observation[];
  patients: PatientProfile[];
  activePatientId: string;
  onImportObservations: (imported: Observation[]) => void;
}

export const DataImportExportView: React.FC<DataImportExportViewProps> = ({
  observations,
  patients,
  activePatientId,
  onImportObservations
}) => {
  const [selectedExportScope, setSelectedExportScope] = useState<'current' | 'all'>('current');
  const [copiedJson, setCopiedJson] = useState(false);
  const [importedPreview, setImportedPreview] = useState<Observation[] | null>(null);
  const [importErrors, setImportErrors] = useState<string[]>([]);
  const [importSuccessMsg, setImportSuccessMsg] = useState<string | null>(null);
  const [isExporting, setIsExporting] = useState(false);

  // Sample CSV text that can be pasted or imported
  const [customCsvInput, setCustomCsvInput] = useState<string>(
    `observation_id,patient_id,recorded_at,metric_key,value,unit,category,context_notes,is_synthetic\n` +
      `demo-import-1,${activePatientId},2026-10-21,systolic_bp,128,mmHg,cardiovascular,"Home automated test",1\n` +
      `demo-import-2,${activePatientId},2026-10-21,diastolic_bp,82,mmHg,cardiovascular,"Home automated test",1\n` +
      `demo-import-3,${activePatientId},2026-10-22,fasting_glucose,102,mg/dL,metabolic,"Fasted 12h morning check",1`
  );

  const exportObservations =
    selectedExportScope === 'current'
      ? observations.filter((o) => o.patientId === activePatientId)
      : observations;

  const handleDownloadCsv = async () => {
    setIsExporting(true);
    try {
      const blob = await apiClient.exportPatientData(activePatientId, 'csv');
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute(
        'download',
        `swasthya_twin_${selectedExportScope === 'current' ? activePatientId : 'all_cohort'}_${new Date().toISOString().split('T')[0]}.csv`
      );
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to export CSV:', err);
      setImportErrors(['Failed to export data from backend. Please try again.']);
    } finally {
      setIsExporting(false);
    }
  };

  const handleValidateCsv = () => {
    setImportSuccessMsg(null);
    // Client-side validation only - actual import would require backend CSV upload endpoint
    // For now, we'll do basic CSV parsing validation
    const lines = customCsvInput.split(/\r?\n/).filter((l) => l.trim().length > 0);
    if (lines.length < 2) {
      setImportErrors(['CSV file is empty or missing data rows.']);
      setImportedPreview(null);
      return;
    }

    const headerLine = lines[0].toLowerCase();
    const requiredCols = ['patient_id', 'recorded_at', 'metric_key', 'value'];
    const errors: string[] = [];
    for (const col of requiredCols) {
      if (!headerLine.includes(col)) {
        errors.push(`Missing mandatory column header: ${col}`);
      }
    }

    if (errors.length > 0) {
      setImportErrors(errors);
      setImportedPreview(null);
    } else {
      setImportErrors([]);
      setImportSuccessMsg('CSV schema validated. Note: Actual import requires backend file upload endpoint (not yet implemented).');
    }
  };

  const handleCommitImport = () => {
    // This would require a backend file upload endpoint
    // For now, show a message that this is not yet fully implemented
    setImportSuccessMsg('CSV import requires backend file upload endpoint. Please use the Flask dashboard for CSV uploads.');
    setImportedPreview(null);
  };

  const handleCopyFhirJson = () => {
    const fhirSample = {
      resourceType: 'Bundle',
      type: 'collection',
      id: `swasthya-twin-export-${Date.now()}`,
      meta: {
        lastUpdated: new Date().toISOString()
      },
      entry: exportObservations.slice(0, 10).map((o) => ({
        resource: {
          resourceType: 'Observation',
          id: o.id,
          status: 'final',
          code: {
            text: METRIC_DEFINITIONS[o.metricKey]?.label || o.metricKey
          },
          subject: {
            reference: `Patient/${o.patientId}`
          },
          effectiveDateTime: o.recordedAt,
          valueQuantity: {
            value: o.value,
            unit: o.unit
          },
          note: o.contextNotes ? [{ text: o.contextNotes }] : undefined
        }
      }))
    };

    navigator.clipboard.writeText(JSON.stringify(fhirSample, null, 2));
    setCopiedJson(true);
    setTimeout(() => setCopiedJson(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Overview Banner */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs">
        <h2 className="text-base font-bold text-slate-900">
          Data Import & Export Gateway
        </h2>
        <p className="text-xs text-slate-500 mt-1 max-w-3xl leading-relaxed">
          Full round-trip interoperability with your existing Python/Flask backend and SQLite database. Export calibrated longitudinal observations in standardized CSV format or FHIR JSON, and validate incoming observation batches before updating the active digital twin state.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Export Panel */}
        <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <div className="flex items-center gap-2">
                <Download className="w-4 h-4 text-teal-800" />
                <h3 className="text-sm font-semibold text-slate-900">
                  Export Longitudinal Records
                </h3>
              </div>
              <span className="text-xs font-mono text-slate-500">
                {exportObservations.length} records ready
              </span>
            </div>

            <div className="space-y-4 text-xs">
              <div>
                <label className="block font-medium text-slate-700 mb-1.5">
                  Export Scope
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => setSelectedExportScope('current')}
                    className={`p-2.5 rounded border text-left transition-colors ${
                      selectedExportScope === 'current'
                        ? 'border-teal-700 bg-teal-50/60 font-semibold text-teal-950'
                        : 'border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    <div>Active Twin ({activePatientId})</div>
                    <div className="text-[11px] text-slate-500 font-normal mt-0.5">
                      {observations.filter((o) => o.patientId === activePatientId).length} observations
                    </div>
                  </button>

                  <button
                    onClick={() => setSelectedExportScope('all')}
                    className={`p-2.5 rounded border text-left transition-colors ${
                      selectedExportScope === 'all'
                        ? 'border-teal-700 bg-teal-50/60 font-semibold text-teal-950'
                        : 'border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    <div>All Cohort Profiles</div>
                    <div className="text-[11px] text-slate-500 font-normal mt-0.5">
                      {observations.length} total records
                    </div>
                  </button>
                </div>
              </div>

              {/* SQLite Schema Mapping Preview */}
              <div className="p-3 bg-slate-50 rounded border border-slate-200/80">
                <span className="font-semibold text-slate-700 block mb-1">
                  Flask / SQLite Schema Compatibility:
                </span>
                <code className="text-[11px] text-slate-600 block font-mono">
                  observation_id, patient_id, recorded_at, metric_key, value, unit, category, context_notes, is_synthetic
                </code>
              </div>
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-3">
            <button
              onClick={handleCopyFhirJson}
              className="flex items-center gap-1.5 text-xs font-medium text-slate-700 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 border border-slate-200 px-3 py-2 rounded transition-colors"
            >
              {copiedJson ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedJson ? 'FHIR Copied' : 'Copy FHIR JSON'}</span>
            </button>

            <button
              onClick={handleDownloadCsv}
              disabled={isExporting}
              className="flex items-center gap-1.5 text-xs font-semibold text-white bg-teal-800 hover:bg-teal-900 px-4 py-2 rounded transition-colors shadow-2xs disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isExporting ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Exporting...</span>
                </>
              ) : (
                <>
                  <Download className="w-3.5 h-3.5" />
                  <span>Download CSV File</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Import & Validator Panel */}
        <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <div className="flex items-center gap-2">
                <Upload className="w-4 h-4 text-teal-800" />
                <h3 className="text-sm font-semibold text-slate-900">
                  CSV Batch Importer & Validator
                </h3>
              </div>
              <span className="text-xs text-slate-400">Schema Check</span>
            </div>

            <div className="space-y-3 text-xs">
              <p className="text-slate-500">
                Paste raw CSV rows below to simulate ingestion from external devices, EHR exports, or your Flask backend.
              </p>

              <textarea
                rows={5}
                value={customCsvInput}
                onChange={(e) => setCustomCsvInput(e.target.value)}
                className="w-full p-2.5 text-[11px] font-mono bg-slate-50 border border-slate-200 rounded text-slate-800 focus:outline-none focus:ring-1 focus:ring-teal-700"
                placeholder="Paste CSV rows..."
              />

              {importErrors.length > 0 && (
                <div className="p-3 bg-rose-50 border border-rose-200 rounded text-xs text-rose-800 space-y-1">
                  <div className="font-semibold flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-rose-600" />
                    <span>Validation Errors Detected:</span>
                  </div>
                  <ul className="list-disc pl-5 space-y-0.5 text-[11px]">
                    {importErrors.map((err, i) => (
                      <li key={i}>{err}</li>
                    ))}
                  </ul>
                </div>
              )}

              {importSuccessMsg && (
                <div className="p-3 bg-emerald-50 border border-emerald-200 rounded text-xs text-emerald-800 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>{importSuccessMsg}</span>
                </div>
              )}

              {importedPreview && (
                <div className="p-3 bg-teal-50 border border-teal-200 rounded text-xs text-teal-900 space-y-2">
                  <div className="font-semibold">
                    Validated {importedPreview.length} observations ready for ingestion:
                  </div>
                  <div className="max-h-28 overflow-y-auto font-mono text-[11px] divide-y divide-teal-200/60">
                    {importedPreview.map((p, i) => (
                      <div key={i} className="py-1 flex justify-between">
                        <span>{p.recordedAt} · {p.metricKey}</span>
                        <span className="font-bold">{p.value} {p.unit}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-3">
            <button
              onClick={handleValidateCsv}
              className="px-3 py-2 text-xs font-medium text-slate-700 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded transition-colors"
            >
              Validate Schema
            </button>
            {importedPreview && (
              <button
                onClick={handleCommitImport}
                className="px-4 py-2 text-xs font-semibold text-white bg-teal-800 hover:bg-teal-900 rounded transition-colors shadow-2xs"
              >
                Commit {importedPreview.length} Records to Twin
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
