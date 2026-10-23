import React, { useState, useEffect } from 'react';
import {
  PatientProfile,
  Observation
} from './types/health';
import { Sidebar, NavTabId } from './components/layout/Sidebar';
import { TopBar } from './components/layout/TopBar';
import { OverviewDashboard } from './components/views/OverviewDashboard';
import { PatientProfilesView } from './components/views/PatientProfilesView';
import { HealthTrendsView } from './components/views/HealthTrendsView';
import { RiskInsightsView } from './components/views/RiskInsightsView';
import { ScenarioSimulatorView } from './components/views/ScenarioSimulatorView';
import { ObservationsLogView } from './components/views/ObservationsLogView';
import { DataImportExportView } from './components/views/DataImportExportView';
import { EvidenceReportsView } from './components/views/EvidenceReportsView';
import { ProjectInfoFlaskGuide } from './components/views/ProjectInfoFlaskGuide';
import { RecordObservationModal } from './components/modals/RecordObservationModal';
import { apiClient, PatientProfile as APIPatient, Observation as APIObservation } from './api/client';

export default function App() {
  const [currentTab, setCurrentTab] = useState<NavTabId>('overview');
  const [patients, setPatients] = useState<PatientProfile[]>([]);
  const [activePatientId, setActivePatientId] = useState<string>('');
  const [observations, setObservations] = useState<Observation[]>([]);
  const [isRecordModalOpen, setIsRecordModalOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load data on mount
  useEffect(() => {
    async function loadData() {
      try {
        setIsLoading(true);
        setError(null);

        // Initialize demo if needed
        const demoResponse = await apiClient.initializeDemo();

        // Load patients
        const apiPatients = await apiClient.getPatients();

        // Convert API patients to internal format
        const convertedPatients: PatientProfile[] = apiPatients.map(p => ({
          id: p.id,
          birthYear: p.birthYear,
          sexAtBirth: p.sexAtBirth,
          monitoringStatus: p.monitoringStatus as any,
          primaryFocus: p.primaryFocus,
          enrolledDate: p.enrolledDate,
          baselineWindowDays: p.baselineWindowDays,
          smokerStatus: p.smokerStatus as any,
          notes: p.notes
        }));

        setPatients(convertedPatients);

        // Set active patient
        if (convertedPatients.length > 0) {
          const firstPatientId = convertedPatients[0].id;
          setActivePatientId(firstPatientId);

          // Load observations for active patient
          const apiObservations = await apiClient.getObservations(firstPatientId);

          // Convert API observations to internal format
          const convertedObservations: Observation[] = apiObservations.map(o => ({
            id: o.id,
            patientId: o.patientId,
            recordedAt: o.recordedAt,
            metricKey: o.metricKey as any,
            value: o.value,
            unit: o.unit,
            category: o.category as any,
            contextNotes: o.contextNotes,
            isSynthetic: o.isSynthetic
          }));

          setObservations(convertedObservations);
        }
      } catch (err) {
        console.error('Failed to load data:', err);
        setError('Failed to load data from backend. Please refresh the page.');
      } finally {
        setIsLoading(false);
      }
    }

    loadData();
  }, []);

  // Load observations when active patient changes
  useEffect(() => {
    async function loadPatientObservations() {
      if (!activePatientId) return;

      try {
        const apiObservations = await apiClient.getObservations(activePatientId);

        const convertedObservations: Observation[] = apiObservations.map(o => ({
          id: o.id,
          patientId: o.patientId,
          recordedAt: o.recordedAt,
          metricKey: o.metricKey as any,
          value: o.value,
          unit: o.unit,
          category: o.category as any,
          contextNotes: o.contextNotes,
          isSynthetic: o.isSynthetic
        }));

        setObservations(convertedObservations);
      } catch (err) {
        console.error('Failed to load observations:', err);
      }
    }

    loadPatientObservations();
  }, [activePatientId]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#f7f9f8]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-800 mx-auto mb-4"></div>
          <p className="text-slate-600">Loading Swasthya Twin...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#f7f9f8]">
        <div className="text-center max-w-md p-6 bg-white rounded-lg border border-rose-200 shadow-lg">
          <p className="text-rose-700 font-semibold mb-2">Error Loading Application</p>
          <p className="text-slate-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-teal-800 text-white rounded hover:bg-teal-900"
          >
            Refresh Page
          </button>
        </div>
      </div>
    );
  }

  const activePatient =
    patients.find((p) => p.id === activePatientId) || patients[0];

  const handleAddObservation = (newObs: Observation) => {
    setObservations((prev) => [newObs, ...prev]);
  };

  const handleImportObservations = (imported: Observation[]) => {
    setObservations((prev) => [...imported, ...prev]);
  };

  const handleDeleteObservation = (id: string) => {
    setObservations((prev) => prev.filter((o) => o.id !== id));
  };

  const handleAddPatient = (newPatient: PatientProfile) => {
    setPatients((prev) => [...prev, newPatient]);
    setActivePatientId(newPatient.id);
  };

  return (
    <div className="min-h-screen flex bg-[#f7f9f8] text-[#0f172a] font-sans antialiased">
      {/* Left Application Sidebar */}
      <Sidebar
        currentTab={currentTab}
        onSelectTab={setCurrentTab}
        activePatient={activePatient}
        isOpenMobile={isMobileMenuOpen}
        onCloseMobile={() => setIsMobileMenuOpen(false)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <TopBar
          currentTab={currentTab}
          patients={patients}
          activePatient={activePatient}
          onSelectPatient={setActivePatientId}
          onOpenRecordModal={() => setIsRecordModalOpen(true)}
          onOpenMobileMenu={() => setIsMobileMenuOpen(true)}
        />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          {currentTab === 'overview' && (
            <OverviewDashboard
              patient={activePatient}
              observations={observations}
              onNavigateTab={setCurrentTab}
              onOpenRecordModal={() => setIsRecordModalOpen(true)}
            />
          )}

          {currentTab === 'profiles' && (
            <PatientProfilesView
              patients={patients}
              activePatientId={activePatientId}
              observations={observations}
              onSelectPatient={setActivePatientId}
              onNavigateTab={setCurrentTab}
              onAddPatient={handleAddPatient}
            />
          )}

          {currentTab === 'trends' && (
            <HealthTrendsView
              patient={activePatient}
              observations={observations}
              onOpenRecordModal={() => setIsRecordModalOpen(true)}
            />
          )}

          {currentTab === 'risk' && (
            <RiskInsightsView
              patient={activePatient}
              observations={observations}
              onNavigateTab={setCurrentTab}
            />
          )}

          {currentTab === 'simulator' && (
            <ScenarioSimulatorView
              patient={activePatient}
              observations={observations}
            />
          )}

          {currentTab === 'observations' && (
            <ObservationsLogView
              observations={observations}
              patients={patients}
              activePatientId={activePatientId}
              onOpenRecordModal={() => setIsRecordModalOpen(true)}
              onDeleteObservation={handleDeleteObservation}
            />
          )}

          {currentTab === 'data' && (
            <DataImportExportView
              observations={observations}
              patients={patients}
              activePatientId={activePatientId}
              onImportObservations={handleImportObservations}
            />
          )}

          {currentTab === 'reports' && (
            <EvidenceReportsView
              patient={activePatient}
              observations={observations}
            />
          )}

          {currentTab === 'project' && <ProjectInfoFlaskGuide />}
        </main>
      </div>

      {/* Manual Observation Entry Dialog */}
      <RecordObservationModal
        isOpen={isRecordModalOpen}
        onClose={() => setIsRecordModalOpen(false)}
        onAddObservation={handleAddObservation}
        patients={patients}
        currentPatientId={activePatientId}
      />
    </div>
  );
}
