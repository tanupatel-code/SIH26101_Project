import React, { useState, useEffect } from "react";
import {
  Award,
  CheckCircle2,
  ChevronRight,
  Clock,
  HelpCircle,
  RotateCcw,
  Sparkles,
  TrendingUp,
  X,
  XCircle,
} from "lucide-react";

export default function QuizPlayer({
  quizId = "QUIZ-GENERAL",
  title = "Statistical Competency Assessment",
  domain = "statisticalMethods",
  domainName = "Statistical Methods & Sampling",
  questions = [],
  apiBaseUrl = (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_BASE_URL ? import.meta.env.VITE_API_BASE_URL.replace(/\/$/, "") : "http://localhost:8000"),
  apiToken = "",
  onClose,
  onCompleted,
}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({}); // { [questionIdx]: selectedOptionIdx }
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [results, setResults] = useState(null);
  const [timeLeft, setTimeLeft] = useState(15 * 60); // 15 minutes timer

  // Countdown timer
  useEffect(() => {
    if (submitted) return;
    const timer = setInterval(() => {
      setTimeLeft((t) => (t > 0 ? t - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, [submitted]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const currentQ = questions[currentIndex] || {};
  const totalQ = questions.length;
  const answeredCount = Object.keys(selectedAnswers).length;

  const handleSelectOption = (optIndex) => {
    if (submitted) return;
    setSelectedAnswers({
      ...selectedAnswers,
      [currentIndex]: optIndex,
    });
  };

  const handleSubmit = async () => {
    if (answeredCount < totalQ) {
      const confirmSubmit = window.confirm(
        `You have answered ${answeredCount} of ${totalQ} questions. Submit anyway?`
      );
      if (!confirmSubmit) return;
    }

    setSubmitting(true);
    try {
      const answersPayload = questions.map((q, idx) => {
        const selected = selectedAnswers[idx] ?? -1;
        const isCorrect = selected === q.correct_index;
        return {
          question_id: q.id || `Q-${idx + 1}`,
          selected_option: selected,
          correct_option: q.correct_index,
          is_correct: isCorrect,
        };
      });

      const response = await fetch(`${apiBaseUrl}/api/assessments/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiToken}`,
        },
        body: JSON.stringify({
          quiz_id: quizId,
          title: title,
          domain: domain,
          answers: answersPayload,
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to submit assessment.");
      }

      setResults(data);
      setSubmitted(true);
      if (onCompleted) {
        onCompleted(data);
      }
    } catch (err) {
      alert(`Error submitting quiz: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  if (totalQ === 0) {
    return (
      <div className="quiz-overlay">
        <div className="quiz-container" style={{ padding: 32, textAlign: "center" }}>
          <h3>No Questions Available</h3>
          <p>Please check your parameters or upload learning materials to generate a quiz.</p>
          <button className="primary-btn" onClick={onClose} style={{ marginTop: 16 }}>
            Close
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="quiz-overlay">
      <div className="quiz-container">
        {/* Header */}
        <div className="quiz-header">
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span className="edu-badge cadre-nssta">{domainName}</span>
              {currentQ.bloom_level && (
                <span className={`edu-badge bloom-${currentQ.bloom_level.toLowerCase()}`}>
                  Bloom: {currentQ.bloom_level}
                </span>
              )}
            </div>
            <h2 style={{ fontSize: "1.1rem", margin: "6px 0 0", color: "#f8fafc" }}>{title}</h2>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            {!submitted && (
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                  color: timeLeft < 120 ? "#ff637d" : "#66e7ff",
                  fontWeight: 600,
                  fontSize: "0.9rem",
                }}
              >
                <Clock size={16} />
                <span>{formatTime(timeLeft)}</span>
              </div>
            )}
            <button className="icon-btn" onClick={onClose} title="Exit Quiz">
              <X size={18} />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="quiz-body">
          {!submitted ? (
            <div>
              {/* Progress counter */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  fontSize: "0.85rem",
                  color: "#94a3b8",
                  marginBottom: 12,
                }}
              >
                <span>
                  Question {currentIndex + 1} of {totalQ}
                </span>
                <span>
                  Answered: {answeredCount} / {totalQ}
                </span>
              </div>

              {/* Question Statement */}
              <div className="quiz-question-box">
                <div className="quiz-question-text">{currentQ.question}</div>
              </div>

              {/* Options List */}
              <div className="quiz-options-list">
                {(currentQ.options || []).map((opt, optIdx) => {
                  const letter = ["A", "B", "C", "D"][optIdx] || optIdx;
                  const isSelected = selectedAnswers[currentIndex] === optIdx;
                  return (
                    <button
                      key={optIdx}
                      type="button"
                      className={`quiz-option-btn ${isSelected ? "selected" : ""}`}
                      onClick={() => handleSelectOption(optIdx)}
                    >
                      <span className="quiz-option-letter">{letter}</span>
                      <span>{opt}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          ) : (
            /* Results & Review Scorecard */
            <div>
              <div className="scorecard-header">
                <div className="scorecard-circle">
                  <strong>{Math.round(results?.score ?? 0)}%</strong>
                  <span>Score</span>
                </div>
                <h2 style={{ margin: "4px 0 8px", color: "#f8fafc" }}>
                  {results?.score >= 70 ? "Competency Benchmark Met!" : "Targeted Upskilling Advised"}
                </h2>
                <p style={{ color: "#94a3b8", fontSize: "0.9rem", margin: 0 }}>
                  You answered {results?.correctCount ?? 0} out of {results?.totalQuestions ?? totalQ} questions correctly.
                </p>
              </div>

              {/* Closed-loop dynamic feedback message */}
              <div className="scorecard-feedback-banner">
                <TrendingUp size={22} color="#43e5ad" />
                <div style={{ fontSize: "0.9rem", color: "#e2e8f0" }}>
                  <strong>Competency Recalculated:</strong> Your dynamic profile has been updated!
                  {results?.updatedCompetencyScore && (
                    <span> Current {domainName} score is now <b>{results.updatedCompetencyScore.toFixed(2)}/5.00</b>.</span>
                  )}
                  {" "}Recommended iGOT Karmayogi modules have been tuned to your remaining gaps.
                </div>
              </div>

              {/* Detailed Question Review & Rationale */}
              <h3 style={{ fontSize: "1rem", color: "#cbd5e1", marginTop: 24, marginBottom: 12 }}>
                Question-by-Question Diagnostic Review:
              </h3>
              {questions.map((q, idx) => {
                const userAns = selectedAnswers[idx];
                const isCorrect = userAns === q.correct_index;
                const letter = ["A", "B", "C", "D"];
                return (
                  <div
                    key={idx}
                    className={`review-item ${isCorrect ? "correct" : "incorrect"}`}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                      <strong style={{ fontSize: "0.92rem", color: "#f1f5f9" }}>
                        Question {idx + 1}: {q.question}
                      </strong>
                      <span style={{ fontSize: "0.82rem", fontWeight: 700, color: isCorrect ? "#43e5ad" : "#ff637d" }}>
                        {isCorrect ? "CORRECT (+1)" : "INCORRECT"}
                      </span>
                    </div>
                    <div style={{ fontSize: "0.85rem", color: "#94a3b8", margin: "4px 0" }}>
                      Your Answer: <b>{userAns !== undefined && userAns !== -1 ? `${letter[userAns]}: ${q.options[userAns]}` : "Not Answered"}</b>
                    </div>
                    {!isCorrect && (
                      <div style={{ fontSize: "0.85rem", color: "#43e5ad", margin: "4px 0" }}>
                        Correct Answer: <b>{letter[q.correct_index]}: {q.options[q.correct_index]}</b>
                      </div>
                    )}
                    {q.explanation && (
                      <div className="review-explanation">
                        <span style={{ fontWeight: 600, color: "#66e7ff" }}>Educational Rationale: </span>
                        {q.explanation}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer Navigation */}
        <div className="quiz-footer">
          {!submitted ? (
            <>
              <button
                type="button"
                className="secondary-btn"
                disabled={currentIndex === 0}
                onClick={() => setCurrentIndex((i) => Math.max(0, i - 1))}
              >
                Previous
              </button>

              <div style={{ display: "flex", gap: 10 }}>
                {currentIndex < totalQ - 1 ? (
                  <button
                    type="button"
                    className="primary-btn"
                    onClick={() => setCurrentIndex((i) => Math.min(totalQ - 1, i + 1))}
                  >
                    Next Question <ChevronRight size={14} />
                  </button>
                ) : (
                  <button
                    type="button"
                    className="primary-btn"
                    style={{ background: "#43e5ad", color: "#02070f" }}
                    disabled={submitting}
                    onClick={handleSubmit}
                  >
                    {submitting ? "Grading..." : "Submit Assessment"} <CheckCircle2 size={14} />
                  </button>
                )}
              </div>
            </>
          ) : (
            <div style={{ display: "flex", justifyContent: "flex-end", width: "100%" }}>
              <button
                type="button"
                className="primary-btn"
                onClick={onClose}
              >
                Return to Dashboard
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
