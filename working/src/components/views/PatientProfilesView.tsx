import React, { useState, useMemo } from 'react';
import { PatientProfile, Observation } from '../../types/health';
import { Search, Plus, UserCheck, ShieldCheck, Calendar, Activity, Check, ChevronRight, X, AlertTriangle } from 'lucide-react';
import { NavTabId } from '../layout/Sidebar';

interface PatientProfilesViewProps {
  patients: PatientProfile[];
  activePatientId: string;
  observations: Observation[];
  onSelectPatient: (patientId: string) => void;
  onNavigateTab: (tab: NavTabId) => void;
  onAddPatient: (newPatient: PatientProfile) => void;
}

export const PatientProfilesView: React.FC<PatientProfilesViewProps> = ({
  patients,
  activePatientId,
  observations,
  onSelectPatient,
  onNavigateTab,
  onAddPatient
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStatusFilter, setSelectedStatusFilter] = useState<string>('all');
  const [inspectingPatientId, setInspectingPatientId] = useState<string>(activePatientId);
  const [showAddModal, setShowAddModal] = useState(false);

  // New patient form state
  const [newId, setNewId] = useState(`DEMO-00${patients.length + 1}`);
  const [newBirthYear, setNewBirthYear] = useState(1982);
  const [newSex, setNewSex] = useState<'Female' | 'Male'>('Female');
  const [newFocus, setNewFocus] = useState('Metabolic Rate & Cardiorespiratory Stability');
  const [newSmoker, setNewSmoker] = useState<'Non-Smoker' | 'Former Smoker' | 'Current Smoker'>('Non-Smoker');
  const [newNotes, setNewNotes] = useState('Enrolled for baseline physiological calibration protocol.');

  // Calculate observation counts and latest observation date per patient
  const patientStats = useMemo(() => {
    const stats: Record<string, { count: number; lastDate: string; firstDate: string }> = {};
    for (const p of patients) {
      const pObs = observations
        .filter((o) => o.patientId === p.id)
        .sort((a, b) => new Date(a.recordedAt).getTime() - new Date(b.recordedAt).getTime());
      stats[p.id] = {
        count: pObs.length,
        firstDate: pObs.length > 0 ? pObs[0].recordedAt : 'N/A',
        lastDate: pObs.length > 0 ? pObs[pObs.length - 1].recordedAt : 'N/A'
      };
    }
    return stats;
  }, [patients, observations]);

  // Filtered patients
  const filteredPatients = useMemo(() => {
    return patients.filter((p) => {
      const matchesSearch =
        p.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.primaryFocus.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.monitoringStatus.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesStatus =
        selectedStatusFilter === 'all' || p.monitoringStatus === selectedStatusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [patients, searchQuery, selectedStatusFilter]);

  const inspectingPatient =
    patients.find((p) => p.id === inspectingPatientId) || patients[0];
  const inspectingStats = patientStats[inspectingPatient?.id || ''] || {
    count: 0,
    firstDate: 'N/A',
    lastDate: 'N/A'
  };

  const handleCreatePatient = (e: React.FormEvent) => {
    e.preventDefault();
    const created: PatientProfile = {
      id: newId.trim().toUpperCase(),
      birthYear: newBirthYear,
      sexAtBirth: newSex,
      monitoringStatus: 'Sparse History',
      primaryFocus: newFocus.trim(),
      enrolledDate: new Date().toISOString().split('T')[0],
      baselineWindowDays: 60,
      smokerStatus: newSmoker,
      notes: newNotes.trim()
    };
    onAddPatient(created);
    setInspectingPatientId(created.id);
    setShowAddModal(false);
  };

  return (
    <div className="space-y-6">
      {/* Top Controls: Search, Status Filter & Add Profile Button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-4 rounded-lg border border-slate-200 shadow-2xs">
        <div className="flex flex-1 items-center gap-3">
          <div className="relative flex-1 max-w-sm">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search by ID, focus, or status..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded text-slate-900 focus:outline-none focus:ring-1 focus:ring-teal-700"
            />
          </div>

          {/* Status filter tabs */}
          <div className="hidden md:flex items-center gap-1 bg-slate-100 p-1 rounded text-xs">
            {['all', 'Baseline Established', 'Active Monitoring', 'Sparse History', 'Post-Intervention'].map((status) => (
              <button
                key={status}
                onClick={() => setSelectedStatusFilter(status)}
                className={`px-2 py-1 rounded transition-colors whitespace-nowrap ${
                  selectedStatusFilter === status
                    ? 'bg-white text-slate-900 shadow-2xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {status === 'all' ? 'All Profiles' : status}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-white bg-teal-800 hover:bg-teal-900 rounded transition-colors shadow-2xs self-start sm:self-auto"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Add Synthetic Profile</span>
        </button>
      </div>

      {/* Main Grid: Patient List & Inspection Drawer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Patient Table (8 cols on lg) */}
        <div className="lg:col-span-7 xl:col-span-8 bg-white rounded-lg border border-slate-200 overflow-hidden shadow-2xs">
          <div className="px-5 py-3 border-b border-slate-100 flex items-center justify-between">
            <h3 className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
              Pseudonymous Digital Twin Directory ({filteredPatients.length})
            </h3>
            <span className="text-[11px] text-slate-400">
              Select a row to inspect or switch active twin
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500 font-medium bg-slate-50/70">
                  <th className="py-2.5 px-4">Twin Identifier</th>
                  <th className="py-2.5 px-4">Primary Clinical Focus</th>
                  <th className="py-2.5 px-4 text-center">Observations</th>
                  <th className="py-2.5 px-4">Latest Observation</th>
                  <th className="py-2.5 px-4">Monitoring Status</th>
                  <th className="py-2.5 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {filteredPatients.map((p) => {
                  const stats = patientStats[p.id] || { count: 0, lastDate: 'N/A' };
                  const isCurrentActive = p.id === activePatientId;
                  const isInspecting = p.id === inspectingPatientId;

                  return (
                    <tr
                      key={p.id}
                      onClick={() => setInspectingPatientId(p.id)}
                      className={`cursor-pointer transition-colors ${
                        isInspecting
                          ? 'bg-teal-50/40'
                          : 'hover:bg-slate-50/80'
                      }`}
                    >
                      <td className="py-3 px-4 font-mono font-semibold text-slate-900 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <span>{p.id}</span>
                          {isCurrentActive && (
                            <span className="text-[10px] text-teal-800 bg-teal-100/70 px-1.5 py-0.5 rounded font-sans font-medium">
                              Active
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-slate-800 font-medium max-w-xs truncate">
                        {p.primaryFocus}
                      </td>
                      <td className="py-3 px-4 text-center font-mono font-semibold text-slate-900 tabular-nums">
                        {stats.count}
                      </td>
                      <td className="py-3 px-4 font-mono text-slate-500 whitespace-nowrap">
                        {stats.lastDate}
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`text-[11px] font-medium ${
                            p.monitoringStatus === 'Baseline Established'
                              ? 'text-emerald-700'
                              : p.monitoringStatus === 'Active Monitoring'
                              ? 'text-teal-700'
                              : p.monitoringStatus === 'Post-Intervention'
                              ? 'text-sky-700'
                              : 'text-amber-700'
                          }`}
                        >
                          {p.monitoringStatus}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right whitespace-nowrap">
                        {isCurrentActive ? (
                          <span className="text-[11px] text-slate-400 font-sans">
                            Currently Loaded
                          </span>
                        ) : (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              onSelectPatient(p.id);
                            }}
                            className="text-xs font-semibold text-teal-800 hover:text-teal-900 hover:underline px-2 py-1 rounded"
                          >
                            Load Twin
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {filteredPatients.length === 0 && (
            <div className="p-8 text-center text-slate-400 text-xs">
              No profiles matching the search query or status filter.
            </div>
          )}
        </div>

        {/* Selected Patient Inspection Panel (4 cols on lg) */}
        {inspectingPatient && (
          <div className="lg:col-span-5 xl:col-span-4 bg-white rounded-lg border border-slate-200 p-5 shadow-2xs space-y-4">
            <div className="flex items-start justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-[10px] text-slate-400 font-mono uppercase tracking-wider">
                  Digital Twin Inspector
                </span>
                <h3 className="text-lg font-bold font-mono text-slate-900">
                  {inspectingPatient.id}
                </h3>
              </div>
              {inspectingPatient.id === activePatientId ? (
                <span className="text-xs font-semibold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded">
                  Active in Session
                </span>
              ) : (
                <button
                  onClick={() => onSelectPatient(inspectingPatient.id)}
                  className="text-xs font-semibold text-white bg-teal-800 hover:bg-teal-900 px-3 py-1.5 rounded transition-colors shadow-2xs"
                >
                  Switch to this Twin
                </button>
              )}
            </div>

            {/* Physiological & Enrollment Specifications */}
            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Clinical Focus:</span>
                <span className="font-medium text-slate-800 text-right max-w-[200px]">
                  {inspectingPatient.primaryFocus}
                </span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Demographics:</span>
                <span className="font-medium text-slate-800">
                  {2026 - inspectingPatient.birthYear} years old · {inspectingPatient.sexAtBirth}
                </span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Enrollment Date:</span>
                <span className="font-mono text-slate-700">
                  {inspectingPatient.enrolledDate}
                </span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Total Observations:</span>
                <span className="font-mono font-semibold text-slate-900">
                  {inspectingStats.count} records
                </span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Baseline Window:</span>
                <span className="font-medium text-slate-800">
                  {inspectingPatient.baselineWindowDays} days calibration
                </span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Tobacco Risk Profile:</span>
                <span className="font-medium text-slate-800">
                  {inspectingPatient.smokerStatus}
                </span>
              </div>
            </div>

            {/* Clinical & Twin Notes */}
            <div className="p-3 bg-slate-50 rounded border border-slate-100 text-xs text-slate-600">
              <span className="font-semibold text-slate-700 block mb-1">
                Clinical Context & Baseline Protocol:
              </span>
              <p className="leading-relaxed">{inspectingPatient.notes}</p>
            </div>

            {inspectingStats.count < 10 && (
              <div className="flex items-start gap-2 p-3 bg-amber-50 border border-amber-200 rounded text-xs text-amber-800">
                <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <span>
                  Sparse baseline warning: Profile has only {inspectingStats.count} recorded observations. Statistical baselines and risk evaluations use imputed parameters.
                </span>
              </div>
            )}

            {/* Quick Actions for this Patient */}
            <div className="pt-2 flex flex-col gap-2">
              <button
                onClick={() => {
                  onSelectPatient(inspectingPatient.id);
                  onNavigateTab('trends');
                }}
                className="w-full text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 py-2 rounded transition-colors text-center"
              >
                Analyze Health Trends
              </button>
              <button
                onClick={() => {
                  onSelectPatient(inspectingPatient.id);
                  onNavigateTab('simulator');
                }}
                className="w-full text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 py-2 rounded transition-colors text-center"
              >
                Run What-If Scenario
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Add Synthetic Patient Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4">
          <div className="bg-white rounded-lg border border-slate-200 shadow-xl max-w-md w-full overflow-hidden">
            <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100">
              <h3 className="text-sm font-semibold text-slate-900">
                Add Synthetic Digital Twin Profile
              </h3>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreatePatient} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Pseudonymous Identifier (e.g. DEMO-005)
                </label>
                <input
                  type="text"
                  required
                  value={newId}
                  onChange={(e) => setNewId(e.target.value)}
                  className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded font-mono"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">
                    Birth Year
                  </label>
                  <input
                    type="number"
                    min="1940"
                    max="2010"
                    value={newBirthYear}
                    onChange={(e) => setNewBirthYear(parseInt(e.target.value) || 1980)}
                    className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded font-mono"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">
                    Sex at Birth
                  </label>
                  <select
                    value={newSex}
                    onChange={(e) => setNewSex(e.target.value as 'Female' | 'Male')}
                    className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded"
                  >
                    <option value="Female">Female</option>
                    <option value="Male">Male</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Primary Clinical Monitoring Focus
                </label>
                <input
                  type="text"
                  required
                  value={newFocus}
                  onChange={(e) => setNewFocus(e.target.value)}
                  className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Tobacco Status
                </label>
                <select
                  value={newSmoker}
                  onChange={(e) =>
                    setNewSmoker(
                      e.target.value as 'Non-Smoker' | 'Former Smoker' | 'Current Smoker'
                    )
                  }
                  className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded"
                >
                  <option value="Non-Smoker">Non-Smoker</option>
                  <option value="Former Smoker">Former Smoker</option>
                  <option value="Current Smoker">Current Smoker</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">
                  Baseline Notes
                </label>
                <textarea
                  rows={2}
                  value={newNotes}
                  onChange={(e) => setNewNotes(e.target.value)}
                  className="w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-xs font-medium text-white bg-teal-800 hover:bg-teal-900 rounded"
                >
                  Create Twin Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
