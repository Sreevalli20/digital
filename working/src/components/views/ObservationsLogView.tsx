import React, { useState, useMemo } from 'react';
import { PatientProfile, Observation, MetricCategory } from '../../types/health';
import { METRIC_DEFINITIONS } from '../../data/mockData';
import {
  Search,
  Filter,
  Plus,
  ArrowUpDown,
  Download,
  Calendar,
  Layers,
  Trash2,
  CheckCircle2,
  Tag
} from 'lucide-react';

interface ObservationsLogViewProps {
  observations: Observation[];
  patients: PatientProfile[];
  activePatientId: string;
  onOpenRecordModal: () => void;
  onDeleteObservation?: (id: string) => void;
}

export const ObservationsLogView: React.FC<ObservationsLogViewProps> = ({
  observations,
  patients,
  activePatientId,
  onOpenRecordModal,
  onDeleteObservation
}) => {
  const [patientFilter, setPatientFilter] = useState<string>(activePatientId);
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortOrder, setSortOrder] = useState<'desc' | 'asc'>('desc');
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 15;

  const filteredObservations = useMemo(() => {
    return observations
      .filter((o) => {
        const matchesPatient = patientFilter === 'all' || o.patientId === patientFilter;
        const matchesCategory = categoryFilter === 'all' || o.category === categoryFilter;
        const matchesSearch =
          searchQuery === '' ||
          o.metricKey.toLowerCase().includes(searchQuery.toLowerCase()) ||
          (METRIC_DEFINITIONS[o.metricKey]?.label || '')
            .toLowerCase()
            .includes(searchQuery.toLowerCase()) ||
          (o.contextNotes || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
          o.recordedAt.includes(searchQuery);

        return matchesPatient && matchesCategory && matchesSearch;
      })
      .sort((a, b) => {
        const timeA = new Date(a.recordedAt).getTime();
        const timeB = new Date(b.recordedAt).getTime();
        return sortOrder === 'desc' ? timeB - timeA : timeA - timeB;
      });
  }, [observations, patientFilter, categoryFilter, searchQuery, sortOrder]);

  const totalPages = Math.ceil(filteredObservations.length / pageSize) || 1;
  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredObservations.slice(start, start + pageSize);
  }, [filteredObservations, currentPage]);

  return (
    <div className="space-y-6">
      {/* Search, Filter & Action Toolbar */}
      <div className="bg-white rounded-lg border border-slate-200 p-4 shadow-2xs space-y-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div className="flex flex-1 items-center gap-3">
            {/* Search Input */}
            <div className="relative flex-1 max-w-sm">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search biomarker, date, or clinical notes..."
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded text-slate-900 focus:outline-none focus:ring-1 focus:ring-teal-700"
              />
            </div>

            {/* Patient Filter */}
            <select
              value={patientFilter}
              onChange={(e) => {
                setPatientFilter(e.target.value);
                setCurrentPage(1);
              }}
              className="text-xs bg-slate-50 border border-slate-200 rounded px-2.5 py-1.5 text-slate-800 font-mono"
            >
              <option value="all">All Patients ({patients.length})</option>
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.id} ({p.monitoringStatus})
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc')}
              className="flex items-center gap-1.5 text-xs text-slate-700 bg-slate-50 hover:bg-slate-100 border border-slate-200 px-3 py-1.5 rounded transition-colors"
            >
              <ArrowUpDown className="w-3.5 h-3.5" />
              <span>{sortOrder === 'desc' ? 'Newest' : 'Oldest'}</span>
            </button>

            <button
              onClick={onOpenRecordModal}
              className="flex items-center gap-1.5 text-xs font-semibold text-white bg-teal-800 hover:bg-teal-900 px-3 py-1.5 rounded transition-colors shadow-2xs"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Record Observation</span>
            </button>
          </div>
        </div>

        {/* Category Filter Pills */}
        <div className="flex flex-wrap items-center gap-1.5 pt-2 border-t border-slate-100 text-xs">
          <span className="text-[11px] text-slate-400 mr-1">Domain:</span>
          {['all', 'cardiovascular', 'metabolic', 'anthropometric'].map((cat) => (
            <button
              key={cat}
              onClick={() => {
                setCategoryFilter(cat);
                setCurrentPage(1);
              }}
              className={`px-2.5 py-1 rounded transition-colors capitalize ${
                categoryFilter === cat
                  ? 'bg-teal-900 text-white font-semibold shadow-2xs'
                  : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border border-slate-200/80'
              }`}
            >
              {cat === 'all' ? 'All Domains' : cat}
            </button>
          ))}
          <span className="ml-auto text-[11px] text-slate-500 font-mono">
            Showing {filteredObservations.length} observations
          </span>
        </div>
      </div>

      {/* Observations Ledger Table */}
      <div className="bg-white rounded-lg border border-slate-200 overflow-hidden shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 font-medium bg-slate-50/70">
                <th className="py-2.5 px-4">Observation Date</th>
                <th className="py-2.5 px-4">Twin ID</th>
                <th className="py-2.5 px-4">Biomarker / Measurement</th>
                <th className="py-2.5 px-4 text-right">Value</th>
                <th className="py-2.5 px-4">Domain</th>
                <th className="py-2.5 px-4">Clinical Context Notes</th>
                <th className="py-2.5 px-4">Status & Target</th>
                <th className="py-2.5 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {paginatedData.map((obs) => {
                const def = METRIC_DEFINITIONS[obs.metricKey];
                const isOptimal = def && obs.value <= def.normalMax && obs.value >= def.normalMin;

                return (
                  <tr key={obs.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4 font-mono text-slate-700 whitespace-nowrap">
                      {obs.recordedAt}
                    </td>
                    <td className="py-3 px-4 font-mono font-semibold text-slate-900">
                      {obs.patientId}
                    </td>
                    <td className="py-3 px-4 font-medium text-slate-900">
                      {def?.label || obs.metricKey}
                    </td>
                    <td className="py-3 px-4 text-right font-mono font-bold text-slate-900 tabular-nums">
                      {obs.value} <span className="text-slate-400 font-normal">{obs.unit}</span>
                    </td>
                    <td className="py-3 px-4 capitalize text-slate-500">
                      {obs.category}
                    </td>
                    <td className="py-3 px-4 text-slate-500 max-w-xs truncate">
                      {obs.contextNotes || 'Routine observation'}
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <span
                        className={`text-[11px] font-medium ${
                          isOptimal ? 'text-emerald-700' : 'text-amber-700'
                        }`}
                      >
                        {isOptimal ? 'Within Reference' : 'Variance Noted'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      {onDeleteObservation && (
                        <button
                          onClick={() => onDeleteObservation(obs.id)}
                          className="text-slate-400 hover:text-rose-600 p-1 rounded"
                          title="Delete observation"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {filteredObservations.length === 0 && (
          <div className="p-8 text-center text-slate-400 text-xs">
            No observations matching your current filters.
          </div>
        )}

        {/* Pagination Controls */}
        <div className="p-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500 bg-slate-50/50">
          <span>
            Page {currentPage} of {totalPages}
          </span>
          <div className="flex items-center gap-1">
            <button
              disabled={currentPage <= 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="px-2.5 py-1 rounded border border-slate-200 bg-white disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50"
            >
              Previous
            </button>
            <button
              disabled={currentPage >= totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="px-2.5 py-1 rounded border border-slate-200 bg-white disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
