import React, { useState, useRef } from 'react';
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
  Loader2,
  X
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
  const [isImporting, setIsImporting] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

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

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setImportErrors([]);
      setImportSuccessMsg(null);
      setImportedPreview(null);
    }
  };

  const handleCommitImport = async () => {
    if (!selectedFile) {
      setImportErrors(['Please select a CSV file to import.']);
      return;
    }

    setIsImporting(true);
    setImportErrors([]);
    setImportSuccessMsg(null);

    try {
      const result = await apiClient.importCSV(activePatientId, selectedFile);
      setImportSuccessMsg(result.message);
      setImportedPreview(result.observations);
      onImportObservations(result.observations);
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err: any) {
      console.error('Failed to import CSV:', err);
      if (err.message) {
        setImportErrors([err.message]);
      } else {
        setImportErrors(['Failed to import CSV. Please check the file format and try again.']);
      }
    } finally {
      setIsImporting(false);
    }
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
                  CSV Batch Importer
                </h3>
              </div>
              <span className="text-xs text-slate-400">Flask Backend</span>
            </div>

            <div className="space-y-3 text-xs">
              <p className="text-slate-500">
                Upload a CSV file to import observations from external devices, EHR exports, or your Flask backend.
              </p>

              <div className="border-2 border-dashed border-slate-300 rounded-lg p-4 text-center hover:border-teal-400 transition-colors">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".csv"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="csv-file-input"
                />
                <label
                  htmlFor="csv-file-input"
                  className="cursor-pointer flex flex-col items-center gap-2"
                >
                  <FileSpreadsheet className="w-8 h-8 text-slate-400" />
                  <span className="text-slate-600">
                    {selectedFile ? selectedFile.name : 'Click to select a CSV file'}
                  </span>
                  <span className="text-slate-400 text-[10px]">
                    Max file size: 16MB
                  </span>
                </label>
                {selectedFile && (
                  <button
                    onClick={(e) => {
                      e.preventDefault();
                      setSelectedFile(null);
                      if (fileInputRef.current) {
                        fileInputRef.current.value = '';
                      }
                    }}
                    className="mt-2 text-rose-600 hover:text-rose-700 text-[10px] flex items-center gap-1"
                  >
                    <X className="w-3 h-3" />
                    Remove file
                  </button>
                )}
              </div>

              {importErrors.length > 0 && (
                <div className="p-3 bg-rose-50 border border-rose-200 rounded text-xs text-rose-800 space-y-1">
                  <div className="font-semibold flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-rose-600" />
                    <span>Import Errors:</span>
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
                    Successfully imported {importedPreview.length} observations:
                  </div>
                  <div className="max-h-28 overflow-y-auto font-mono text-[11px] divide-y divide-teal-200/60">
                    {importedPreview.slice(0, 10).map((p, i) => (
                      <div key={i} className="py-1 flex justify-between">
                        <span>{p.recordedAt} · {p.metricKey}</span>
                        <span className="font-bold">{p.value} {p.unit}</span>
                      </div>
                    ))}
                    {importedPreview.length > 10 && (
                      <div className="py-1 text-slate-500 text-center">
                        ... and {importedPreview.length - 10} more
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-3">
            <button
              onClick={handleCommitImport}
              disabled={!selectedFile || isImporting}
              className="px-4 py-2 text-xs font-semibold text-white bg-teal-800 hover:bg-teal-900 rounded transition-colors shadow-2xs disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isImporting ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Importing...</span>
                </>
              ) : (
                <>
                  <Upload className="w-3.5 h-3.5" />
                  <span>Import CSV</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
