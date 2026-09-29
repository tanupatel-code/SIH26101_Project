import React, { useMemo, useState } from "react";
import { ChevronDown, Search } from "lucide-react";
import { tr } from "../i18n/index.js";
import {
  PageHeading,
  Pill,
  Progress,
  SystemCard,
} from "../components/common/index.js";

export default function CompetenciesPage({ engine = {}, lang, data = {} }) {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState(null);

  const competencies = engine?.competencies || [];
  const filtered = useMemo(
    () =>
      competencies.filter((c) =>
        (c.name || "").toLowerCase().includes(query.toLowerCase())
      ),
    [competencies, query]
  );

  const avgScore = competencies.length
    ? (
        competencies.reduce((s, c) => s + (c.score || 0), 0) /
        competencies.length
      ).toFixed(1)
    : "0.0";

  return (
    <div className="stack">
      <PageHeading
        kicker={tr(lang, "competencyEngine").toUpperCase()}
        title={tr(lang, "competencies")}
        subtitle={tr(lang, "visualSummary")}
        actions={
          <div className="search">
            <Search size={15} />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={tr(lang, "search")}
              aria-label={tr(lang, "search")}
            />
          </div>
        }
      />

      <div className="summary-grid">
        <SystemCard className="summary-card">
          <span>{tr(lang, "competencies").toUpperCase()}</span>
          <strong>{competencies.length}</strong>
        </SystemCard>
        <SystemCard className="summary-card">
          <span>{tr(lang, "strong").toUpperCase()}</span>
          <strong className="green">{engine?.strongSkills || 0}</strong>
        </SystemCard>
        <SystemCard className="summary-card">
          <span>{tr(lang, "gaps").toUpperCase()}</span>
          <strong className="amber">
            {(engine?.criticalGaps || 0) + (engine?.moderateGaps || 0)}
          </strong>
        </SystemCard>
        <SystemCard className="summary-card">
          <span>{tr(lang, "score").toUpperCase()}</span>
          <strong className="cyan">{avgScore} / 5</strong>
        </SystemCard>
      </div>

      <SystemCard className="engine-competency-block">
        <div className="engine-panel-head">
          <div>
            <div className="system-label">{tr(lang, "gapAssessment")}</div>
            <h2>Benchmark comparison</h2>
            <p>
              Multi-signal competency analysis across assessment, course, self-assessment and learning effort.
            </p>
          </div>
          <div className="engine-score">
            {engine?.overallScore || 0}
            <span>/100</span>
          </div>
        </div>

        <div className="engine-evidence-grid">
          {competencies.map((item) => (
            <div className="engine-evidence" key={item.key}>
              <div className="engine-evidence-title">
                <strong>{item.name}</strong>
                <Pill tone={(item.level || "").toLowerCase()}>{item.level}</Pill>
              </div>
              <Progress value={(item.score || 0) * 20} color="cyan" />
              <div className="engine-evidence-meta">
                <span>{(item.score || 0).toFixed(1)}/5</span>
                <span>
                  {item.gap ? `Gap ${item.gap.toFixed(1)}` : "Benchmark met"}
                </span>
                <span>{item.trend || "Stable"}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="recommendation-stack">
          <div className="system-label">{tr(lang, "priority")}</div>
          {(engine?.recommendations || []).map((r, i) => (
            <div className="recommendation-line" key={r}>
              <b>0{i + 1}</b>
              <span>{r}</span>
            </div>
          ))}
        </div>
      </SystemCard>

      <SystemCard>
        <div className="card-header">
          <div>
            <div className="system-label">CRITICAL SKILLS</div>
            <h2>Critical Skill Gaps</h2>
          </div>
          <Pill>{(data?.criticalSkills || []).length}</Pill>
        </div>
        <div className="assessment-list">
          {(data?.criticalSkills || []).map((item, i) => (
            <div className="assessment" key={`${item.competency}-${i}`}>
              <div className="assessment-number">0{i + 1}</div>
              <div className="grow">
                <strong>{item.competency}</strong>
                <span>
                  {item.priority || "Priority"} ·{" "}
                  {Number(item.currentScore || 0).toFixed(2)}/5 · Gap{" "}
                  {Number(item.gap || 0).toFixed(2)}
                </span>
              </div>
              <div className="grow">
                <span>
                  {item.recommendedAction || "Targeted practice recommended."}
                </span>
              </div>
            </div>
          ))}
        </div>
      </SystemCard>

      <SystemCard>
        <div className="card-header">
          <div>
            <div className="system-label">BENCHMARK COMPARISON</div>
            <h2>Current Readiness</h2>
          </div>
          <Pill>{(data?.benchmarkComparison || []).length}</Pill>
        </div>
        <div className="assessment-list">
          {(data?.benchmarkComparison || []).map((item, i) => (
            <div className="assessment" key={`${item.competency}-${i}`}>
              <div className="assessment-number">0{i + 1}</div>
              <div className="grow">
                <strong>{item.competency}</strong>
                <span>
                  {Number(item.currentScore || 0).toFixed(2)} /{" "}
                  {Number(item.benchmark || 0).toFixed(2)} · {item.status || "—"}
                </span>
              </div>
              <strong>{Number(item.readinessPercent || 0).toFixed(1)}%</strong>
            </div>
          ))}
        </div>
      </SystemCard>

      <SystemCard>
        <div className="card-header">
          <div>
            <div className="system-label">{tr(lang, "skillMatrix")}</div>
            <h2>{tr(lang, "currentReadiness")}</h2>
          </div>
          <Pill>{competencies.length} domains</Pill>
        </div>
        <div className="detail-list">
          {filtered.map((item) => {
            const Icon = item.icon;
            const open = selected === item.name;
            return (
              <div
                className={`detail-row ${open ? "open" : ""}`}
                key={item.name}
              >
                <button
                  className="detail-trigger"
                  onClick={() => setSelected(open ? null : item.name)}
                  aria-expanded={open}
                >
                  <div className={`mini-icon ${item.color || "cyan"}`}>
                    {Icon && <Icon size={16} />}
                  </div>
                  <div className="grow">
                    <strong>{item.name}</strong>
                    <span>{item.description || item.desc}</span>
                    <Progress
                      value={(item.score || 0) * 20}
                      color={item.color || "cyan"}
                    />
                  </div>
                  <div className="detail-score">
                    <strong>{(item.score || 0).toFixed(1)}</strong>
                    <Pill tone={(item.level || "").toLowerCase()}>
                      {item.level}
                    </Pill>
                  </div>
                  <ChevronDown
                    size={15}
                    className={open ? "rotate" : ""}
                    aria-hidden="true"
                  />
                </button>
                {open && (
                  <div className="detail-body">
                    <div>
                      <span>Trend</span>
                      <strong>{item.trend || "Stable"}</strong>
                    </div>
                    <div>
                      <span>Benchmark</span>
                      <strong>{item.benchmark || 3.5} / 5</strong>
                    </div>
                    <div>
                      <span>Priority</span>
                      <strong>{item.level === "Weak" ? "High" : "Normal"}</strong>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </SystemCard>
    </div>
  );
}
