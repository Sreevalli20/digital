import React from 'react';
import {
  LayoutDashboard,
  Users,
  TrendingUp,
  ShieldAlert,
  Sliders,
  ClipboardList,
  Database,
  FileText,
  Info,
  Activity,
  HeartPulse
} from 'lucide-react';
import { PatientProfile } from '../../types/health';

export type NavTabId =
  | 'overview'
  | 'profiles'
  | 'trends'
  | 'risk'
  | 'simulator'
  | 'observations'
  | 'data'
  | 'reports';

interface SidebarProps {
  currentTab: NavTabId;
  onSelectTab: (tab: NavTabId) => void;
  activePatient: PatientProfile;
  isOpenMobile: boolean;
  onCloseMobile: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onSelectTab,
  activePatient,
  isOpenMobile,
  onCloseMobile
}) => {
  const navItems = [
    { id: 'overview' as NavTabId, label: 'Overview', icon: LayoutDashboard },
    { id: 'profiles' as NavTabId, label: 'Patient Profiles', icon: Users },
    { id: 'trends' as NavTabId, label: 'Health Trends', icon: TrendingUp },
    { id: 'risk' as NavTabId, label: 'Risk Insights', icon: ShieldAlert },
    { id: 'simulator' as NavTabId, label: 'Scenario Simulator', icon: Sliders },
    { id: 'observations' as NavTabId, label: 'Observations Log', icon: ClipboardList },
    { id: 'data' as NavTabId, label: 'Data Import & Export', icon: Database },
    { id: 'reports' as NavTabId, label: 'Evidence & Reports', icon: FileText }
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpenMobile && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/50 md:hidden"
          onClick={onCloseMobile}
          aria-hidden="true"
        />
      )}

      {/* Main Sidebar Shell */}
      <aside
        className={`fixed md:sticky top-0 left-0 z-40 h-screen w-64 shrink-0 bg-[#0c2a23] text-emerald-100 flex flex-col justify-between border-r border-[#153f36] transition-transform duration-200 md:translate-x-0 ${
          isOpenMobile ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        {/* Brand Lockup */}
        <div>
          <div className="h-16 flex items-center px-5 border-b border-[#18453b]">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded bg-teal-800/80 border border-teal-600/40 flex items-center justify-center text-teal-200 shadow-xs">
                <HeartPulse className="w-5 h-5 text-emerald-300" />
              </div>
              <div>
                <h1 className="text-sm font-semibold tracking-tight text-white flex items-center gap-1.5">
                  Swasthya Twin
                </h1>
                <p className="text-[10px] text-teal-300/70 font-sans tracking-wide">
                  Happiest Health 2026
                </p>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="p-3 space-y-0.5">
            <div className="px-3 py-1.5 text-[10px] uppercase tracking-wider font-semibold text-teal-400/60">
              Longitudinal Workspace
            </div>
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    onSelectTab(item.id);
                    onCloseMobile();
                  }}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded text-xs font-medium transition-colors text-left ${
                    isActive
                      ? 'bg-teal-900/80 text-white font-semibold shadow-xs border border-teal-700/50'
                      : 'text-emerald-100/75 hover:bg-teal-950/40 hover:text-white'
                  }`}
                >
                  <Icon
                    className={`w-4 h-4 shrink-0 ${
                      isActive ? 'text-teal-300' : 'text-teal-400/70'
                    }`}
                  />
                  <span className="truncate">{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Selected Twin Context Footer Widget */}
        <div className="p-3 m-3 bg-[#081e19] rounded border border-[#16433a]">
          <div className="text-[10px] text-teal-400/70 uppercase tracking-wider font-medium mb-1">
            Active Digital Twin
          </div>
          <div className="flex items-baseline justify-between mb-1">
            <span className="text-xs font-semibold text-white font-mono">
              {activePatient.id}
            </span>
            <span className="text-[11px] text-teal-200 font-sans">
              {2026 - activePatient.birthYear}y · {activePatient.sexAtBirth.charAt(0)}
            </span>
          </div>
          <p className="text-[11px] text-teal-300/75 line-clamp-1">
            {activePatient.primaryFocus}
          </p>
          <div className="mt-2 pt-2 border-t border-[#16433a] flex items-center justify-between text-[10px] text-teal-400/60">
            <span>Status:</span>
            <span className="text-emerald-300 font-medium">
              {activePatient.monitoringStatus}
            </span>
          </div>
        </div>
      </aside>
    </>
  );
};
