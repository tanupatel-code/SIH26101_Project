import React, { useState } from "react";
import {
  BookOpen,
  CheckCircle2,
  ExternalLink,
  GraduationCap,
  Lock,
  PlayCircle,
  TrendingUp,
  X,
} from "lucide-react";
import { tr } from "../i18n/index.js";
import {
  PageHeading,
  Pill,
  Progress,
  SystemCard,
} from "../components/common/index.js";
import IgotHub from "../IgotHub.jsx";
import { API_BASE_URL } from "../services/api/client.js";

export default function LearningPathPage({
  lang,
  data = {},
  engine = {},
  onNavigate,
  onStartQuiz,
  apiToken = "",
}) {
  const [selectedModule, setSelectedModule] = useState(null);
  const [activeTab, setActiveTab] = useState("curriculum"); // "curriculum" | "igot"

  const modules = data?.learningPath?.modules || data?.modules || [];
  const completed = engine?.completedModules ?? 0;
  const total = engine?.totalModules ?? modules.length;
  const progress = engine?.learningProgress ?? 0;
  const totalHours = engine?.learningHours ?? 0;

  return (
    <div className="stack">
      <PageHeading
        kicker={tr(lang, "trainingPipeline").toUpperCase()}
        title={tr(lang, "path")}
        subtitle={`${completed} of ${total} modules completed · ${totalHours} learning hours`}
        actions={
          <div className="tab-pill-row">
            <button
              type="button"
              className={`pill-btn ${activeTab === "curriculum" ? "active" : ""}`}
              onClick={() => setActiveTab("curriculum")}
            >
              <TrendingUp size={14} /> Roadmap
            </button>
            <button
              type="button"
              className={`pill-btn ${activeTab === "igot" ? "active" : ""}`}
              onClick={() => setActiveTab("igot")}
            >
              <GraduationCap size={14} /> iGOT Karmayogi Hub
            </button>
          </div>
        }
      />

      {activeTab === "igot" ? (
        <IgotHub
          apiBaseUrl={API_BASE_URL}
          apiToken={apiToken}
          userCourses={data?.courses || []}
          criticalSkills={data?.criticalSkills || []}
        />
      ) : (
        <>
          <SystemCard className="track-banner">
            <div>
              <div className="system-label">
                {tr(lang, "activeTrack").toUpperCase()}
              </div>
              <h2>
                {data?.learningPath?.track ||
                  data?.profile?.course ||
                  data?.profile?.track ||
                  "Learning Path"}
              </h2>
              <p>
                {completed} of {total} modules completed · {totalHours} hours recorded
              </p>
            </div>
            <div className="track-ring">{progress}%</div>
          </SystemCard>

          <div className="module-grid">
            {modules.map((m) => (
              <SystemCard
                key={m.step || m.title}
                className={`module-card ${m.state || "locked"}`}
              >
                <div className="module-top">
                  <span className="module-number">0{m.step}</span>
                  <Pill
                    tone={
                      m.state === "done"
                        ? "strong"
                        : m.state === "active"
                        ? "active"
                        : "locked"
                    }
                  >
                    {m.status === "Completed"
                      ? tr(lang, "completed")
                      : m.status === "In Progress"
                      ? tr(lang, "inProgress")
                      : tr(lang, "locked")}
                  </Pill>
                </div>
                <h2>{m.title}</h2>
                <p>
                  Structured module with practical lessons, domain exercises and assessment checkpoints.
                </p>
                <div className="module-meta">
                  <span>{m.duration || "—"}</span>
                  <span>
                    {m.lessons || "—"} {tr(lang, "lessons")}
                  </span>
                </div>
                <Progress
                  value={m.progress || 0}
                  color={m.state === "done" ? "green" : "cyan"}
                />
                <button
                  className={
                    m.state === "locked" ? "secondary-btn disabled" : "primary-btn"
                  }
                  disabled={m.state === "locked"}
                  onClick={() => setSelectedModule(m)}
                  title={
                    m.state === "locked"
                      ? "Prerequisites required"
                      : "Open module curriculum workspace"
                  }
                >
                  {m.state === "locked" ? <Lock size={14} /> : <PlayCircle size={14} />}
                  {m.state === "done"
                    ? tr(lang, "reviewModule")
                    : m.state === "active"
                    ? tr(lang, "continueModule")
                    : tr(lang, "locked")}
                </button>
              </SystemCard>
            ))}
          </div>
        </>
      )}

      {selectedModule && (
        <div
          className="app-modal-overlay"
          onClick={() => setSelectedModule(null)}
          role="dialog"
          aria-modal="true"
        >
          <div className="app-modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="app-modal-header">
              <div>
                <div className="system-label" style={{ color: "#0f2e5a" }}>
                  MODULE 0{selectedModule.step} · {selectedModule.duration || "8 hrs"}
                </div>
                <h3>{selectedModule.title}</h3>
                <p>National Statistical System Accredited Training Syllabus</p>
              </div>
              <button
                className="icon-btn"
                onClick={() => setSelectedModule(null)}
                aria-label="Close"
              >
                <X size={16} />
              </button>
            </div>
            <div className="app-modal-body">
              <div
                className="credential-seal-banner"
                style={{ background: "#eff6ff", borderColor: "#bfdbfe", color: "#1e40af" }}
              >
                <div
                  className="credential-seal-icon"
                  style={{ background: "#dbeafe", color: "#1d4ed8" }}
                >
                  <BookOpen size={24} />
                </div>
                <div className="credential-seal-text">
                  <strong style={{ color: "#1e3a8a" }}>
                    Curriculum Syllabus & Practice Directives
                  </strong>
                  <span style={{ color: "#2563eb" }}>
                    Status: {selectedModule.status || "In Progress"} · {selectedModule.progress || 0}% Completed
                  </span>
                </div>
              </div>

              <div className="lesson-checklist">
                <div className="lesson-check-item">
                  <div>
                    <strong>Lesson 1: Theoretical Framework & Official Sampling Design</strong>
                    <span>Stratified multistage sampling & UN fundamental principles</span>
                  </div>
                  <CheckCircle2 size={16} color="#059669" />
                </div>
                <div className="lesson-check-item">
                  <div>
                    <strong>Lesson 2: Field Protocols, CAPI Enumeration & Data Cleaning</strong>
                    <span>Survey protocols, non-sampling error minimization</span>
                  </div>
                  <CheckCircle2 size={16} color="#059669" />
                </div>
                <div className="lesson-check-item">
                  <div>
                    <strong>Lesson 3: Computational Tabulation & Statistical Software Practice</strong>
                    <span>Automated consistency checks using Python, R & QGIS</span>
                  </div>
                  <CheckCircle2
                    size={16}
                    color={selectedModule.state === "done" ? "#059669" : "#94a3b8"}
                  />
                </div>
                <div className="lesson-check-item">
                  <div>
                    <strong>Lesson 4: Diagnostic Validation & Verification Checkpoint</strong>
                    <span>End-of-module assessment derived from MoSPI manuals</span>
                  </div>
                  <CheckCircle2
                    size={16}
                    color={selectedModule.state === "done" ? "#059669" : "#94a3b8"}
                  />
                </div>
              </div>
            </div>
            <div className="app-modal-footer">
              <a
                href="https://igotkarmayogi.gov.in"
                target="_blank"
                rel="noreferrer"
                className="secondary-btn"
                style={{ textDecoration: "none" }}
              >
                <ExternalLink size={14} /> Open in iGOT Portal
              </a>
              <button
                className="primary-btn"
                onClick={() => {
                  const mod = selectedModule;
                  setSelectedModule(null);
                  if (onStartQuiz) {
                    onStartQuiz({
                      domain: mod.domain || "statisticalMethods",
                      title: mod.title,
                    });
                  }
                }}
              >
                <PlayCircle size={14} /> {tr(lang, "launchModuleQuiz")}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
