/**
 * API Client for Flask Backend Integration
 * Connects React UI to Flask API endpoints
 */

const API_BASE_URL = '/api/react';

export interface PatientProfile {
  id: string;
  birthYear: number;
  sexAtBirth: 'Female' | 'Male';
  monitoringStatus: string;
  primaryFocus: string;
  enrolledDate: string;
  baselineWindowDays: number;
  smokerStatus: string;
  notes: string;
}

export interface Observation {
  id: string;
  patientId: string;
  recordedAt: string;
  metricKey: string;
  value: number;
  unit: string;
  category: string;
  contextNotes?: string;
  isSynthetic: boolean;
}

export interface RiskAssessment {
  id: string;
  patientId: string;
  assessmentType: string;
  title: string;
  category: string;
  scorePercent: number;
  classification: string;
  methodologyDescription: string;
  contributingFactors: Array<{
    factor: string;
    contributionPercent: number;
    observedValue: string;
    baselineComparison: string;
    impactLevel: string;
  }>;
  missingInputs: string[];
  dataCompletenessPercent: number;
  clinicalDisclaimer: string;
}

export interface MetricDefinition {
  key: string;
  label: string;
  shortLabel: string;
  unit: string;
  category: string;
  normalMin: number;
  normalMax: number;
  optimalTarget: string;
  decimals: number;
  description: string;
  clinicalRelevance: string;
}

class APIClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async getPatients(): Promise<PatientProfile[]> {
    return this.fetch<PatientProfile[]>('/patients');
  }

  async getObservations(patientId: string): Promise<Observation[]> {
    return this.fetch<Observation[]>(`/patients/${patientId}/observations`);
  }

  async getRiskAssessment(patientId: string): Promise<RiskAssessment[]> {
    return this.fetch<RiskAssessment[]>(`/patients/${patientId}/risk`);
  }

  async getMetricDefinitions(): Promise<Record<string, MetricDefinition>> {
    return this.fetch<Record<string, MetricDefinition>>('/metrics');
  }

  async initializeDemo(): Promise<{
    message: string;
    patients: PatientProfile[];
    created: boolean;
  }> {
    return this.fetch('/demo/initialize', {
      method: 'POST',
    });
  }

  async createObservation(patientId: string, observation: Partial<Observation>): Promise<Observation> {
    return this.fetch<Observation>(`/patients/${patientId}/observations`, {
      method: 'POST',
      body: JSON.stringify(observation),
    });
  }

  async createScenario(patientId: string, scenarioData: {
    scenarioName?: string;
    description?: string;
    adjustments?: {
      physicalActivityMinutesPerDay: number;
      sodiumReductionMg: number;
      sleepHours: number;
      weightReductionKg: number;
      dietaryGlycemicIndexShift: string;
    };
  }): Promise<any> {
    return this.fetch(`/patients/${patientId}/scenarios`, {
      method: 'POST',
      body: JSON.stringify(scenarioData),
    });
  }

  async exportPatientData(patientId: string, format: string = 'csv'): Promise<Blob> {
    const url = `${this.baseUrl}/patients/${patientId}/export?format=${format}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    return response.blob();
  }

  async importCSV(patientId: string, file: File): Promise<{
    message: string;
    created: number;
    observations: Observation[];
  }> {
    const formData = new FormData();
    formData.append('file', file);

    const url = `${this.baseUrl}/patients/${patientId}/import/csv`;
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || `API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }
}

export const apiClient = new APIClient();
