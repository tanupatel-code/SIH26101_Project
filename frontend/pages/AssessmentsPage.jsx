import React, { useState } from "react";
import {
  CheckCircle2,
  ChevronRight,
  ClipboardList,
  RotateCcw,
  Target,
  X,
} from "lucide-react";
import { tr } from "../i18n/index.js";
import {
  PageHeading,
  Pill,
  StatCard,
  SystemCard,
} from "../components/common/index.js";

export default function AssessmentsPage({ lang, data = {}, engine = {}, onStartQuiz }) {
  const [selectedAssessment, setSelectedAssessment] = useState(null);

  const assessments = data?.assessments || [];
  const averageScore = engine?.assessmentAverage || 0;
  const assignments = data?.assignments || [];
  const courses = data?.courses || [];

  return (
    <div className="stack">
      <PageHeading
        kicker={tr(lang, "assessmentControl").toUpperCase()}
        title={tr(lang, "assessments")}
        subtitle={`${assessments.length} assessment records for ${data?.profile?.name || "this user"}`}
      />

      <div className="stats-grid three">
        <StatCard
          label={tr(lang, "completed")}
          value={engine?.assessmentsCompleted ?? 0}
          suffix={`/${engine?.assessmentsTotal ?? assessments.length}`}
          meta="Recorded scored assessments"
          color="green"
          icon={CheckCircle2}
        />
        <StatCard
          label={tr(lang, "score")}
          value={averageScore}
          suffix="%"
          meta="Average across assessments"
          color="cyan"
          icon={Target}
        />
        <StatCard
          label="Assignments"
          value={engine?.assignmentsCompleted ?? 0}
          suffix={`/${engine?.assignmentsTotal ?? assignments.length}`}
          meta="Completed assignments"
          color="purple"
          icon={ClipboardList}
        />
      </div>

      <SystemCard>
        <div className="card-header">
          <div>
            <div className="system-label">{tr(lang, "upcomingQueue")}</div>
            <h2>{tr(lang, "nextCheckpoints")}</h2>
          </div>
        </div>
        <div className="assessment-list large">
          {assessments.map((a, i) => (
            <div
              className={`assessment ${["blue", "amber", "green", "purple", "red"][i % 5]}`}
              key={a.id || a.title || i}
            >
              <div className="assessment-number">0{i + 1}</div>
              <div className="grow">
                <strong>{a.title || "Assessment"}</strong>
                <span>
                  {a.domain || "—"} · Score {Number(a.score ?? 0)}% ·{" "}
                  {a.status || "Recorded"}
                </span>
              </div>
              <button
                className="secondary-btn"
                onClick={() => setSelectedAssessment(a)}
              >
                {tr(lang, "openDetails")} <ChevronRight size={14} />
              </button>
            </div>
          ))}
        </div>
      </SystemCard>

      <SystemCard>
        <div className="card-header">
          <div>
            <div className="system-label">ASSIGNMENTS</div>
            <h2>Assignment Records</h2>
          </div>
        </div>
        <div className="assessment-list large">
          {assignments.map((a, i) => (
            <div
              className={`assessment ${["blue", "amber", "green", "purple", "red"][i % 5]}`}
              key={a.id || i}
            >
              <div className="assessment-number">0{i + 1}</div>
              <div className="grow">
                <strong>{a.title || "Assignment"}</strong>
                <span>
                  {a.domain || "—"} · {Number(a.score ?? 0)}/
                  {Number(a.maxScore ?? 100)} · {a.status || "Recorded"} ·{" "}
                  {a.dueDate || "—"}
                </span>
              </div>
              <Pill
                tone={
                  String(a.status || "").toLowerCase() === "completed"
                    ? "strong"
                    : "active"
                }
              >
                {a.status || "Recorded"}
              </Pill>
            </div>
          ))}
        </div>
      </SystemCard>

      <SystemCard>
        <div className="card-header">
          <div>
            <div className="system-label">COURSES</div>
            <h2>Course Performance</h2>
          </div>
          <Pill>{courses.length}</Pill>
        </div>
        <div className="assessment-list large">
          {courses.map((c, i) => (
            <div
              className={`assessment ${["blue", "amber", "green", "purple", "red"][i % 5]}`}
              key={c.id || i}
            >
              <div className="assessment-number">0{i + 1}</div>
              <div className="grow">
                <strong>{c.title || "Course"}</strong>
                <span>
                  {c.domain || "—"} · Score {Number(c.score ?? 0)}% ·{" "}
                  {c.progress ?? 0}% progress · {c.hours ?? 0} hrs
                </span>
              </div>
              <Pill
                tone={
                  String(c.status || "").toLowerCase() === "completed"
                    ? "strong"
                    : "active"
                }
              >
                {c.status || "Recorded"}
              </Pill>
            </div>
          ))}
        </div>
      </SystemCard>

      {selectedAssessment && (
        <div
          className="app-modal-overlay"
          onClick={() => setSelectedAssessment(null)}
          role="dialog"
          aria-modal="true"
        >
          <div className="app-modal-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="app-modal-header">
              <div>
                <div className="system-label" style={{ color: "#0f2e5a" }}>
                  DIAGNOSTIC ASSESSMENT · {selectedAssessment.id || "ASM-RECORD"}
                </div>
                <h3>{selectedAssessment.title}</h3>
                <p>Domain: {selectedAssessment.domain || "Official Statistics"}</p>
              </div>
              <button
                className="icon-btn"
                onClick={() => setSelectedAssessment(null)}
                aria-label="Close"
              >
                <X size={16} />
              </button>
            </div>
            <div className="app-modal-body">
              <div className="credential-meta-grid">
                <div className="credential-meta-item">
                  <span>Domain Focus</span>
                  <strong>
                    {selectedAssessment.domain || "Statistical Methodology"}
                  </strong>
                </div>
                <div className="credential-meta-item">
                  <span>Achieved Score</span>
                  <strong
                    style={{
                      color:
                        Number(selectedAssessment.score ?? 0) >= 75
                          ? "#166534"
                          : "#b45309",
                    }}
                  >
                    {Number(selectedAssessment.score ?? 0)}%
                  </strong>
                </div>
                <div className="credential-meta-item">
                  <span>Evaluation Status</span>
                  <strong>
                    {Number(selectedAssessment.score ?? 0) >= 75
                      ? "Benchmark Met (Proficient)"
                      : "Targeted Upskilling Required"}
                  </strong>
                </div>
                <div className="credential-meta-item">
                  <span>Bloom's Taxonomy Level</span>
                  <strong>Application & Analysis</strong>
                </div>
              </div>

              <div className="credential-hash-box">
                <span>Diagnostic Assessment Recommendation</span>
                <p
                  style={{
                    margin: "4px 0 0",
                    fontSize: "0.85rem",
                    color: "#334155",
                    lineHeight: 1.5,
                  }}
                >
                  {Number(selectedAssessment.score ?? 0) >= 75
                    ? "Performance demonstrates solid mastery of survey sampling and validation protocols. Recommended to maintain proficiency via advanced case studies."
                    : "Score indicates room for improvement in foundational concepts. Complete the recommended iGOT Karmayogi modules and retake this diagnostic quiz."}
                </p>
              </div>
            </div>
            <div className="app-modal-footer">
              <button
                className="secondary-btn"
                onClick={() => setSelectedAssessment(null)}
              >
                Close
              </button>
              <button
                className="primary-btn"
                onClick={() => {
                  const asm = selectedAssessment;
                  setSelectedAssessment(null);
                  if (onStartQuiz) {
                    onStartQuiz({
                      domain: asm.domain || "statisticalMethods",
                      title: asm.title,
                    });
                  }
                }}
              >
                <RotateCcw size={14} /> Retake Diagnostic Quiz
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
