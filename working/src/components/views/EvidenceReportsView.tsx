import React, { useRef } from 'react';
import { PatientProfile, Observation, MetricKey } from '../../types/health';
import {
  calculateMetricBaseline,
  evaluateRiskAssessments,
  METRIC_DEFINITIONS
} from '../../data/mockData';
import {
  Printer,
  FileText,
  Download,
  ShieldCheck,
  CheckCircle2,
  Calendar,
  Activity,
  HeartPulse
} from 'lucide-react';

interface EvidenceReportsViewProps {
  patient: PatientProfile;
  observations: Observation[];
}

export const EvidenceReportsView: React.FC<EvidenceReportsViewProps> = ({
  patient,
  observations
}) => {
  const reportDate = new Date().toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  });

  const patientObs = observations
    .filter((o) => o.patientId === patient.id)
    .sort((a, b) => new Date(a.recordedAt).getTime() - new Date(b.recordedAt).getTime());

  const keyMetrics: MetricKey[] = [
    'systolic_bp',
    'diastolic_bp',
    'fasting_glucose',
    'hba1c',
    'resting_heart_rate',
    'ldl_cholesterol',
    'bmi'
  ];

  const baselines = keyMetrics.map((k) =>
    calculateMetricBaseline(patient.id, k, observations, patient.baselineWindowDays)
  );

  const riskAssessments = evaluateRiskAssessments(patient, observations);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6">
      {/* Top Action Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-4 rounded-lg border border-slate-200 shadow-2xs">
        <div>
          <h2 className="text-sm font-semibold text-slate-900">
            Digital Health Twin Evidence & Longitudinal Report
          </h2>
          <p className="text-xs text-slate-500">
            Clinical-grade structured export for review, physician consultation, and audit records.
          </p>
        </div>

        <button
          onClick={handlePrint}
          className="flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-white bg-teal-800 hover:bg-teal-900 rounded transition-colors shadow-2xs self-start sm:self-auto"
        >
          <Printer className="w-3.5 h-3.5" />
          <span>Print / Export PDF Report</span>
        </button>
      </div>

      {/* Printable Report Document Sheet */}
      <div className="bg-white rounded-lg border border-slate-200 p-8 shadow-xs max-w-4xl mx-auto space-y-6 font-sans text-slate-800 print:border-none print:shadow-none print:p-0">
        {/* Document Header */}
        <div className="border-b-2 border-slate-900 pb-5">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <HeartPulse className="w-5 h-5 text-teal-800" />
                <span className="text-xs font-bold uppercase tracking-wider text-teal-900">
                  Swasthya Twin Health Analytics
                </span>
              </div>
              <h1 className="text-xl font-bold tracking-tight text-slate-900">
                Longitudinal Twin Baseline & Variance Audit
              </h1>
              <p className="text-xs text-slate-500 mt-0.5">
                Happiest Health Digital Twin Research Protocol 2026
              </p>
            </div>

            <div className="text-right text-xs space-y-1">
              <div>
                <span className="text-slate-400">Generated:</span>{' '}
                <span className="font-mono font-medium text-slate-800">{reportDate}</span>
              </div>
              <div>
                <span className="text-slate-400">Cohort ID:</span>{' '}
                <span className="font-mono font-bold text-slate-900">{patient.id}</span>
              </div>
              <div>
                <span className="text-slate-400">Synthetic Classification:</span>{' '}
                <span className="text-emerald-800 font-medium">Research Demo</span>
              </div>
            </div>
          </div>
        </div>

        {/* Patient Profile & Baseline Setup */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-slate-50 rounded border border-slate-200 text-xs">
          <div>
            <span className="text-slate-400 block text-[11px]">Chronological Age</span>
            <span className="font-semibold text-slate-900">
              {2026 - patient.birthYear} years ({patient.sexAtBirth})
            </span>
          </div>
          <div>
            <span className="text-slate-400 block text-[11px]">Observation History</span>
            <span className="font-semibold text-slate-900 font-mono">
              {patientObs.length} records recorded
            </span>
          </div>
          <div>
            <span className="text-slate-400 block text-[11px]">Calibration Window</span>
            <span className="font-semibold text-slate-900">
              {patient.baselineWindowDays} days calibration
            </span>
          </div>
          <div>
            <span className="text-slate-400 block text-[11px]">Monitoring Status</span>
            <span className="font-semibold text-teal-800">
              {patient.monitoringStatus}
            </span>
          </div>
        </div>

        {/* Section 1: Baseline Variance Table */}
        <div className="space-y-3">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            1. Calibrated Biomarker Baselines vs. Latest Observed State
          </h2>

          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 font-medium bg-slate-50">
                <th className="py-2 px-3">Biomarker</th>
                <th className="py-2 px-3 text-right">Established Baseline</th>
                <th className="py-2 px-3 text-right">Latest Observed</th>
                <th className="py-2 px-3 text-right">Net Shift (Delta)</th>
                <th className="py-2 px-3">Clinical Reference</th>
                <th className="py-2 px-3">Evaluation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {baselines.map((b) => {
                const def = METRIC_DEFINITIONS[b.metricKey];
                const hasData = b.observationCount > 0;
                return (
                  <tr key={b.metricKey}>
                    <td className="py-2.5 px-3 font-medium text-slate-900">
                      {def.label}
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono tabular-nums text-slate-700">
                      {hasData && b.observationCount >= 2
                        ? `${b.mean} ${def.unit}`
                        : 'Uncalibrated'}
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono font-bold tabular-nums text-slate-900">
                      {hasData ? `${b.latestValue} ${def.unit}` : '—'}
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono tabular-nums">
                      {hasData && b.observationCount >= 2 ? (
                        <span
                          className={
                            b.deltaFromBaseline < 0
                              ? 'text-emerald-700'
                              : b.deltaFromBaseline > 0
                              ? 'text-amber-700'
                              : 'text-slate-500'
                          }
                        >
                          {b.deltaFromBaseline > 0 ? '+' : ''}
                          {b.deltaFromBaseline} {def.unit}
                        </span>
                      ) : (
                        '—'
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-slate-500">
                      {def.optimalTarget}
                    </td>
                    <td className="py-2.5 px-3">
                      <span
                        className={`font-medium ${
                          b.statusLabel === 'Optimal'
                            ? 'text-emerald-700'
                            : b.statusLabel === 'High Risk'
                            ? 'text-rose-700'
                            : 'text-amber-700'
                        }`}
                      >
                        {b.statusLabel}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Section 2: Screening Risk Profiles */}
        <div className="space-y-3">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900 border-b border-slate-200 pb-1">
            2. Rules-Based Longitudinal Screening Assessments
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {riskAssessments.map((ra) => (
              <div key={ra.id} className="p-3 bg-slate-50 border border-slate-200 rounded text-xs space-y-1.5">
                <div className="font-semibold text-slate-900">{ra.title}</div>
                <div className="text-lg font-bold font-mono text-teal-900">
                  {ra.scorePercent}% ({ra.classification})
                </div>
                <p className="text-[11px] text-slate-500 leading-snug">
                  {ra.methodologyDescription}
                </p>
                <div className="text-[10px] text-slate-400 pt-1">
                  Primary factor: {ra.contributingFactors[0]?.factor}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Section 3: Clinical Rationale & Footnotes */}
        <div className="p-4 bg-slate-50 rounded border border-slate-200 text-xs text-slate-600 space-y-2">
          <h3 className="font-semibold text-slate-800">
            Clinical Governance & Evidence Base
          </h3>
          <p className="text-[11px] leading-relaxed">
            Longitudinal baseline models utilize sequential observation clustering with dynamic Bayesian variance boundaries. Lifestyle what-if response curves are calibrated against meta-analyses from the DASH-Sodium multi-center trial (Appel et al.), the Diabetes Prevention Program (DPP Research Group), and the Look AHEAD trial.
          </p>
          <p className="text-[10px] text-slate-400 italic">
            Disclaimer: Swasthya Twin is an investigational software prototype for the Happiest Health Digital Twin Challenge 2026. This document is for demonstration purposes using synthetic participant records and does not constitute medical advice or a verified diagnosis.
          </p>
        </div>
      </div>
    </div>
  );
};
