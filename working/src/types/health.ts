export type MetricCategory = 'cardiovascular' | 'metabolic' | 'anthropometric' | 'telemetry';

export type MetricKey =
  | 'systolic_bp'
  | 'diastolic_bp'
  | 'fasting_glucose'
  | 'hba1c'
  | 'resting_heart_rate'
  | 'ldl_cholesterol'
  | 'hdl_cholesterol'
  | 'total_cholesterol'
  | 'bmi'
  | 'egfr';

export interface MetricDefinition {
  key: MetricKey;
  label: string;
  shortLabel: string;
  unit: string;
  category: MetricCategory;
  normalMin: number;
  normalMax: number;
  optimalTarget: string;
  decimals: number;
  description: string;
  clinicalRelevance: string;
}

export interface Observation {
  id: string;
  patientId: string;
  recordedAt: string; // ISO date string YYYY-MM-DD
  metricKey: MetricKey;
  value: number;
  unit: string;
  category: MetricCategory;
  contextNotes?: string;
  isSynthetic: boolean;
}

export interface PatientProfile {
  id: string; // e.g. 'DEMO-001'
  birthYear: number;
  sexAtBirth: 'Female' | 'Male';
  monitoringStatus: 'Active Monitoring' | 'Baseline Established' | 'Sparse History' | 'Post-Intervention';
  primaryFocus: string;
  enrolledDate: string;
  baselineWindowDays: number;
  smokerStatus: 'Non-Smoker' | 'Former Smoker' | 'Current Smoker';
  notes: string;
}

export interface MetricBaseline {
  metricKey: MetricKey;
  mean: number;
  standardDeviation: number;
  observationCount: number;
  minObserved: number;
  maxObserved: number;
  latestValue: number;
  latestDate: string;
  deltaFromBaseline: number;
  trend: 'improving' | 'stable' | 'elevated' | 'insufficient_data';
  statusLabel: 'Optimal' | 'Normal' | 'Borderline' | 'Elevated' | 'High Risk';
}

export interface ContributingFactor {
  factor: string;
  contributionPercent: number; // 0 to 100
  observedValue: string;
  baselineComparison: string;
  impactLevel: 'low' | 'moderate' | 'high';
}

export interface RiskAssessment {
  id: string;
  patientId: string;
  assessmentType: 'cardiovascular_10yr' | 'diabetes_progression' | 'metabolic_burden';
  title: string;
  category: 'Cardiovascular' | 'Metabolic' | 'Multisystem';
  scorePercent: number; // e.g., 14.8%
  classification: 'Low Risk' | 'Borderline' | 'Elevated' | 'High Risk';
  methodologyDescription: string;
  contributingFactors: ContributingFactor[];
  missingInputs: string[];
  dataCompletenessPercent: number;
  clinicalDisclaimer: string;
}

export interface ScenarioAdjustments {
  physicalActivityMinutesPerDay: number; // baseline 0-120
  sodiumReductionMg: number; // 0 to 2000
  sleepHours: number; // 5 to 9
  weightReductionKg: number; // 0 to 10
  dietaryGlycemicIndexShift: 'none' | 'moderate_reduction' | 'strict_low_gi';
}

export interface ScenarioSimulationResult {
  scenarioName: string;
  patientId: string;
  projectedMetrics: {
    metricKey: MetricKey;
    baselineValue: number;
    simulatedValue: number;
    absoluteDelta: number;
    percentDelta: number;
    unit: string;
    clinicalSignificance: string;
  }[];
  projectedRiskChanges: {
    assessmentType: string;
    baselineScore: number;
    projectedScore: number;
    percentReduction: number;
  }[];
  evidenceCitations: {
    study: string;
    finding: string;
  }[];
}
