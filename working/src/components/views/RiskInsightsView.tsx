import React, { useState } from 'react';
import { PatientProfile, Observation, RiskAssessment } from '../../types/health';
import { evaluateRiskAssessments } from '../../data/mockData';
import {
  ShieldAlert,
  AlertCircle,
  HelpCircle,
  FileCheck2,
  ChevronRight,
  Info,
  Layers,
  Database,
  ArrowRight
} from 'lucide-react';
import { NavTabId } from '../layout/Sidebar';

interface RiskInsightsViewProps {
  patient: PatientProfile;
  observations: Observation[];
  onNavigateTab: (tab: NavTabId) => void;
}

export const RiskInsightsView: React.FC<RiskInsightsViewProps> = ({
  patient,
  observations,
  onNavigateTab
}) => {
  const assessments = evaluateRiskAssessments(patient, observations);
  const [selectedAssessmentId, setSelectedAssessmentId] = useState<string>(assessments[0].id);

  const activeAssessment =
    assessments.find((a) => a.id === selectedAssessmentId) || assessments[0];

  return (
    <div className="space-y-6">
      {/* Prominent Mandatory Clinical Methodology & Disclaimer Box */}
      <div className="bg-amber-50/60 border border-amber-200/90 rounded-lg p-4 text-xs text-amber-900 shadow-2xs">
        <div className="flex items-start gap-3">
          <Info className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h2 className="font-semibold text-amber-950 text-xs">
              Methodology & Non-Diagnostic Clinical Limitation Disclosure
            </h2>
            <p className="leading-relaxed text-amber-900/90">
              The Swasthya Twin risk evaluation engine is a <strong>transparent rules-based screening prototype</strong> designed to observe directional physiological variance over time. It is <strong>not a clinically validated diagnostic tool</strong> or an autonomous machine-learning diagnostic system. All calculations use published epidemiological formulas (ACC/AHA pooled cohorts, ADA screening guidelines, NCEP ATP III) applied strictly to this demo dataset.
            </p>
          </div>
        </div>
      </div>

      {/* Screen Overview: Assessment Selector Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {assessments.map((a) => {
          const isSelected = a.id === activeAssessment.id;
          return (
            <div
              key={a.id}
              onClick={() => setSelectedAssessmentId(a.id)}
              className={`bg-white rounded-lg border p-4 cursor-pointer transition-all ${
                isSelected
                  ? 'border-teal-700 ring-1 ring-teal-700 shadow-xs'
                  : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50/50'
              }`}
            >
              <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                <span>{a.category} Domain</span>
                <span className="font-mono text-[11px] text-slate-400">
                  {a.dataCompletenessPercent}% Complete
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900 leading-snug mb-3">
                {a.title}
              </h3>

              <div className="flex items-baseline justify-between mb-2">
                <span className="text-2xl font-bold font-mono text-slate-900 tabular-nums">
                  {a.scorePercent}%
                </span>
                <span
                  className={`text-xs font-semibold ${
                    a.classification === 'High Risk'
                      ? 'text-rose-700'
                      : a.classification === 'Elevated'
                      ? 'text-amber-700'
                      : a.classification === 'Borderline'
                      ? 'text-yellow-700'
                      : 'text-emerald-700'
                  }`}
                >
                  {a.classification}
                </span>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                <div
                  className={`h-full ${
                    a.classification === 'High Risk'
                      ? 'bg-rose-600'
                      : a.classification === 'Elevated'
                      ? 'bg-amber-600'
                      : 'bg-emerald-600'
                  }`}
                  style={{ width: `${Math.min(100, a.scorePercent * 2)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Deep-Dive Inspection for Selected Assessment */}
      <div className="bg-white rounded-lg border border-slate-200 p-6 shadow-2xs space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 gap-3">
          <div>
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-teal-800" />
              <h3 className="text-base font-bold text-slate-900">
                {activeAssessment.title}
              </h3>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Target Patient: <strong className="font-mono text-slate-800">{patient.id}</strong> ·{' '}
              {activeAssessment.methodologyDescription}
            </p>
          </div>

          <div className="flex items-center gap-3 self-start sm:self-auto">
            <div className="text-right">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">
                Calculated Screening Risk
              </span>
              <span className="text-lg font-bold font-mono text-slate-900">
                {activeAssessment.scorePercent}% ({activeAssessment.classification})
              </span>
            </div>
          </div>
        </div>

        {/* Explainability Breakdown: Contributing Factors */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
              Transparent Factor Contribution Breakdown
            </h4>
            <span className="text-[11px] text-slate-400">
              Deterministic weight allocation from rules engine
            </span>
          </div>

          <div className="space-y-3">
            {activeAssessment.contributingFactors.map((f, idx) => (
              <div
                key={idx}
                className="p-3.5 bg-slate-50 rounded border border-slate-200/80 space-y-2 text-xs"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                  <div className="font-semibold text-slate-800 flex items-center gap-2">
                    <span>{f.factor}</span>
                  </div>
                  <div className="flex items-center gap-2 text-slate-600">
                    <span className="font-mono font-medium text-slate-900">
                      Observed: {f.observedValue}
                    </span>
                    <span className="text-slate-300">·</span>
                    <span className="text-[11px] text-slate-500">
                      {f.baselineComparison}
                    </span>
                  </div>
                </div>

                {/* Contribution bar */}
                <div className="flex items-center gap-3">
                  <div className="flex-1 bg-slate-200 h-2 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${
                        f.impactLevel === 'high'
                          ? 'bg-rose-600'
                          : f.impactLevel === 'moderate'
                          ? 'bg-amber-600'
                          : 'bg-teal-700'
                      }`}
                      style={{ width: `${f.contributionPercent}%` }}
                    />
                  </div>
                  <span className="font-mono text-[11px] text-slate-500 w-16 text-right tabular-nums">
                    {f.contributionPercent}% weight
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Missing Inputs & Data Quality Audit */}
        <div className="p-4 bg-slate-50/80 rounded border border-slate-200 space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-semibold text-slate-800 flex items-center gap-2">
              <FileCheck2 className="w-4 h-4 text-teal-800" />
              <span>Data Completeness & Imputation Audit</span>
            </h4>
            <span className="text-xs font-mono font-medium text-slate-700">
              {activeAssessment.dataCompletenessPercent}% Observed Inputs
            </span>
          </div>

          {activeAssessment.missingInputs.length > 0 ? (
            <div className="space-y-1.5 text-xs text-slate-600">
              <p className="text-[11px] text-amber-800 font-medium">
                The following variables were not observed in {patient.id}'s record and use conservative population baselines:
              </p>
              <ul className="list-disc pl-5 space-y-1 text-slate-700">
                {activeAssessment.missingInputs.map((item, idx) => (
                  <li key={idx} className="font-mono text-[11px]">{item}</li>
                ))}
              </ul>
            </div>
          ) : (
            <p className="text-xs text-emerald-800 font-medium">
              All clinical parameters required by this rules formula were directly observed in {patient.id}'s longitudinal series.
            </p>
          )}
        </div>

        {/* Action Link: Send to Scenario Simulator */}
        <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-t border-slate-100">
          <div className="text-xs text-slate-500">
            Simulate how lifestyle modulations adjust these contributing factors.
          </div>
          <button
            onClick={() => onNavigateTab('simulator')}
            className="flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-white bg-teal-800 hover:bg-teal-900 rounded transition-colors shadow-2xs self-start sm:self-auto"
          >
            <span>Launch What-If Simulation for {patient.id}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
