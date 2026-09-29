import React, { useState, useEffect } from "react";
import {
  Award,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  ExternalLink,
  GraduationCap,
  PlayCircle,
  Search,
  Sparkles,
  Target,
  TrendingUp,
  AlertCircle,
} from "lucide-react";
import {
  apiGetIgotCourses,
  apiGetIgotRecommendations,
  apiEnrollIgotCourse,
} from "./services/api/client.js";

export default function IgotHub({
  apiBaseUrl,
  apiToken = "",
  userCourses = [],
  criticalSkills = [],
  onEnrollSuccess,
}) {
  const [courses, setCourses] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDomain, setSelectedDomain] = useState("all");
  const [enrollingId, setEnrollingId] = useState(null);
  const [statusMessage, setStatusMessage] = useState(null);

  useEffect(() => {
    fetchIgotData();
  }, [apiToken]);

  const fetchIgotData = async () => {
    setLoading(true);
    try {
      // 1. Fetch catalog courses via centralized client
      const catData = await apiGetIgotCourses();
      setCourses(catData?.courses || []);

      // 2. Fetch personalized recommendations
      if (apiToken) {
        const recData = await apiGetIgotRecommendations(apiToken);
        setRecommendations(recData?.recommendations || []);
      }
    } catch (err) {
      console.warn("iGOT fetch warning:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async (course) => {
    setEnrollingId(course.id);
    setStatusMessage(null);
    try {
      const data = await apiEnrollIgotCourse(course.id, apiToken);
      setStatusMessage({
        type: "success",
        text: `Successfully registered training for '${course.title}'! 4 learning hours credited to your training pipeline.`,
      });
      if (onEnrollSuccess) {
        onEnrollSuccess(data.userPayload);
      }
      fetchIgotData();
    } catch (err) {
      setStatusMessage({
        type: "error",
        text: `Enrollment notice: ${err.message}`,
      });
    } finally {
      setEnrollingId(null);
    }
  };

  const enrolledCourseIds = new Set(userCourses.map((c) => c.id || c.title));

  const filteredCatalog = courses.filter((c) => {
    if (selectedDomain === "all") return true;
    return c.competency_domain === selectedDomain;
  });

  return (
    <div className="stack">
      {/* Header */}
      <div className="page-heading system-card">
        <div>
          <div className="kicker">STATISTICAL CAPACITY BUILDING · iGOT CURRICULUM CATALOG</div>
          <h1>iGOT Karmayogi Competency Pathways</h1>
          <p>
            Curated competency-linked training repository mapped to National Statistical System competency standards and NSSTA training modules.
          </p>
        </div>
        <a
          href="https://igotkarmayogi.gov.in"
          target="_blank"
          rel="noreferrer"
          className="secondary-btn"
          style={{ textDecoration: "none" }}
        >
          <ExternalLink size={14} /> Open Official iGOT Portal
        </a>
      </div>

      {statusMessage && (
        <div
          className="system-card"
          style={{
            borderColor: statusMessage.type === "success" ? "rgba(74, 222, 128, 0.4)" : "rgba(248, 113, 113, 0.4)",
            background: statusMessage.type === "success" ? "rgba(6, 78, 59, 0.25)" : "rgba(127, 29, 29, 0.25)",
            padding: "12px 18px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
          }}
        >
          {statusMessage.type === "success" ? (
            <CheckCircle2 size={18} color="#4ade80" />
          ) : (
            <AlertCircle size={18} color="#f87171" />
          )}
          <span style={{ fontSize: "0.95rem" }}>{statusMessage.text}</span>
        </div>
      )}

      {/* Dynamic Gap-Targeted Recommendations Banner */}
      <section className="system-card" style={{ borderColor: "rgba(102, 231, 255, 0.4)", background: "linear-gradient(180deg, rgba(8, 22, 42, 0.95), rgba(4, 12, 24, 0.95))" }}>
        <div className="card-header">
          <div>
            <div className="system-label" style={{ color: "#66e7ff" }}>
              <Sparkles size={14} style={{ display: "inline", verticalAlign: "middle", marginRight: 4 }} />
              DYNAMIC AI RECOMMENDATIONS
            </div>
            <h2>Curated Specifically to Bridge Your Competency Gaps</h2>
            <p style={{ margin: "4px 0 0", color: "#94a3b8", fontSize: "0.9rem" }}>
              Targeted upskilling derived from your latest assessment diagnostics.
            </p>
          </div>
          <span className="edu-badge bloom-application">{recommendations.length} Courses Prioritized</span>
        </div>

        <div className="igot-course-grid">
          {recommendations.slice(0, 3).map((course) => {
            const isEnrolled = enrolledCourseIds.has(course.id);
            return (
              <div className="igot-card" key={course.id}>
                <div>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
                    <span className="edu-badge cadre-nssta">{course.frac_competency_code || "FRAC-STAT"}</span>
                    <span style={{ fontSize: "0.82rem", color: "#ffc75d", fontWeight: 700 }}>
                      ★ {course.rating}
                    </span>
                  </div>
                  <div className="igot-card-badge">{course.provider}</div>
                  <h3>{course.title}</h3>
                  <div style={{ fontSize: "0.82rem", color: "#67e8f9", marginBottom: 8, fontWeight: 600 }}>
                    {course.reason_for_recommendation}
                  </div>
                  <ul className="igot-outcomes">
                    {(course.learning_outcomes || []).slice(0, 2).map((outcome, idx) => (
                      <li key={idx}>{outcome}</li>
                    ))}
                  </ul>
                </div>
                <div style={{ borderTop: "1px solid rgba(255,255,255,0.08)", paddingTop: 12, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ fontSize: "0.82rem", color: "#94a3b8" }}>{course.duration} · {course.level}</span>
                  <button
                    type="button"
                    className="primary-btn"
                    style={{ fontSize: "0.82rem", padding: "6px 14px" }}
                    disabled={isEnrolled || enrollingId === course.id}
                    onClick={() => handleEnroll(course)}
                  >
                    {isEnrolled ? (
                      <>
                        <CheckCircle2 size={13} color="#43e5ad" /> Enrolled
                      </>
                    ) : enrollingId === course.id ? (
                      "Enrolling..."
                    ) : (
                      <>
                        <PlayCircle size={13} /> Enroll & Sync
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Catalog Filter & Browser */}
      <section className="system-card">
        <div className="card-header">
          <div>
            <div className="system-label">NSSTA & MoSPI COURSE DIRECTORY</div>
            <h2>All Official Statistical Courses</h2>
          </div>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {[
              ["all", "All Domains"],
              ["statisticalMethods", "Sampling & Methods"],
              ["nationalAccounts", "National Accounts"],
              ["priceIndices", "Price Indices"],
              ["dataQuality", "Data Quality"],
              ["gisSpatial", "GIS & Spatial"],
              ["dataScienceAi", "Python & Data Tools"],
            ].map(([val, label]) => (
              <button
                key={val}
                type="button"
                className={`theme-option ${selectedDomain === val ? "active" : ""}`}
                style={{ fontSize: "0.82rem", padding: "6px 12px" }}
                onClick={() => setSelectedDomain(val)}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <div className="igot-course-grid">
          {filteredCatalog.map((course) => {
            const isEnrolled = enrolledCourseIds.has(course.id);
            return (
              <div className="igot-card" key={course.id}>
                <div>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
                    <span className="edu-badge cadre-nssta">{course.id}</span>
                    <span style={{ fontSize: "0.82rem", color: "#ffc75d", fontWeight: 700 }}>
                      ★ {course.rating}
                    </span>
                  </div>
                  <div className="igot-card-badge">{course.provider}</div>
                  <h3>{course.title}</h3>
                  <div style={{ fontSize: "0.8rem", color: "#94a3b8", marginBottom: 8 }}>
                    Target Cadre: {(course.target_cadres || []).join(", ")}
                  </div>
                  <ul className="igot-outcomes">
                    {(course.learning_outcomes || []).map((outcome, idx) => (
                      <li key={idx}>{outcome}</li>
                    ))}
                  </ul>
                </div>
                <div style={{ borderTop: "1px solid rgba(255,255,255,0.08)", paddingTop: 12, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ fontSize: "0.82rem", color: "#94a3b8" }}>{course.duration}</span>
                  <div style={{ display: "flex", gap: 8 }}>
                    <a
                      href={course.karmayogi_url}
                      target="_blank"
                      rel="noreferrer"
                      className="icon-btn"
                      title="Open on iGOT Karmayogi"
                    >
                      <ExternalLink size={14} />
                    </a>
                    <button
                      type="button"
                      className="primary-btn"
                      style={{ fontSize: "0.82rem", padding: "6px 14px" }}
                      disabled={isEnrolled || enrollingId === course.id}
                      onClick={() => handleEnroll(course)}
                    >
                      {isEnrolled ? "Enrolled" : enrollingId === course.id ? "..." : "Enroll"}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
