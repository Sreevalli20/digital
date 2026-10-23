import React, { useState, useMemo } from 'react';
import { PatientProfile, Observation, MetricKey } from '../../types/health';
import { METRIC_DEFINITIONS, calculateMetricBaseline } from '../../data/mockData';
import { InteractiveTrendChart } from '../common/InteractiveTrendChart';
import {
  TrendingUp,
  TrendingDown,
  Info,
  Calendar,
  AlertCircle,
  Activity,
  Layers,
  ArrowUpDown,
  Filter
} from 'lucide-react';

interface HealthTrendsViewProps {
  patient: PatientProfile;
  observations: Observation[];
  onOpenRecordModal: () => void;
}

export const HealthTrendsView: React.FC<HealthTrendsViewProps> = ({
  patient,
  observations,
  onOpenRecordModal
}) => {
  const [selectedMetric, setSelectedMetric] = useState<MetricKey>('systolic_bp');
  const [timeRange, setTimeRange] = useState<'1M' | '3M' | '6M' | '1Y' | 'ALL'>('ALL');
  const [sortOrder, setSortOrder] = useState<'desc' | 'asc'>('desc');

  const def = METRIC_DEFINITIONS[selectedMetric];

  // Filter observations for this patient and this metric
  const metricObservations = useMemo(() => {
    return observations
      .filter((o) => o.patientId === patient.id && o.metricKey === selectedMetric)
      .sort((a, b) => {
        const timeA = new Date(a.recordedAt).getTime();
        const timeB = new Date(b.recordedAt).getTime();
        return sortOrder === 'desc' ? timeB - timeA : timeA - timeB;
      });
  }, [observations, patient.id, selectedMetric, sortOrder]);

  const baseline = calculateMetricBaseline(
    patient.id,
    selectedMetric,
    observations,
    patient.baselineWindowDays
  );

  const hasSufficientHistory = metricObservations.length >= 3;

  // Category grouping for the metric selector
  const metricsByCategory = useMemo(() => {
    const categories: Record<string, typeof METRIC_DEFINITIONS[MetricKey][]> = {
      cardiovascular: [],
      metabolic: [],
      anthropometric: []
    };
    for (const m of Object.values(METRIC_DEFINITIONS)) {
      if (categories[m.category]) {
        categories[m.category].push(m);
      }
    }
    return categories;
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Controls: Metric Selector Tabs & Time Range Controls */}
      <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-2xs space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-teal-800" />
            <h2 className="text-sm font-semibold text-slate-900">
              Longitudinal Analytics Selector
            </h2>
            <span className="text-slate-300">|</span>
            <span className="text-xs font-mono font-medium text-slate-700">
              {patient.id}
            </span>
          </div>

          {/* Time range buttons */}
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded text-xs self-start sm:self-auto">
            {(['1M', '3M', '6M', '1Y', 'ALL'] as const).map((r) => (
              <button
                key={r}
                onClick={() => setTimeRange(r)}
                className={`px-2.5 py-1 font-medium rounded transition-colors ${
                  timeRange === r
                    ? 'bg-white text-slate-900 shadow-2xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {r}
              </button>
            ))}
          </div>
        </div>

        {/* Metric Quick Buttons */}
        <div className="flex flex-wrap gap-1.5 pt-1 border-t border-slate-100">
          {Object.values(METRIC_DEFINITIONS).map((m) => {
            const isSelected = m.key === selectedMetric;
            const countForMetric = observations.filter(
              (o) => o.patientId === patient.id && o.metricKey === m.key
            ).length;

            return (
              <button
                key={m.key}
                onClick={() => setSelectedMetric(m.key)}
                className={`px-3 py-1.5 rounded text-xs transition-colors flex items-center gap-2 ${
                  isSelected
                    ? 'bg-teal-900 text-white font-semibold shadow-2xs'
                    : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200/80'
                }`}
              >
                <span>{m.shortLabel}</span>
                <span
                  className={`text-[10px] font-mono px-1.5 py-0.2 rounded ${
                    isSelected
                      ? 'bg-teal-800 text-teal-200'
                      : 'bg-slate-200/80 text-slate-600'
                  }`}
                >
                  {countForMetric}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Longitudinal Analytics Card */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-100 gap-3">
          <div>
            <div className="flex items-baseline gap-2">
              <h3 className="text-base font-bold text-slate-900">{def.label}</h3>
              <span className="text-xs font-mono text-slate-400">({def.unit})</span>
              <span className="text-xs text-slate-300">·</span>
              <span className="text-xs font-medium text-emerald-700">
                Target: {def.optimalTarget}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              {def.description} {def.clinicalRelevance}
            </p>
          </div>

          <button
            onClick={onOpenRecordModal}
            className="text-xs font-semibold text-teal-800 hover:text-teal-900 bg-teal-50 hover:bg-teal-100 border border-teal-200 px-3 py-1.5 rounded self-start md:self-auto transition-colors"
          >
            + Add {def.shortLabel} Measurement
          </button>
        </div>

        {/* Statistical Summary Strip */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 my-4">
          <div className="p-3 bg-slate-50 rounded border border-slate-200/70">
            <span className="text-[11px] text-slate-400 block mb-0.5">Personal Baseline</span>
            <span className="text-base font-bold font-mono text-slate-900 tabular-nums">
              {baseline.observationCount >= 2 ? `${baseline.mean} ${def.unit}` : 'Uncalibrated'}
            </span>
            <span className="text-[10px] text-slate-400 block mt-0.5">
              {baseline.observationCount >= 2 ? `±${baseline.standardDeviation} SD` : 'Requires 2+ obs'}
            </span>
          </div>

          <div className="p-3 bg-slate-50 rounded border border-slate-200/70">
            <span className="text-[11px] text-slate-400 block mb-0.5">Latest Reading</span>
            <span className="text-base font-bold font-mono text-slate-900 tabular-nums">
              {baseline.observationCount > 0 ? `${baseline.latestValue} ${def.unit}` : '—'}
            </span>
            <span className="text-[10px] text-slate-400 block mt-0.5">
              {baseline.latestDate !== 'N/A' ? baseline.latestDate : 'No record'}
            </span>
          </div>

          <div className="p-3 bg-slate-50 rounded border border-slate-200/70">
            <span className="text-[11px] text-slate-400 block mb-0.5">Delta vs Baseline</span>
            <span
              className={`text-base font-bold font-mono tabular-nums ${
                baseline.deltaFromBaseline < 0
                  ? 'text-emerald-700'
                  : baseline.deltaFromBaseline > 0
                  ? 'text-amber-700'
                  : 'text-slate-700'
              }`}
            >
              {baseline.observationCount >= 2
                ? `${baseline.deltaFromBaseline > 0 ? '+' : ''}${baseline.deltaFromBaseline} ${def.unit}`
                : '—'}
            </span>
            <span className="text-[10px] text-slate-400 block mt-0.5">
              {baseline.trend === 'improving'
                ? 'Favorable shift'
                : baseline.trend === 'elevated'
                ? 'Elevated shift'
                : 'Stable baseline'}
            </span>
          </div>

          <div className="p-3 bg-slate-50 rounded border border-slate-200/70">
            <span className="text-[11px] text-slate-400 block mb-0.5">Observed Range</span>
            <span className="text-base font-bold font-mono text-slate-900 tabular-nums">
              {baseline.observationCount > 0
                ? `${baseline.minObserved} – ${baseline.maxObserved}`
                : '—'}
            </span>
            <span className="text-[10px] text-slate-400 block mt-0.5">Min to Max</span>
          </div>

          <div className="p-3 bg-slate-50 rounded border border-slate-200/70">
            <span className="text-[11px] text-slate-400 block mb-0.5">Sample Density</span>
            <span className="text-base font-bold font-mono text-slate-900 tabular-nums">
              {baseline.observationCount} records
            </span>
            <span className="text-[10px] text-slate-400 block mt-0.5">
              {baseline.observationCount >= 4 ? 'High Confidence' : 'Sparse Baseline'}
            </span>
          </div>
        </div>

        {/* Insufficient History Explanatory Alert */}
        {!hasSufficientHistory && (
          <div className="mb-4 p-3.5 bg-amber-50/70 border border-amber-200 rounded text-xs text-amber-900 flex items-start gap-3">
            <AlertCircle className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
            <div>
              <strong className="font-semibold block mb-0.5">
                Sparse Observation Window ({metricObservations.length} of 3 minimum measurements)
              </strong>
              <span>
                Personal baseline calculation and clinical standard deviations require at least 3 longitudinal observations spaced across multiple intake periods. Current values reflect exploratory provisional markers.
              </span>
            </div>
          </div>
        )}

        {/* Interactive Chart */}
        <div className="py-2">
          <InteractiveTrendChart
            observations={observations.filter((o) => o.patientId === patient.id)}
            metricKey={selectedMetric}
            baseline={baseline}
            timeRange={timeRange}
            height={300}
            showBaselineBand={true}
            showClinicalReference={true}
          />
        </div>
      </div>

      {/* Historical Observations Table for Selected Metric */}
      <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs">
        <div className="flex items-center justify-between mb-4 pb-2 border-b border-slate-100">
          <div>
            <h3 className="text-sm font-semibold text-slate-900">
              Chronological Observation Ledger: {def.label}
            </h3>
            <p className="text-xs text-slate-500">
              Complete audit trail of all recorded values for {patient.id}.
            </p>
          </div>

          <button
            onClick={() => setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc')}
            className="flex items-center gap-1.5 text-xs text-slate-600 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 px-2.5 py-1.5 rounded border border-slate-200 transition-colors"
          >
            <ArrowUpDown className="w-3.5 h-3.5" />
            <span>Sort Date: {sortOrder === 'desc' ? 'Newest First' : 'Oldest First'}</span>
          </button>
        </div>

        {metricObservations.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500 font-medium bg-slate-50/70">
                  <th className="py-2.5 px-3">Date</th>
                  <th className="py-2.5 px-3 text-right">Value ({def.unit})</th>
                  <th className="py-2.5 px-3 text-right">vs Personal Baseline</th>
                  <th className="py-2.5 px-3">Clinical Evaluation</th>
                  <th className="py-2.5 px-3">Context / Device Notes</th>
                  <th className="py-2.5 px-3">Provenance</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {metricObservations.map((obs) => {
                  const deltaFromBase = baseline.observationCount >= 2 ? obs.value - baseline.mean : 0;
                  const isOptimal = obs.value <= def.normalMax && obs.value >= def.normalMin;

                  return (
                    <tr key={obs.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-2.5 px-3 font-mono font-medium text-slate-800 whitespace-nowrap">
                        {obs.recordedAt}
                      </td>
                      <td className="py-2.5 px-3 text-right font-mono font-semibold text-slate-900 tabular-nums">
                        {obs.value}
                      </td>
                      <td className="py-2.5 px-3 text-right font-mono tabular-nums">
                        {baseline.observationCount >= 2 ? (
                          <span
                            className={
                              deltaFromBase < 0
                                ? 'text-emerald-700'
                                : deltaFromBase > 0
                                ? 'text-amber-700'
                                : 'text-slate-400'
                            }
                          >
                            {deltaFromBase > 0 ? '+' : ''}
                            {deltaFromBase.toFixed(1)} {def.unit}
                          </span>
                        ) : (
                          <span className="text-slate-400">—</span>
                        )}
                      </td>
                      <td className="py-2.5 px-3">
                        <span
                          className={`font-medium ${
                            isOptimal
                              ? 'text-emerald-700'
                              : obs.value > def.normalMax * 1.15
                              ? 'text-rose-700'
                              : 'text-amber-700'
                          }`}
                        >
                          {isOptimal ? 'Optimal' : obs.value > def.normalMax ? 'Elevated' : 'Below Target'}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-slate-500 max-w-sm truncate">
                        {obs.contextNotes || 'Routine calibration'}
                      </td>
                      <td className="py-2.5 px-3 text-[11px] text-slate-400 font-mono">
                        Synthetic Demo
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center text-slate-400 text-xs">
            No observations recorded for {def.label} yet.
          </div>
        )}
      </div>
    </div>
  );
};
