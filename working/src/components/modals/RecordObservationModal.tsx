import React, { useState } from 'react';
import { Observation, MetricKey, PatientProfile } from '../../types/health';
import { METRIC_DEFINITIONS } from '../../data/mockData';
import { X, CheckCircle, AlertCircle } from 'lucide-react';

interface RecordObservationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddObservation: (observation: Observation) => void;
  patients: PatientProfile[];
  currentPatientId: string;
}

export const RecordObservationModal: React.FC<RecordObservationModalProps> = ({
  isOpen,
  onClose,
  onAddObservation,
  patients,
  currentPatientId
}) => {
  const [selectedPatientId, setSelectedPatientId] = useState(currentPatientId);
  const [selectedMetric, setSelectedMetric] = useState<MetricKey>('systolic_bp');
  const [value, setValue] = useState('');
  const [date, setDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [notes, setNotes] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState(false);

  if (!isOpen) return null;

  const currentDef = METRIC_DEFINITIONS[selectedMetric];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const numVal = parseFloat(value);
    if (isNaN(numVal) || value.trim() === '') {
      setError('Please provide a valid numerical observation value.');
      return;
    }

    // Physiological bounds check
    let minBound = 0;
    let maxBound = 1000;
    if (selectedMetric === 'systolic_bp') { minBound = 60; maxBound = 260; }
    else if (selectedMetric === 'diastolic_bp') { minBound = 40; maxBound = 160; }
    else if (selectedMetric === 'fasting_glucose') { minBound = 40; maxBound = 500; }
    else if (selectedMetric === 'hba1c') { minBound = 3.5; maxBound = 18.0; }
    else if (selectedMetric === 'resting_heart_rate') { minBound = 35; maxBound = 220; }
    else if (selectedMetric === 'bmi') { minBound = 12.0; maxBound = 70.0; }

    if (numVal < minBound || numVal > maxBound) {
      setError(`Value ${numVal} is outside physiologically viable range (${minBound}–${maxBound} ${currentDef.unit}).`);
      return;
    }

    const newObs: Observation = {
      id: `obs-manual-${Date.now()}`,
      patientId: selectedPatientId,
      recordedAt: date,
      metricKey: selectedMetric,
      value: Number(numVal.toFixed(currentDef.decimals)),
      unit: currentDef.unit,
      category: currentDef.category,
      contextNotes: notes.trim() || undefined,
      isSynthetic: true
    };

    onAddObservation(newObs);
    setSuccessMsg(true);
    setTimeout(() => {
      setSuccessMsg(false);
      onClose();
      setValue('');
      setNotes('');
    }, 600);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4">
      <div className="bg-white rounded-lg border border-slate-200 shadow-xl max-w-lg w-full overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
          <div>
            <h3 className="text-base font-semibold text-slate-900">Record Clinical Observation</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Append a validated measurement to the patient's longitudinal digital twin record.
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 p-1 rounded hover:bg-slate-100 transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="flex items-start gap-2.5 p-3 text-xs text-amber-800 bg-amber-50 border border-amber-200 rounded">
              <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {successMsg && (
            <div className="flex items-center gap-2 p-3 text-xs text-emerald-800 bg-emerald-50 border border-emerald-200 rounded">
              <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>Observation appended and twin baseline updated.</span>
            </div>
          )}

          {/* Patient Selector */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              Target Patient
            </label>
            <select
              value={selectedPatientId}
              onChange={(e) => setSelectedPatientId(e.target.value)}
              className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded text-slate-900 focus:outline-none focus:ring-1 focus:ring-teal-700 focus:border-teal-700"
            >
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.id} — {p.primaryFocus} ({p.monitoringStatus})
                </option>
              ))}
            </select>
          </div>

          {/* Metric Selector */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                Biomarker / Metric
              </label>
              <select
                value={selectedMetric}
                onChange={(e) => setSelectedMetric(e.target.value as MetricKey)}
                className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded text-slate-900 focus:outline-none focus:ring-1 focus:ring-teal-700 focus:border-teal-700"
              >
                {Object.values(METRIC_DEFINITIONS).map((m) => (
                  <option key={m.key} value={m.key}>
                    {m.label} ({m.unit})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                Measurement Date
              </label>
              <input
                type="date"
                value={date}
                max={new Date().toISOString().split('T')[0]}
                onChange={(e) => setDate(e.target.value)}
                className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded text-slate-900 focus:outline-none focus:ring-1 focus:ring-teal-700 focus:border-teal-700 font-mono"
              />
            </div>
          </div>

          {/* Value Input with Unit & Reference Display */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-xs font-medium text-slate-700">
                Observed Value ({currentDef.unit})
              </label>
              <span className="text-[11px] text-slate-500">
                Optimal: {currentDef.optimalTarget}
              </span>
            </div>
            <div className="relative">
              <input
                type="number"
                step={currentDef.decimals > 0 ? '0.1' : '1'}
                placeholder={`e.g. ${currentDef.normalMin + Math.round((currentDef.normalMax - currentDef.normalMin) / 2)}`}
                value={value}
                onChange={(e) => setValue(e.target.value)}
                className="w-full px-3 py-2 pr-16 text-sm bg-white border border-slate-200 rounded text-slate-900 focus:outline-none focus:ring-1 focus:ring-teal-700 focus:border-teal-700 font-mono tabular-nums"
                required
              />
              <span className="absolute right-3 top-2.5 text-xs text-slate-400 font-mono">
                {currentDef.unit}
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">
              {currentDef.clinicalRelevance}
            </p>
          </div>

          {/* Notes / Clinical Context */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              Clinical Context / Protocol Notes (Optional)
            </label>
            <input
              type="text"
              placeholder="e.g. Morning fasted 10h, verified by omron automated cuff"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded text-slate-900 focus:outline-none focus:ring-1 focus:ring-teal-700 focus:border-teal-700"
            />
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-slate-700 hover:text-slate-900 bg-white hover:bg-slate-50 border border-slate-200 rounded transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-xs font-medium text-white bg-teal-800 hover:bg-teal-900 rounded transition-colors shadow-xs"
            >
              Commit Observation
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
