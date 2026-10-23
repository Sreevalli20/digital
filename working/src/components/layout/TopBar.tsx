import React from 'react';
import { Menu, Plus, UserCheck, ShieldCheck } from 'lucide-react';
import { PatientProfile } from '../../types/health';
import { NavTabId } from './Sidebar';

interface TopBarProps {
  currentTab: NavTabId;
  patients: PatientProfile[];
  activePatient: PatientProfile;
  onSelectPatient: (patientId: string) => void;
  onOpenRecordModal: () => void;
  onOpenMobileMenu: () => void;
}

export const TopBar: React.FC<TopBarProps> = ({
  currentTab,
  patients,
  activePatient,
  onSelectPatient,
  onOpenRecordModal,
  onOpenMobileMenu
}) => {
  const getTabTitle = (tab: NavTabId): string => {
    switch (tab) {
      case 'overview':
        return 'Overview Dashboard';
      case 'profiles':
        return 'Patient Profiles';
      case 'trends':
        return 'Health Trends & Analytics';
      case 'risk':
        return 'Risk Screening Insights';
      case 'simulator':
        return 'What-If Scenario Simulator';
      case 'observations':
        return 'Observations Log';
      case 'data':
        return 'Data Import & Export';
      case 'reports':
        return 'Evidence & Reports';
      case 'project':
        return 'Project Architecture & Flask Guide';
      default:
        return 'Dashboard';
    }
  };

  return (
    <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-xs border-b border-slate-200 px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
      {/* Left: Mobile trigger & Breadcrumbs */}
      <div className="flex items-center gap-3 min-w-0">
        <button
          onClick={onOpenMobileMenu}
          className="md:hidden p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded"
          aria-label="Open navigation menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="min-w-0">
          <nav className="flex items-center gap-1.5 text-xs text-slate-500 font-sans">
            <span className="font-medium text-slate-700">Swasthya Twin</span>
            <span className="text-slate-300">/</span>
            <span className="truncate">{getTabTitle(currentTab)}</span>
            <span className="text-slate-300 hidden sm:inline">/</span>
            <span className="text-slate-700 font-mono hidden sm:inline">{activePatient.id}</span>
          </nav>
          <h2 className="text-sm font-semibold text-slate-900 truncate tracking-tight">
            {getTabTitle(currentTab)}
          </h2>
        </div>
      </div>

      {/* Right: Patient Selector, Synthetic Demo Badge & Action Button */}
      <div className="flex items-center gap-3 shrink-0">
        {/* Synthetic Demo indicator (Clean, unboxed, transparent disclosure) */}
        <div className="hidden lg:flex items-center gap-2 text-xs text-slate-500 border border-emerald-200/80 bg-emerald-50/50 px-2.5 py-1 rounded">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-700 shrink-0" />
          <span className="text-emerald-900 font-medium">Synthetic Demo Dataset</span>
          <span className="text-emerald-600/70">·</span>
          <span className="text-emerald-800">No External AI / Backend Dependency</span>
        </div>

        {/* Patient Switcher */}
        <div className="relative">
          <select
            value={activePatient.id}
            onChange={(e) => onSelectPatient(e.target.value)}
            className="text-xs font-medium bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded px-2.5 py-1.5 text-slate-800 focus:outline-none focus:ring-1 focus:ring-teal-700 cursor-pointer font-mono"
            aria-label="Select active patient digital twin"
          >
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.id} ({p.monitoringStatus})
              </option>
            ))}
          </select>
        </div>

        {/* Primary Page Action Button */}
        <button
          onClick={onOpenRecordModal}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-teal-800 hover:bg-teal-900 rounded transition-colors shadow-xs"
        >
          <Plus className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Record Observation</span>
          <span className="sm:hidden">Add</span>
        </button>
      </div>
    </header>
  );
};
