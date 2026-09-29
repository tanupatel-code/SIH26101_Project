import React from "react";
import {
  Activity,
  AlertTriangle,
  CalendarDays,
  Check,
  ChevronRight,
  ClipboardCheck,
  Lock,
  Sparkles,
  Target,
  TrendingUp,
} from "lucide-react";
import { tr } from "../i18n/index.js";
import {
  PageHeading,
  Pill,
  Progress,
  StatCard,
  SystemCard,
} from "../components/common/index.js";
import { isOfficerUser } from "../services/auth/authService.js";

export default function DashboardPage({ user = {}, lang, onNavigate, engine = {}, data = {} }) {
  const modules = data?.learningPath?.modules || data?.modules || [];
  const assessments = data?.assessments || [];
  const activeModule =
    modules.find((m) => m?.state === "active") ||
    modules.find((m) => String(m?.status || "").toLowerCase() === "in progress");
  const nextRecommendation =
    engine?.recommendations?.[0] ||
    "Continue your learning path and complete the active module.";
  const projectId = user?.projectId || data?.profile?.projectId || "SIH26101";
  const moduleProgress = Number(activeModule?.progress || 0);
  const isOfficer = isOfficerUser(user);
  const defaultRole = isOfficer
    ? "Senior Statistical Officer (SSO)"
    : "Citizen Data Analyst & Research Scholar";
  const defaultDept = isOfficer ? "MoSPI" : "Academic / Citizen Track";

  return (
    <div className="stack">
      <PageHeading
        kicker={tr(lang, "command")}
        title={`${tr(lang, "hello")}, ${user?.name || "Learner"}.`}
        subtitle={`${user?.role || defaultRole} · ${user?.department || defaultDept} · ${projectId}`}
        actions={
          <Pill tone="online">
            <Activity size={12} /> {tr(lang, "online")}
          </Pill>
        }
      />

      <div className="stats-grid">
        <StatCard
          label={tr(lang, "competency")}
          value={engine?.overallScore || 0}
          suffix="/100"
          meta="Diagnostic index score"
          color="cyan"
          icon={Target}
        />
        <StatCard
          label={tr(lang, "gaps")}
          value={(engine?.criticalGaps || 0) + (engine?.moderateGaps || 0)}
          meta={
            engine?.topGaps?.map((g) => g.name).slice(0, 2).join(" · ") ||
            "No critical gaps"
          }
          color="red"
          icon={AlertTriangle}
        />
        <StatCard
          label={tr(lang, "learning")}
          value={engine?.learningProgress ?? 0}
          suffix="%"
          meta={`${engine?.completedModules ?? 0}/${engine?.totalModules ?? 0} modules`}
          color="green"
          icon={TrendingUp}
        />
        <StatCard
          label={tr(lang, "completed")}
          value={engine?.assessmentsCompleted ?? 0}
          suffix={`/${engine?.assessmentsTotal ?? 0}`}
          meta="Recorded scored evaluations"
          color="purple"
          icon={ClipboardCheck}
        />
      </div>

      <div className="hero-grid">
        <SystemCard className="player-card">
          <div className="system-label">{tr(lang, "player")}</div>
          <div className="player-layout">
            <div className="avatar-xl">{(user?.name || "A")[0]}</div>
            <div className="player-info">
              <div className="player-name">{user?.name || "Learner"}</div>
              <div className="player-role">{user?.role || defaultRole}</div>
              <div className="rank-line">
                <span>{tr(lang, "rank").toUpperCase()}</span>
                <strong>
                  {isOfficer
                    ? "MoSPI Cadre (SSS)"
                    : user?.department || "National Open Statistical Learning"}
                </strong>
                <span>{tr(lang, "level").toUpperCase()}</span>
                <strong>{engine?.overallScore || 0}% Ready</strong>
              </div>
              <div className="xp-row">
                <span>{tr(lang, "xp")}</span>
                <Progress value={engine?.overallScore || 0} color="cyan" />
                <strong>{engine?.overallScore || 0}/100</strong>
              </div>
            </div>
          </div>
          <div className="metric-strip">
            <div>
              <span>SAMPLING & INFERENCE</span>
              <strong>
                {(
                  engine?.competencies?.find((c) => c.key === "statisticalMethods")
                    ?.score ?? 0
                ).toFixed(1)}
              </strong>
            </div>
            <div>
              <span>DATA QUALITY</span>
              <strong>
                {(
                  engine?.competencies?.find((c) => c.key === "dataQuality")
                    ?.score ?? 0
                ).toFixed(1)}
              </strong>
            </div>
            <div>
              <span>GIS & SPATIAL</span>
              <strong>
                {(
                  engine?.competencies?.find((c) => c.key === "gis")?.score ?? 0
                ).toFixed(1)}
              </strong>
            </div>
            <div>
              <span>DATA SCIENCE & ML</span>
              <strong>
                {(
                  engine?.competencies?.find((c) => c.key === "machineLearning")
                    ?.score ?? 0
                ).toFixed(1)}
              </strong>
            </div>
          </div>
        </SystemCard>

        <SystemCard className="recommendation-card">
          <div className="system-label">{tr(lang, "recommendation")}</div>
          <div className="recommendation-title">
            <Sparkles size={18} /> {activeModule?.title || "Learning Path"}
          </div>
          <p>{nextRecommendation}</p>
          <div className="recommendation-box">
            <div>
              <span>{tr(lang, "activeModule").toUpperCase()}</span>
              <strong>{activeModule?.title || "No active module"}</strong>
            </div>
            <Progress value={moduleProgress} color="cyan" />
            <span className="progress-label">{moduleProgress}% complete</span>
          </div>
          <button className="primary-btn" onClick={() => onNavigate("Learning Path")}>
            {tr(lang, "continue")} <ChevronRight size={16} />
          </button>
        </SystemCard>
      </div>

      <div className="three-grid">
        <SystemCard>
          <div className="card-header">
            <div>
              <div className="system-label">{tr(lang, "matrix").toUpperCase()}</div>
              <h2>{tr(lang, "competencies")}</h2>
            </div>
            <button className="ghost-btn" onClick={() => onNavigate("My Competencies")}>
              {tr(lang, "viewAll")} <ChevronRight size={14} />
            </button>
          </div>
          <div className="compact-list">
            {(engine?.competencies || []).map((item) => {
              const Icon = item.icon;
              return (
                <div className="compact-row" key={item.key}>
                  <div className={`mini-icon ${item.color || "cyan"}`}>
                    <Icon size={15} />
                  </div>
                  <div className="grow">
                    <strong>{item.name}</strong>
                    <Progress value={item.score * 20} color={item.color || "cyan"} />
                  </div>
                  <strong className={`score ${item.color || "cyan"}`}>
                    {item.score.toFixed(1)}
                  </strong>
                </div>
              );
            })}
          </div>
        </SystemCard>

        <SystemCard>
          <div className="card-header">
            <div>
              <div className="system-label">
                {tr(lang, "trainingPipeline").toUpperCase()}
              </div>
              <h2>{tr(lang, "path")}</h2>
            </div>
            <button className="ghost-btn" onClick={() => onNavigate("Learning Path")}>
              {tr(lang, "viewAll")} <ChevronRight size={14} />
            </button>
          </div>
          <div className="timeline">
            {modules.map((m) => (
              <div className="timeline-row" key={m.step}>
                <div className={`timeline-node ${m.state || "locked"}`}>
                  {m.state === "done" ? (
                    <Check size={13} />
                  ) : m.state === "locked" ? (
                    <Lock size={12} />
                  ) : (
                    m.step
                  )}
                </div>
                <div className="grow">
                  <strong>{m.title}</strong>
                  <span>
                    {m.status} · {m.duration}
                  </span>
                </div>
                {m.state !== "locked" && (
                  <div className="mini-progress">
                    <Progress
                      value={m.progress}
                      color={m.state === "done" ? "green" : "cyan"}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        </SystemCard>

        <SystemCard>
          <div className="card-header">
            <div>
              <div className="system-label">{tr(lang, "schedule").toUpperCase()}</div>
              <h2>{tr(lang, "upcoming")}</h2>
            </div>
            <CalendarDays size={17} />
          </div>
          <div className="assessment-list">
            {assessments.slice(0, 5).map((a, index) => (
              <div
                className={`assessment ${["blue", "amber", "green", "purple", "red"][index % 5]}`}
                key={a.id || a.title || index}
              >
                <div className="assessment-date">{a.id || `A${index + 1}`}</div>
                <div className="grow">
                  <strong>{a.title || a.domain || "Assessment"}</strong>
                  <span>
                    {a.domain || "Assessment"} · Score {Number(a.score ?? 0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </SystemCard>
      </div>

      <SystemCard className="insight-card">
        <div className="insight-icon">
          <Sparkles size={22} />
        </div>
        <div className="grow">
          <div className="system-label">{tr(lang, "insight")}</div>
          <h2>{tr(lang, "trajectory")}</h2>
          <p>{nextRecommendation}</p>
        </div>
        <button
          className="secondary-btn"
          onClick={() => onNavigate("My Competencies")}
        >
          {tr(lang, "openAnalysis")} <ChevronRight size={14} />
        </button>
      </SystemCard>
    </div>
  );
}
