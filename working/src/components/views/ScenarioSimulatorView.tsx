import React, { useState, useMemo } from 'react';
import {
  PatientProfile,
  Observation,
  ScenarioAdjustments
} from '../../types/health';
import {
  runScenarioSimulation,
  calculateMetricBaseline,
  METRIC_DEFINITIONS
} from '../../data/mockData';
import {
  Sliders,
  RotateCcw,
  TrendingDown,
  Info,
  ShieldCheck,
  BookOpen,
  ArrowRight,
  CheckCircle2,
  Sparkles,
  HeartPulse
} from 'lucide-react';

interface ScenarioSimulatorViewProps {
  patient: PatientProfile;
  observations: Observation[];
}

export const ScenarioSimulatorView: React.FC<ScenarioSimulatorViewProps> = ({
  patient,
  observations
}) => {
  // Scenario state
  const defaultAdjustments: ScenarioAdjustments = {
    physicalActivityMinutesPerDay: 30,
    sodiumReductionMg: 1000,
    sleepHours: 7.5,
    weightReductionKg: 3,
    dietaryGlycemicIndexShift: 'moderate_reduction'
  };

  const [adjustments, setAdjustments] = useState<ScenarioAdjustments>(defaultAdjustments);
  const [selectedTrajectoryMetric, setSelectedTrajectoryMetric] = useState<
    'systolic_bp' | 'fasting_glucose' | 'resting_heart_rate'
  >('systolic_bp');

  const simulation = useMemo(() => {
    return runScenarioSimulation(patient, observations, adjustments);
  }, [patient, observations, adjustments]);

  const handleReset = () => {
    setAdjustments({
      physicalActivityMinutesPerDay: 0,
      sodiumReductionMg: 0,
      sleepHours: 6.5,
      weightReductionKg: 0,
      dietaryGlycemicIndexShift: 'none'
    });
  };

  const handleApplyPreset = (preset: 'cardio' | 'metabolic' | 'optimal') => {
    if (preset === 'cardio') {
      setAdjustments({
        physicalActivityMinutesPerDay: 45,
        sodiumReductionMg: 1500,
        sleepHours: 7.5,
        weightReductionKg: 2,
        dietaryGlycemicIndexShift: 'none'
      });
    } else if (preset === 'metabolic') {
      setAdjustments({
        physicalActivityMinutesPerDay: 40,
        sodiumReductionMg: 800,
        sleepHours: 7.5,
        weightReductionKg: 5,
        dietaryGlycemicIndexShift: 'strict_low_gi'
      });
    } else {
      setAdjustments({
        physicalActivityMinutesPerDay: 60,
        sodiumReductionMg: 1200,
        sleepHours: 8.0,
        weightReductionKg: 4,
        dietaryGlycemicIndexShift: 'moderate_reduction'
      });
    }
  };

  // Trajectory visualization helper
  const targetMetricProj = simulation.projectedMetrics.find(
    (m) => m.metricKey === selectedTrajectoryMetric
  );
  const def = METRIC_DEFINITIONS[selectedTrajectoryMetric];

  return (
    <div className="space-y-6">
      {/* Disclaimer Kicker */}
      <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 text-xs text-slate-700 flex items-start gap-3 shadow-2xs">
        <Info className="w-4 h-4 text-teal-800 shrink-0 mt-0.5" />
        <div>
          <strong className="font-semibold text-slate-900 block mb-0.5">
            Hypothetical Twin Projection — Research Sandbox
          </strong>
          <span>
            Simulated outcomes are mathematical directional estimates based on clinical trial meta-analyses (DASH, Diabetes Prevention Program, and Look AHEAD). These are hypothetical projections for lifestyle planning, <strong>not guaranteed clinical outcomes or diagnostic prescriptions</strong>.
          </span>
        </div>
      </div>

      {/* Main Grid: Adjustment Controls (Left) & Projected Results (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Controls Column (5 cols on lg) */}
        <div className="lg:col-span-5 bg-white rounded-lg border border-slate-200 p-5 shadow-2xs space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-semibold text-slate-900 flex items-center gap-2">
                <Sliders className="w-4 h-4 text-teal-800" />
                <span>Intervention Controls</span>
              </h3>
              <p className="text-[11px] text-slate-500">
                Adjust variables to test personal baseline response
              </p>
            </div>
            <button
              onClick={handleReset}
              className="text-xs text-slate-500 hover:text-slate-900 flex items-center gap-1 transition-colors"
            >
              <RotateCcw className="w-3 h-3" />
              <span>Reset</span>
            </button>
          </div>

          {/* Quick Intervention Presets */}
          <div>
            <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider block mb-2">
              Clinical Protocol Presets
            </span>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => handleApplyPreset('cardio')}
                className="p-2 text-left rounded border border-slate-200 bg-slate-50 hover:bg-slate-100 transition-colors"
              >
                <div className="text-[11px] font-semibold text-slate-900">DASH Cardio</div>
                <div className="text-[10px] text-slate-500">Low sodium + 45m</div>
              </button>
              <button
                onClick={() => handleApplyPreset('metabolic')}
                className="p-2 text-left rounded border border-slate-200 bg-slate-50 hover:bg-slate-100 transition-colors"
              >
                <div className="text-[11px] font-semibold text-slate-900">DPP Glycemic</div>
                <div className="text-[10px] text-slate-500">Low GI + -5kg</div>
              </button>
              <button
                onClick={() => handleApplyPreset('optimal')}
                className="p-2 text-left rounded border border-slate-200 bg-slate-50 hover:bg-slate-100 transition-colors"
              >
                <div className="text-[11px] font-semibold text-slate-900">Balanced</div>
                <div className="text-[10px] text-slate-500">Comprehensive</div>
              </button>
            </div>
          </div>

          {/* Sliders */}
          <div className="space-y-4 pt-2">
            {/* Aerobic Activity */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <label className="font-medium text-slate-700">
                  Daily Moderate-to-Vigorous Activity
                </label>
                <span className="font-mono font-bold text-teal-800">
                  +{adjustments.physicalActivityMinutesPerDay} min/day
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="90"
                step="5"
                value={adjustments.physicalActivityMinutesPerDay}
                onChange={(e) =>
                  setAdjustments({
                    ...adjustments,
                    physicalActivityMinutesPerDay: parseInt(e.target.value)
                  })
                }
                className="w-full accent-teal-800 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
                <span>0 min</span>
                <span>30 min (AHA baseline)</span>
                <span>90 min</span>
              </div>
            </div>

            {/* Sodium Reduction */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <label className="font-medium text-slate-700">
                  Dietary Sodium Reduction
                </label>
                <span className="font-mono font-bold text-teal-800">
                  -{adjustments.sodiumReductionMg} mg/day
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="2000"
                step="100"
                value={adjustments.sodiumReductionMg}
                onChange={(e) =>
                  setAdjustments({
                    ...adjustments,
                    sodiumReductionMg: parseInt(e.target.value)
                  })
                }
                className="w-full accent-teal-800 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
                <span>0 mg (No change)</span>
                <span>-1,000 mg (DASH level)</span>
                <span>-2,000 mg</span>
              </div>
            </div>

            {/* Sleep Target */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <label className="font-medium text-slate-700">
                  Nightly Sleep Duration Target
                </label>
                <span className="font-mono font-bold text-teal-800">
                  {adjustments.sleepHours} hours
                </span>
              </div>
              <input
                type="range"
                min="5.0"
                max="9.0"
                step="0.5"
                value={adjustments.sleepHours}
                onChange={(e) =>
                  setAdjustments({
                    ...adjustments,
                    sleepHours: parseFloat(e.target.value)
                  })
                }
                className="w-full accent-teal-800 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
                <span>5.0 hrs (Deficit)</span>
                <span>7.5 hrs (Restorative)</span>
                <span>9.0 hrs</span>
              </div>
            </div>

            {/* Weight Reduction */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <label className="font-medium text-slate-700">
                  Target Intentional Weight Change
                </label>
                <span className="font-mono font-bold text-teal-800">
                  -{adjustments.weightReductionKg} kg
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.5"
                value={adjustments.weightReductionKg}
                onChange={(e) =>
                  setAdjustments({
                    ...adjustments,
                    weightReductionKg: parseFloat(e.target.value)
                  })
                }
                className="w-full accent-teal-800 cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
                <span>0 kg</span>
                <span>-5 kg (~5% bodyweight)</span>
                <span>-10 kg</span>
              </div>
            </div>

            {/* Dietary Glycemic Index Shift */}
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                Nutritional Pattern Modality
              </label>
              <select
                value={adjustments.dietaryGlycemicIndexShift}
                onChange={(e) =>
                  setAdjustments({
                    ...adjustments,
                    dietaryGlycemicIndexShift: e.target.value as any
                  })
                }
                className="w-full px-3 py-2 text-xs bg-white border border-slate-200 rounded text-slate-800 focus:outline-none focus:ring-1 focus:ring-teal-700"
              >
                <option value="none">Standard Unrestricted Diet</option>
                <option value="moderate_reduction">Moderate Low-Glycemic Whole-Food Shift</option>
                <option value="strict_low_gi">Strict Low-GI / Mediterranean Pattern</option>
              </select>
            </div>
          </div>
        </div>

        {/* Results & Trajectory Column (7 cols on lg) */}
        <div className="lg:col-span-7 space-y-5">
          {/* Side-by-Side Current Baseline vs Simulated Comparison */}
          <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs">
            <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
              <div>
                <h3 className="text-sm font-semibold text-slate-900">
                  Current Baseline vs. Simulated Projection
                </h3>
                <p className="text-xs text-slate-500">
                  Estimated 12-week stabilized equilibrium for {patient.id}
                </p>
              </div>
              <span className="text-[11px] font-mono text-teal-800 font-medium">
                Twin Model v26.1
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {simulation.projectedMetrics.map((proj) => {
                const metricDef = METRIC_DEFINITIONS[proj.metricKey];
                return (
                  <div
                    key={proj.metricKey}
                    onClick={() =>
                      setSelectedTrajectoryMetric(
                        proj.metricKey as 'systolic_bp' | 'fasting_glucose' | 'resting_heart_rate'
                      )
                    }
                    className={`p-3.5 rounded border transition-all cursor-pointer ${
                      selectedTrajectoryMetric === proj.metricKey
                        ? 'bg-teal-50/50 border-teal-700 ring-1 ring-teal-700'
                        : 'bg-slate-50 border-slate-200/80 hover:bg-slate-100/60'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                      <span className="font-medium text-slate-800">
                        {metricDef.shortLabel}
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono">
                        Target {metricDef.optimalTarget}
                      </span>
                    </div>

                    <div className="flex items-baseline justify-between mt-1">
                      <div className="text-xs text-slate-500 font-mono">
                        Baseline:{' '}
                        <span className="font-semibold text-slate-700">
                          {proj.baselineValue} {proj.unit}
                        </span>
                      </div>
                      <div className="text-right">
                        <span className="text-lg font-bold font-mono text-teal-900 tabular-nums">
                          {proj.simulatedValue}{' '}
                          <span className="text-xs font-normal text-slate-500">
                            {proj.unit}
                          </span>
                        </span>
                      </div>
                    </div>

                    {/* Delta highlight */}
                    <div className="mt-2 pt-1.5 border-t border-slate-200/60 flex items-center justify-between text-[11px]">
                      <span className="text-slate-500">Projected Shift:</span>
                      <span
                        className={`font-mono font-semibold tabular-nums ${
                          proj.absoluteDelta <= 0
                            ? 'text-emerald-700'
                            : 'text-amber-700'
                        }`}
                      >
                        {proj.absoluteDelta > 0 ? '+' : ''}
                        {proj.absoluteDelta} {proj.unit} ({proj.percentDelta}%)
                      </span>
                    </div>

                    <p className="text-[10px] text-slate-500 mt-1 line-clamp-1">
                      {proj.clinicalSignificance}
                    </p>
                  </div>
                );
              })}
            </div>

            {/* Projected Risk Score Reductions */}
            <div className="mt-4 pt-4 border-t border-slate-100">
              <span className="text-[11px] font-semibold text-slate-700 uppercase tracking-wider block mb-2">
                Projected Screening Risk Shifts
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {simulation.projectedRiskChanges.map((rc, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-emerald-50/60 border border-emerald-200/80 rounded text-xs"
                  >
                    <div className="font-medium text-emerald-950 mb-1">
                      {rc.assessmentType}
                    </div>
                    <div className="flex items-baseline justify-between">
                      <span className="text-slate-600 font-mono text-[11px]">
                        {rc.baselineScore}% → <strong className="text-emerald-900">{rc.projectedScore}%</strong>
                      </span>
                      <span className="text-emerald-800 font-bold font-mono">
                        -{rc.percentReduction}% Relative
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 12-Week Trajectory Simulation Curve */}
          <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs">
            <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-100">
              <div>
                <h4 className="text-xs font-semibold text-slate-900">
                  Hypothetical 12-Week Trajectory: {def.label}
                </h4>
                <p className="text-[11px] text-slate-500">
                  Simulated adaptation timeline assuming sustained intervention compliance
                </p>
              </div>
              <div className="text-right">
                <span className="text-xs font-mono font-semibold text-teal-800">
                  {targetMetricProj?.simulatedValue} {def.unit} at Week 12
                </span>
              </div>
            </div>

            {/* Visual SVG Trajectory Curve */}
            <div className="py-2">
              <svg viewBox="0 0 600 160" className="w-full h-auto">
                {/* Reference line */}
                <line
                  x1="40"
                  y1="120"
                  x2="560"
                  y2="120"
                  stroke="#cbd5e1"
                  strokeWidth="1"
                  strokeDasharray="2 2"
                />
                <text x="35" y="123" textAnchor="end" className="text-[10px] fill-slate-400 font-mono">
                  {targetMetricProj?.simulatedValue}
                </text>

                {/* Baseline reference */}
                <line
                  x1="40"
                  y1="40"
                  x2="560"
                  y2="40"
                  stroke="#94a3b8"
                  strokeWidth="1"
                  strokeDasharray="3 3"
                />
                <text x="35" y="43" textAnchor="end" className="text-[10px] fill-slate-500 font-mono">
                  {targetMetricProj?.baselineValue}
                </text>

                {/* Trajectory curve from Week 0 to Week 12 */}
                {/* Cubic bezier smoothing out from 40 to 120 */}
                <path
                  d="M 50 40 C 180 45, 260 100, 550 120"
                  fill="none"
                  stroke="#0f766e"
                  strokeWidth="2.5"
                  strokeDasharray="none"
                />

                {/* Week labels */}
                {['Wk 0', 'Wk 2', 'Wk 4', 'Wk 8', 'Wk 12'].map((wk, i) => (
                  <text
                    key={wk}
                    x={50 + (i / 4) * 500}
                    y="145"
                    textAnchor="middle"
                    className="text-[10px] fill-slate-400 font-sans"
                  >
                    {wk}
                  </text>
                ))}

                {/* End point dot */}
                <circle cx="550" cy="120" r="4.5" fill="#042f2e" stroke="#ffffff" strokeWidth="2" />
                {/* Start point dot */}
                <circle cx="50" cy="40" r="4" fill="#64748b" stroke="#ffffff" strokeWidth="2" />
              </svg>
            </div>

            <div className="flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-slate-100">
              <span>Week 0: {targetMetricProj?.baselineValue} {def.unit}</span>
              <span className="text-teal-800 font-medium">
                Stabilizes around Week 6–8 per physiological adaptation latency
              </span>
              <span>Week 12: {targetMetricProj?.simulatedValue} {def.unit}</span>
            </div>
          </div>

          {/* Clinical Evidence Foundations */}
          <div className="bg-white rounded-lg border border-slate-200 p-5 shadow-2xs space-y-3">
            <h4 className="text-xs font-semibold text-slate-900 flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-teal-800" />
              <span>Clinical Evidence & Trial Meta-Analyses Foundations</span>
            </h4>

            <div className="space-y-2 text-xs">
              {simulation.evidenceCitations.map((cite, idx) => (
                <div
                  key={idx}
                  className="p-2.5 bg-slate-50 rounded border border-slate-100"
                >
                  <strong className="text-slate-800 block mb-0.5">
                    {cite.study}
                  </strong>
                  <p className="text-slate-600 leading-relaxed text-[11px]">
                    {cite.finding}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
