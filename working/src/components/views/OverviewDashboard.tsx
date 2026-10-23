import React, { useState } from 'react';
import {
  PatientProfile,
  Observation,
  MetricKey
} from '../../types/health';
import {
  METRIC_DEFINITIONS,
  calculateMetricBaseline,
  evaluateRiskAssessments
} from '../../data/mockData';
import { InteractiveTrendChart } from '../common/InteractiveTrendChart';
import {
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  Sliders,
  ShieldAlert,
  Calendar,
  Layers,
  ChevronRight,
  TrendingDown,
  TrendingUp,
  Clock
} from 'lucide-react';
import { NavTabId } from '../layout/Sidebar';

interface OverviewDashboardProps {
  patient: PatientProfile;
  observations: Observation[];
  onNavigateTab: (tab: NavTabId) => void;
  onOpenRecordModal: () => void;
}

export const OverviewDashboard: React.FC<OverviewDashboardProps> = ({
  patient,
  observations,
  onNavigateTab,
  onOpenRecordModal
}) => {
  const [selectedChartMetric, setSelectedChartMetric] = useState<MetricKey>('systolic_bp');
  const [chartTimeRange, setChartTimeRange] = useState<'1M' | '3M' | '6M' | '1Y' | 'ALL'>('ALL');

  // Filter observations for active patient
  const patientObservations = observations
    .filter((o) => o.patientId === patient.id)
    .sort((a, b) => new Date(b.recordedAt).getTime() - new Date(a.recordedAt).getTime());

  // Metrics to feature in the top KPI strip
  const keyMetricKeys: MetricKey[] = [
    'systolic_bp',
    'diastolic_bp',
    'fasting_glucose',
    'hba1c',
    'resting_heart_rate',
    'bmi'
  ];

  const baselines = keyMetricKeys.map((key) =>
    calculateMetricBaseline(patient.id, key, observations, patient.baselineWindowDays)
  );

  const activeBaseline = calculateMetricBaseline(
    patient.id,
    selectedChartMetric,
    observations,
    patient.baselineWindowDays
  );

  const riskAssessments = evaluateRiskAssessments(patient, observations);

  const daysMonitored = Math.max(
    1,
    Math.round(
      (new Date('2026-10-23').getTime() - new Date(patient.enrolledDate).getTime()) /
        (1000 * 60 * 60 * 24)
    )
  );

  return (
    <div className="space-y-6">
      {/* Welcome Banner & Compact Patient Context */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-slate-900">
              Your health, understood over time.
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Track your health measurements over time, establish personal baselines, and explore hypothetical lifestyle scenarios.
            </p>
          </div>

          {/* Compact Patient Demographic & Twin Baseline Metadata */}
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-slate-600 bg-slate-50 border border-slate-200/80 rounded px-3.5 py-2">
            <div>
              <span className="text-slate-400">Twin ID:</span>{' '}
              <span className="font-mono font-semibold text-slate-900">{patient.id}</span>
            </div>
            <span className="text-slate-300" aria-hidden="true">·</span>
            <div>
              <span className="text-slate-400">Demographics:</span>{' '}
              <span className="font-medium text-slate-800">
                {2026 - patient.birthYear}y / {patient.sexAtBirth}
              </span>
            </div>
            <span className="text-slate-300" aria-hidden="true">·</span>
            <div>
              <span className="text-slate-400">Observations:</span>{' '}
              <span className="font-mono font-semibold text-teal-800">
                {patientObservations.length} records
              </span>
            </div>
            <span className="text-slate-300" aria-hidden="true">·</span>
            <div>
              <span className="text-slate-400">History:</span>{' '}
              <span className="font-medium text-slate-800">{daysMonitored} days</span>
            </div>
            <span className="text-slate-300" aria-hidden="true">·</span>
            <div>
              <span className="text-slate-400">Baseline State:</span>{' '}
              <span className="font-medium text-emerald-800">
                {patient.monitoringStatus}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Key Recorded Biomarkers Grid */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
            Latest Recorded Measurements & Personal Baselines
          </h2>
          <span className="text-xs text-slate-500">
            Compared to early baseline calibration window ({patient.baselineWindowDays} days)
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
          {baselines.map((b) => {
            const def = METRIC_DEFINITIONS[b.metricKey];
            const hasData = b.observationCount > 0;
            const delta = b.deltaFromBaseline;
            const isFavorable =
              b.metricKey === 'hdl_cholesterol' ? delta > 0 : delta <= 0;

            return (
              <div
                key={b.metricKey}
                onClick={() => setSelectedChartMetric(b.metricKey)}
                className={`bg-white rounded-lg border p-3.5 transition-all cursor-pointer ${
                  selectedChartMetric === b.metricKey
                    ? 'border-teal-700 ring-1 ring-teal-700 shadow-xs'
                    : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50/50'
                }`}
              >
                <div className="text-[11px] text-slate-500 font-medium truncate mb-1">
                  {def.shortLabel}
                </div>
                <div className="flex items-baseline gap-1.5 mb-1">
                  <span className="text-xl font-bold font-mono text-slate-900 tabular-nums">
                    {hasData ? b.latestValue : '—'}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">
                    {def.unit}
                  </span>
                </div>

                {/* Personal Baseline Delta */}
                {hasData && b.observationCount >= 2 ? (
                  <div className="flex items-center gap-1 text-[11px] font-sans">
                    {delta < 0 ? (
                      <TrendingDown
                        className={`w-3.5 h-3.5 ${
                          isFavorable ? 'text-emerald-600' : 'text-amber-600'
                        }`}
                      />
                    ) : delta > 0 ? (
                      <TrendingUp
                        className={`w-3.5 h-3.5 ${
                          isFavorable ? 'text-emerald-600' : 'text-amber-600'
                        }`}
                      />
                    ) : (
                      <span className="text-slate-400">—</span>
                    )}
                    <span
                      className={`font-mono tabular-nums ${
                        isFavorable ? 'text-emerald-700' : 'text-amber-700'
                      }`}
                    >
                      {delta > 0 ? '+' : ''}
                      {delta} {def.unit}
                    </span>
                    <span className="text-[10px] text-slate-400">vs base</span>
                  </div>
                ) : (
                  <span className="text-[11px] text-slate-400">Calibrating</span>
                )}

                {/* Clinical Range Tag (Unboxed, clean text) */}
                <div className="mt-2 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px]">
                  <span className="text-slate-400">Target: {def.optimalTarget}</span>
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
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Main Longitudinal Trend Analytics Card */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-semibold text-slate-900">
                Longitudinal Trajectory: {METRIC_DEFINITIONS[selectedChartMetric].label}
              </h2>
              <span className="text-xs text-slate-400 font-mono">
                ({METRIC_DEFINITIONS[selectedChartMetric].unit})
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Twin baseline calibration mean of{' '}
              <strong className="text-slate-800 font-mono">
                {activeBaseline.observationCount >= 2 ? activeBaseline.mean : '—'}{' '}
                {METRIC_DEFINITIONS[selectedChartMetric].unit}
              </strong>{' '}
              established over early observation interval.
            </p>
          </div>

          {/* Time range selector tabs */}
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded">
            {(['1M', '3M', '6M', '1Y', 'ALL'] as const).map((range) => (
              <button
                key={range}
                onClick={() => setChartTimeRange(range)}
                className={`px-2.5 py-1 text-xs font-medium rounded transition-colors ${
                  chartTimeRange === range
                    ? 'bg-white text-slate-900 shadow-2xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {range}
              </button>
            ))}
          </div>
        </div>

        {/* Chart Viewport */}
        <div className="pt-4">
          <InteractiveTrendChart
            observations={observations.filter((o) => o.patientId === patient.id)}
            metricKey={selectedChartMetric}
            baseline={activeBaseline}
            timeRange={chartTimeRange}
            height={280}
            showBaselineBand={true}
            showClinicalReference={true}
          />
        </div>

        {/* Chart Legend & Explanation */}
        <div className="mt-4 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between text-xs text-slate-500 gap-4">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-0.5 bg-teal-700" />
              <span>Observed Twin Measurements</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-0.5 border-b-2 border-dashed border-teal-800" />
              <span>Personal Baseline Mean</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-2 bg-emerald-100 rounded-xs" />
              <span>Normal Reference Interval</span>
            </div>
          </div>
          <button
            onClick={() => onNavigateTab('trends')}
            className="text-xs font-medium text-teal-800 hover:text-teal-900 hover:underline flex items-center gap-1"
          >
            <span>Deep Dive Analytics</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Two Column Section: Risk Screening & Scenario Simulation Link */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Assessment Summary Card */}
        <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-teal-800" />
                <h3 className="text-sm font-semibold text-slate-900">
                  Rules-Based Screening Insights
                </h3>
              </div>
              <span className="text-[11px] text-slate-400 font-sans">
                Prototype Model
              </span>
            </div>

            <p className="text-xs text-slate-600 mb-4">
              Transparent, non-diagnostic screening formulas evaluating longitudinal trajectory against established clinical trial cohorts.
            </p>

            <div className="space-y-3">
              {riskAssessments.slice(0, 2).map((ra) => (
                <div
                  key={ra.id}
                  className="p-3 bg-slate-50 rounded border border-slate-200/80"
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs font-semibold text-slate-800">
                      {ra.title}
                    </span>
                    <span
                      className={`text-xs font-semibold font-mono ${
                        ra.classification === 'High Risk'
                          ? 'text-rose-700'
                          : ra.classification === 'Elevated'
                          ? 'text-amber-700'
                          : 'text-emerald-700'
                      }`}
                    >
                      {ra.scorePercent}% ({ra.classification})
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-500 mb-2">
                    Primary Driver:{' '}
                    <strong className="text-slate-700">
                      {ra.contributingFactors[0]?.factor}
                    </strong>{' '}
                    ({ra.contributingFactors[0]?.observedValue})
                  </div>
                  {/* Progress bar */}
                  <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${
                        ra.classification === 'High Risk'
                          ? 'bg-rose-600'
                          : ra.classification === 'Elevated'
                          ? 'bg-amber-600'
                          : 'bg-emerald-600'
                      }`}
                      style={{ width: `${Math.min(100, ra.scorePercent * 2)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
            <span className="text-[11px] text-slate-400">
              Not a diagnostic tool. Rules-based screening only.
            </span>
            <button
              onClick={() => onNavigateTab('risk')}
              className="text-xs font-medium text-teal-800 hover:text-teal-900 flex items-center gap-1 hover:underline"
            >
              <span>Examine Factors</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Scenario Simulator Workspace Prompt Card */}
        <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Sliders className="w-4 h-4 text-teal-800" />
                <h3 className="text-sm font-semibold text-slate-900">
                  Hypothetical Scenario Simulator
                </h3>
              </div>
              <span className="text-[11px] text-teal-700 font-sans font-medium">
                Twin Projection
              </span>
            </div>

            <p className="text-xs text-slate-600 mb-3">
              Simulate the physiological impact of evidence-based lifestyle modulations (DASH sodium reduction, aerobic activity, sleep restorative windows) on {patient.id}'s personal baseline.
            </p>

            <div className="p-3 bg-teal-50/50 rounded border border-teal-100 space-y-2 text-xs">
              <div className="flex items-center justify-between text-teal-950 font-medium">
                <span>Simulate lifestyle interventions on your baseline</span>
              </div>
              <p className="text-[11px] text-teal-900/80">
                Adjust activity, diet, sleep, and weight parameters to estimate potential changes in blood pressure, glucose, and heart rate.
              </p>
              <p className="text-[10px] text-teal-800/70 pt-1">
                Requires recorded observations to establish a baseline.
              </p>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
            <span className="text-[11px] text-slate-400">
              Interactive sandbox for patient engagement
            </span>
            <button
              onClick={() => onNavigateTab('simulator')}
              className="text-xs font-semibold text-white bg-teal-800 hover:bg-teal-900 px-3 py-1.5 rounded transition-colors flex items-center gap-1.5 shadow-2xs"
            >
              <span>Launch Simulator</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Recent Observations Table */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs">
        <div className="flex items-center justify-between mb-4 pb-2 border-b border-slate-100">
          <div>
            <h3 className="text-sm font-semibold text-slate-900">
              Recent Recorded Observations ({patient.id})
            </h3>
            <p className="text-xs text-slate-500">
              Latest 5 chronological measurements entered into the digital twin ledger.
            </p>
          </div>
          <button
            onClick={() => onNavigateTab('observations')}
            className="text-xs font-medium text-teal-800 hover:text-teal-900 hover:underline flex items-center gap-1"
          >
            <span>View All ({patientObservations.length})</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 font-medium bg-slate-50/70">
                <th className="py-2.5 px-3">Date</th>
                <th className="py-2.5 px-3">Biomarker / Metric</th>
                <th className="py-2.5 px-3 text-right">Value</th>
                <th className="py-2.5 px-3">Category</th>
                <th className="py-2.5 px-3">Context / Method</th>
                <th className="py-2.5 px-3">Record Type</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {patientObservations.slice(0, 5).map((obs) => {
                const def = METRIC_DEFINITIONS[obs.metricKey];
                return (
                  <tr key={obs.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-2.5 px-3 font-mono text-slate-600 whitespace-nowrap">
                      {obs.recordedAt}
                    </td>
                    <td className="py-2.5 px-3 font-medium text-slate-900">
                      {def?.label || obs.metricKey}
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono font-semibold text-slate-900 tabular-nums">
                      {obs.value} <span className="text-slate-400 font-normal">{obs.unit}</span>
                    </td>
                    <td className="py-2.5 px-3 capitalize text-slate-500">
                      {obs.category}
                    </td>
                    <td className="py-2.5 px-3 text-slate-500 truncate max-w-xs">
                      {obs.contextNotes || 'Routine observation'}
                    </td>
                    <td className="py-2.5 px-3 text-slate-400 font-mono text-[11px]">
                      Synthetic Demo
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
