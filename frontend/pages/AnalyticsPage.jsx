import React from "react";
import { tr } from "../i18n/index.js";
import {
  PageHeading,
  Pill,
  SystemCard,
} from "../components/common/index.js";
import { ENGINE_DEFINITIONS } from "../services/competency/competencyEngine.js";

export default function AnalyticsPage({ engine = {}, lang, data = {} }) {
  const maxScore = 5;
  const rawHours =
    data?.analytics?.learningMixHours ||
    engine?.learningHoursByDomain ||
    {};
  const totalHours =
    Object.values(rawHours).reduce((sum, value) => sum + Number(value || 0), 0) ||
    1;
  const assessmentHistory = engine?.assessmentHistory || [];
  const chartAssessments = assessmentHistory.slice(-5);
  const chartPoints = chartAssessments.map((item, i) => {
    const x = 65 + i * 125;
    const score = Math.max(0, Math.min(100, Number(item.score) || 0));
    const y = 220 - score * 1.5;
    return { x, y, score };
  });
  const polylinePoints = chartPoints
    .map((point) => `${point.x},${point.y}`)
    .join(" ");
  const barColors = ["green", "blue", "amber", "red", "purple"];

  const coursesList =
    data?.courses && data.courses.length > 0
      ? data.courses
      : data?.learningPath?.modules && data.learningPath.modules.length > 0
      ? data.learningPath.modules
      : [
          {
            title: "Compilation of Consumer Price Index (CPI) & Inflation Metrics",
            progress: 95,
            hours: 8,
            status: "Active",
          },
          {
            title: "System of National Accounts (SNA 2008) & GDP Compilation",
            progress: 70,
            hours: 12,
            status: "In Progress",
          },
          {
            title: "GIS & Spatial Statistics Intermediate Practice",
            progress: 40,
            hours: 10,
            status: "In Progress",
          },
          {
            title: "Data Quality & Survey Validation Practice",
            progress: 85,
            hours: 6,
            status: "Completed",
          },
        ];

  const totalCourseProgress = coursesList.reduce(
    (sum, c) => sum + Number(c.progress ?? (c.score || 50)),
    0
  );
  const avgCompletion = Math.round(
    totalCourseProgress / (coursesList.length || 1)
  );
  const activeTrackName =
    data?.learningPath?.track ||
    data?.profile?.course ||
    "National Statistical Capacity Track";

  return (
    <div className="stack analytics-page">
      <PageHeading
        kicker={tr(lang, "dataVisuals").toUpperCase()}
        title={tr(lang, "graphical")}
        subtitle={tr(lang, "visualSummary")}
      />
      <div className="analytics-kpi-grid">
        <SystemCard>
          <span>{tr(lang, "competency")}</span>
          <strong>
            {engine?.overallScore || 0}
            <small>/100</small>
          </strong>
        </SystemCard>
        <SystemCard>
          <span>{tr(lang, "score")}</span>
          <strong>
            {engine?.assessmentAverage || 0}
            <small>%</small>
          </strong>
        </SystemCard>
        <SystemCard>
          <span>{tr(lang, "hoursLabel")}</span>
          <strong>
            {engine?.learningHours || 0}
            <small>h</small>
          </strong>
        </SystemCard>
      </div>

      <div className="analytics-grid">
        <SystemCard className="chart-card">
          <div className="card-header">
            <div>
              <div className="system-label">01</div>
              <h2>{tr(lang, "competencyScores")}</h2>
            </div>
          </div>
          <div className="vertical-bars">
            {(engine?.competencies || []).map((c, i) => (
              <div className="vbar-item" key={c.key}>
                <div className="vbar-value">{(c.score || 0).toFixed(1)}</div>
                <div className="vbar-track">
                  <div
                    className={`vbar-fill ${barColors[i % barColors.length]}`}
                    style={{ height: `${((c.score || 0) / maxScore) * 100}%` }}
                  />
                </div>
                <span>{c.name.replace(" & Spatial Statistics", "")}</span>
              </div>
            ))}
          </div>
        </SystemCard>

        <SystemCard className="chart-card">
          <div className="card-header">
            <div>
              <div className="system-label">02</div>
              <h2>{tr(lang, "assessmentHistory")}</h2>
            </div>
          </div>
          <div className="line-chart-wrap">
            <svg
              viewBox="0 0 640 260"
              className="line-chart"
              role="img"
              aria-label={tr(lang, "assessmentHistory")}
            >
              <line x1="45" y1="220" x2="620" y2="220" />
              <line x1="45" y1="170" x2="620" y2="170" />
              <line x1="45" y1="120" x2="620" y2="120" />
              <line x1="45" y1="70" x2="620" y2="70" />
              {polylinePoints && (
                <polyline
                  points={polylinePoints}
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="4"
                />
              )}
              {chartPoints.map((point, i) => (
                <circle key={`${point.x}-${i}`} cx={point.x} cy={point.y} r="6" />
              ))}
              {chartAssessments.map((item, i) => (
                <text
                  key={`${item.title || item.domain || "Q"}-${i}`}
                  x={65 + i * 125 - 10}
                  y="245"
                >
                  Q{i + 1}
                </text>
              ))}
            </svg>
          </div>
          <div className="chart-footnote">
            {chartAssessments.length
              ? chartAssessments.map((item) => `${Number(item.score) || 0}%`).join(" → ")
              : tr(lang, "noData")}
          </div>
        </SystemCard>

        <SystemCard className="chart-card">
          <div className="card-header">
            <div>
              <div className="system-label">03</div>
              <h2>{tr(lang, "learningMix")}</h2>
            </div>
          </div>
          <div className="donut-layout">
            <div className="donut" aria-label={tr(lang, "learningMix")} />
            <div className="legend-list">
              {Object.entries(rawHours).map(([key, h], i) => {
                const def = ENGINE_DEFINITIONS.find((d) => d.key === key);
                return (
                  <div className="legend-row" key={key}>
                    <span className={`legend-dot ${barColors[i % barColors.length]}`} />
                    <div>
                      <strong>{def?.name || key}</strong>
                      <span>
                        {h} {tr(lang, "hoursLabel")}
                      </span>
                    </div>
                    <b>{Math.round((Number(h) / totalHours) * 100)}%</b>
                  </div>
                );
              })}
            </div>
          </div>
        </SystemCard>

        <SystemCard className="chart-card course-analytics-card">
          <div className="card-header">
            <div>
              <div className="system-label">04</div>
              <h2>{tr(lang, "courseAnalytics")}</h2>
            </div>
            <Pill tone="active">{coursesList.length} Courses</Pill>
          </div>
          <div className="course-analytics-content">
            <div className="course-velocity-stats">
              <div className="velocity-stat">
                <span>{tr(lang, "avgCompletion")}</span>
                <strong>{avgCompletion}%</strong>
              </div>
              <div className="velocity-stat">
                <span>{tr(lang, "activeTrack")}</span>
                <strong className="track-title" title={activeTrackName}>
                  {activeTrackName}
                </strong>
              </div>
              <div className="velocity-stat">
                <span>{tr(lang, "weeklyHours")}</span>
                <strong>
                  {Math.max(4, Math.round((engine?.learningHours || 16) / 4))}h/wk
                </strong>
              </div>
            </div>
            <div className="course-progress-list">
              {coursesList.slice(0, 4).map((c, idx) => {
                const pct = Math.max(
                  5,
                  Math.min(100, Number(c.progress ?? (c.score || 50)))
                );
                return (
                  <div
                    className="course-progress-row"
                    key={c.id || c.title || idx}
                  >
                    <div className="c-info">
                      <span className="c-title" title={c.title}>
                        {c.title}
                      </span>
                      <span className="c-meta">
                        {c.hours || c.duration || 6} hrs · {c.status || "Active"}
                      </span>
                    </div>
                    <div className="c-bar-wrap">
                      <div className="c-bar-track">
                        <div
                          className={`c-bar-fill ${barColors[idx % barColors.length]}`}
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                      <span className="c-pct">{pct}%</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </SystemCard>
      </div>
    </div>
  );
}
