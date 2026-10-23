import React, { useState, useMemo } from 'react';
import { Observation, MetricKey, MetricBaseline } from '../../types/health';
import { METRIC_DEFINITIONS } from '../../data/mockData';

interface InteractiveTrendChartProps {
  observations: Observation[];
  metricKey: MetricKey;
  baseline?: MetricBaseline;
  timeRange?: '1M' | '3M' | '6M' | '1Y' | 'ALL';
  height?: number;
  showBaselineBand?: boolean;
  showClinicalReference?: boolean;
}

export const InteractiveTrendChart: React.FC<InteractiveTrendChartProps> = ({
  observations,
  metricKey,
  baseline,
  timeRange = 'ALL',
  height = 280,
  showBaselineBand = true,
  showClinicalReference = true
}) => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  const def = METRIC_DEFINITIONS[metricKey] || METRIC_DEFINITIONS['systolic_bp'];

  // Filter observations by patient, metric, and time range
  const filteredData = useMemo(() => {
    const raw = observations
      .filter((o) => o.metricKey === metricKey)
      .sort((a, b) => new Date(a.recordedAt).getTime() - new Date(b.recordedAt).getTime());

    if (raw.length === 0) return [];
    if (timeRange === 'ALL') return raw;

    const latestTime = new Date(raw[raw.length - 1].recordedAt).getTime();
    let cutoffDays = 365;
    if (timeRange === '1M') cutoffDays = 30;
    if (timeRange === '3M') cutoffDays = 90;
    if (timeRange === '6M') cutoffDays = 180;
    if (timeRange === '1Y') cutoffDays = 365;

    const cutoffTime = latestTime - cutoffDays * 24 * 60 * 60 * 1000;
    const ranged = raw.filter((o) => new Date(o.recordedAt).getTime() >= cutoffTime);
    return ranged.length > 0 ? ranged : raw;
  }, [observations, metricKey, timeRange]);

  if (filteredData.length === 0) {
    return (
      <div
        className="flex flex-col items-center justify-center p-8 bg-stone-50/50 rounded border border-dashed border-stone-200 text-stone-500"
        style={{ height }}
      >
        <span className="text-sm font-medium text-stone-700">No longitudinal observations recorded</span>
        <span className="text-xs text-stone-400 mt-1">
          Record at least one {def.label} measurement to initialize the trend analysis.
        </span>
      </div>
    );
  }

  // Calculate scales and bounds
  const values = filteredData.map((d) => d.value);
  const minVal = Math.min(...values, def.normalMin);
  const maxVal = Math.max(...values, def.normalMax);
  const padding = (maxVal - minVal) * 0.15 || 5;

  const yMin = Math.floor(minVal - padding);
  const yMax = Math.ceil(maxVal + padding);
  const yRange = yMax - yMin || 1;

  const svgPadding = { top: 20, right: 30, bottom: 35, left: 45 };
  const viewBoxWidth = 700;
  const viewBoxHeight = height;
  const chartWidth = viewBoxWidth - svgPadding.left - svgPadding.right;
  const chartHeight = viewBoxHeight - svgPadding.top - svgPadding.bottom;

  // Coordinate transforms
  const getX = (index: number) => {
    if (filteredData.length === 1) return svgPadding.left + chartWidth / 2;
    return svgPadding.left + (index / (filteredData.length - 1)) * chartWidth;
  };

  const getY = (val: number) => {
    const clamped = Math.max(yMin, Math.min(yMax, val));
    return svgPadding.top + chartHeight - ((clamped - yMin) / yRange) * chartHeight;
  };

  // Generate SVG path for the data series
  const points = filteredData.map((d, i) => `${getX(i)},${getY(d.value)}`);
  const pathD = filteredData.length > 1 ? `M ${points.join(' L ')}` : '';
  const areaD =
    filteredData.length > 1
      ? `M ${getX(0)},${getY(yMin)} L ${points.join(' L ')} L ${getX(
          filteredData.length - 1
        )},${getY(yMin)} Z`
      : '';

  // Clinical reference band coords
  const refBandTop = getY(Math.min(yMax, def.normalMax));
  const refBandBottom = getY(Math.max(yMin, def.normalMin));
  const refBandHeight = Math.max(0, refBandBottom - refBandTop);

  // Y-axis ticks
  const tickCount = 5;
  const yTicks = Array.from({ length: tickCount }, (_, i) => {
    const val = yMin + (i / (tickCount - 1)) * yRange;
    return Math.round(val);
  });

  const activeObs = hoveredIndex !== null ? filteredData[hoveredIndex] : null;

  return (
    <div className="relative w-full select-none">
      <svg
        viewBox={`0 0 ${viewBoxWidth} ${viewBoxHeight}`}
        className="w-full h-auto overflow-visible"
        style={{ minHeight: height }}
      >
        <defs>
          <linearGradient id={`grad-${metricKey}`} x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#0f766e" stopOpacity="0.12" />
            <stop offset="100%" stopColor="#0f766e" stopOpacity="0.0" />
          </linearGradient>
        </defs>

        {/* Clinical Normal Target Region */}
        {showClinicalReference && (
          <g>
            <rect
              x={svgPadding.left}
              y={refBandTop}
              width={chartWidth}
              height={refBandHeight}
              fill="#ecfdf5"
              opacity="0.75"
            />
            <line
              x1={svgPadding.left}
              y1={refBandTop}
              x2={svgPadding.left + chartWidth}
              y2={refBandTop}
              stroke="#a7f3d0"
              strokeDasharray="3 3"
              strokeWidth="1"
            />
            <text
              x={svgPadding.left + chartWidth - 8}
              y={refBandTop + 12}
              textAnchor="end"
              className="text-[10px] fill-emerald-700 font-sans font-medium"
            >
              Clinical Optimal Zone ({def.optimalTarget})
            </text>
          </g>
        )}

        {/* Y Axis Grid Lines & Labels */}
        {yTicks.map((tickVal, i) => {
          const y = getY(tickVal);
          return (
            <g key={`ytick-${i}`}>
              <line
                x1={svgPadding.left}
                y1={y}
                x2={svgPadding.left + chartWidth}
                y2={y}
                stroke="#e2e8f0"
                strokeWidth="1"
                strokeDasharray="2 2"
              />
              <text
                x={svgPadding.left - 8}
                y={y + 3}
                textAnchor="end"
                className="text-[10px] fill-slate-400 font-mono tabular-nums"
              >
                {tickVal}
              </text>
            </g>
          );
        })}

        {/* Personal Baseline Line */}
        {showBaselineBand && baseline && baseline.observationCount >= 2 && (
          <g>
            <line
              x1={svgPadding.left}
              y1={getY(baseline.mean)}
              x2={svgPadding.left + chartWidth}
              y2={getY(baseline.mean)}
              stroke="#0f766e"
              strokeWidth="1.5"
              strokeDasharray="4 4"
            />
            <text
              x={svgPadding.left + 10}
              y={getY(baseline.mean) - 6}
              className="text-[10px] fill-teal-800 font-sans font-semibold tracking-tight"
            >
              Personal Baseline: {baseline.mean} {def.unit} (±{baseline.standardDeviation})
            </text>
          </g>
        )}

        {/* Area fill under curve */}
        {areaD && <path d={areaD} fill={`url(#grad-${metricKey})`} />}

        {/* Trend Line */}
        {pathD && (
          <path
            d={pathD}
            fill="none"
            stroke="#0f766e"
            strokeWidth="2.25"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        )}

        {/* Hover Crosshair */}
        {hoveredIndex !== null && (
          <line
            x1={getX(hoveredIndex)}
            y1={svgPadding.top}
            x2={getX(hoveredIndex)}
            y2={svgPadding.top + chartHeight}
            stroke="#94a3b8"
            strokeWidth="1"
            strokeDasharray="2 2"
          />
        )}

        {/* Data points */}
        {filteredData.map((d, i) => {
          const cx = getX(i);
          const cy = getY(d.value);
          const isHovered = hoveredIndex === i;

          return (
            <g
              key={d.id || `point-${i}`}
              className="cursor-pointer group"
              onMouseEnter={() => setHoveredIndex(i)}
              onMouseLeave={() => setHoveredIndex(null)}
            >
              {/* Invisible large hit area */}
              <circle cx={cx} cy={cy} r="14" fill="transparent" />
              {/* Visible dot */}
              <circle
                cx={cx}
                cy={cy}
                r={isHovered ? 5.5 : 3.5}
                fill={isHovered ? '#042f2e' : '#ffffff'}
                stroke="#0f766e"
                strokeWidth={isHovered ? 2.5 : 1.75}
                className="transition-all duration-150"
              />
            </g>
          );
        })}

        {/* X Axis Date Labels */}
        {filteredData.map((d, i) => {
          // Show label if first, last, or evenly spaced
          const showLabel =
            filteredData.length <= 8 ||
            i === 0 ||
            i === filteredData.length - 1 ||
            i % Math.ceil(filteredData.length / 5) === 0;

          if (!showLabel) return null;

          const cx = getX(i);
          const formattedDate = new Date(d.recordedAt).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric'
          });

          return (
            <text
              key={`xlabel-${d.id || i}`}
              x={cx}
              y={svgPadding.top + chartHeight + 18}
              textAnchor="middle"
              className="text-[10px] fill-slate-500 font-sans"
            >
              {formattedDate}
            </text>
          );
        })}
      </svg>

      {/* Interactive Tooltip Card */}
      {activeObs && hoveredIndex !== null && (
        <div
          className="absolute z-20 pointer-events-none bg-slate-900 text-white rounded-md p-2.5 shadow-lg text-xs transform -translate-x-1/2 -translate-y-full transition-all duration-75"
          style={{
            left: `${(getX(hoveredIndex) / viewBoxWidth) * 100}%`,
            top: `${(getY(activeObs.value) / viewBoxHeight) * 100 - 8}%`
          }}
        >
          <div className="flex items-center justify-between gap-4 border-b border-slate-700 pb-1 mb-1.5">
            <span className="font-semibold text-white">
              {activeObs.value} {def.unit}
            </span>
            <span className="text-[11px] text-slate-300 font-mono">
              {new Date(activeObs.recordedAt).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
              })}
            </span>
          </div>
          {baseline && baseline.observationCount >= 2 && (
            <div className="text-[11px] text-slate-300 flex items-center justify-between gap-3">
              <span>vs Personal Baseline:</span>
              <span
                className={`font-mono font-medium ${
                  activeObs.value - baseline.mean < 0
                    ? 'text-emerald-400'
                    : activeObs.value - baseline.mean > 0
                    ? 'text-amber-400'
                    : 'text-slate-300'
                }`}
              >
                {activeObs.value - baseline.mean > 0 ? '+' : ''}
                {(activeObs.value - baseline.mean).toFixed(1)} {def.unit}
              </span>
            </div>
          )}
          {activeObs.contextNotes && (
            <div className="text-[10px] text-slate-400 mt-1 italic">
              {activeObs.contextNotes}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
