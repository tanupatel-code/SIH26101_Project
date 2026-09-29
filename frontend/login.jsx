import React, { useState, useEffect } from "react";
import {
  BarChart3,
  Eye,
  EyeOff,
  Lock,
  Mail,
  ArrowRight,
  UserPlus,
  ShieldCheck,
  GraduationCap,
  Building2,
  Sparkles,
  Activity,
  CheckCircle2,
  Database,
  Layers,
} from "lucide-react";
import "./login.css";
import "./auth-themes.css";

export default function Login({ onLogin, onRegister }) {
  useEffect(() => {
    // Default to clean executive light mode with crisp institutional background
    const theme = localStorage.getItem("statSkillVisualTheme") || "executive";
    const appearance = localStorage.getItem("statSkillAppearance") || "light";
    document.documentElement.dataset.themeMode = theme;
    document.documentElement.dataset.appearanceMode = appearance;
    document.body.classList.remove(
      "theme-solo",
      "theme-executive",
      "theme-aurora",
      "appearance-dark",
      "appearance-light"
    );
    document.body.classList.add(
      `theme-${theme === "pro" ? "executive" : theme}`,
      `appearance-${appearance}`
    );
  }, []);

  const [activePersona, setActivePersona] = useState("officer"); // "officer" or "general"
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isFilling, setIsFilling] = useState(false);

  const selectPersona = (persona) => {
    setActivePersona(persona);
  };

  const handleDemoFill = (type) => {
    setIsFilling(true);
    if (type === "officer") {
      setActivePersona("officer");
      setEmail("ananya.verma@demo.gov.in");
      setPassword("Demo@12345");
    } else {
      setActivePersona("general");
      setEmail("aarav.sharma@learner.in");
      setPassword("Learner@12345");
    }
    setTimeout(() => setIsFilling(false), 400);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      alert("Please enter both email and password.");
      return;
    }

    if (onLogin) {
      await onLogin({
        email,
        password,
        persona: activePersona,
      });
    }
  };

  return (
    <div className="login-page">
      {/* Institutional National Tricolor Ribbon at top */}
      <div className="gov-tricolor-bar" aria-hidden="true" />

      {/* Ambient background statistical geometric accents */}
      <div className="login-backdrop-elements" aria-hidden="true">
        <div className="ambient-radial-glow ambient-glow-left" />
        <div className="ambient-radial-glow ambient-glow-right" />
        <div className="ambient-grid-pattern" />
      </div>

      <div className="login-container">
        {/* LEFT BRAND & STATISTICAL INTELLIGENCE SECTION */}
        <div className="login-brand-section">
          {/* Top Emblem & Department Hierarchy */}
          <div className="gov-emblem-badge">
            <div className="emblem-lockup">
              <span className="gov-india-text">भारत सरकार | Government of India</span>
              <span className="gov-ministry-text">
                Ministry of Statistics & Programme Implementation (MoSPI)
              </span>
              <span className="gov-sub-text">
                National Statistical Systems Training Academy (NSSTA)
              </span>
            </div>
          </div>

          {/* Core Brand Header with Dynamic Iconography */}
          <div className="brand-hero-block">
            <div className="brand-mark-wrapper">
              <div className="brand-logo">
                <BarChart3 size={32} strokeWidth={2.4} />
              </div>
              <div className="brand-pulse-ring" />
            </div>

            <div className="brand-titles">
              <h1>StatSkill AI</h1>
              <p className="brand-subtitle">
                National Statistical Capacity & Competency Intelligence Platform
              </p>
            </div>
          </div>

          {/* Interactive Statistical Visual Element: Dynamic Radar/Constellation Graphic */}
          <div className="stats-visual-card" aria-hidden="true">
            <div className="stats-visual-header">
              <span className="visual-tag">
                <Activity size={13} className="pulse-icon" /> Official Statistical Framework (FRAC)
              </span>
              <span className="visual-metric">7 Core Domains</span>
            </div>

            <svg
              className="stats-constellation-svg"
              viewBox="0 0 380 150"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              {/* Subtle Grid / Reference Coordinate Lines */}
              <line x1="20" y1="75" x2="360" y2="75" stroke="rgba(255,255,255,0.08)" strokeDasharray="3 3" />
              <line x1="190" y1="15" x2="190" y2="135" stroke="rgba(255,255,255,0.08)" strokeDasharray="3 3" />

              {/* Connecting Constellation Vectors */}
              <path
                d="M 45,95 L 95,45 L 160,70 L 220,35 L 285,60 L 335,40"
                stroke="rgba(56, 189, 248, 0.45)"
                strokeWidth="1.8"
                strokeLinecap="round"
                className="animated-vector-path"
              />
              <path
                d="M 45,95 L 120,115 L 190,95 L 260,115 L 335,40"
                stroke="rgba(251, 191, 36, 0.35)"
                strokeWidth="1.4"
                strokeDasharray="4 4"
              />

              {/* Competency Domain Nodes */}
              <g className="node-group">
                <circle cx="45" cy="95" r="5" fill="#38bdf8" />
                <text x="45" y="112" fill="#94a3b8" fontSize="9" textAnchor="middle" fontWeight="600">
                  Sampling
                </text>
              </g>

              <g className="node-group">
                <circle cx="95" cy="45" r="6" fill="#60a5fa" />
                <circle cx="95" cy="45" r="9" stroke="rgba(96,165,250,0.4)" strokeWidth="1" />
                <text x="95" y="34" fill="#cbd5e1" fontSize="9" textAnchor="middle" fontWeight="600">
                  Macro (SNA)
                </text>
              </g>

              <g className="node-group">
                <circle cx="160" cy="70" r="5" fill="#f59e0b" />
                <text x="160" y="87" fill="#94a3b8" fontSize="9" textAnchor="middle" fontWeight="600">
                  CPI / WPI
                </text>
              </g>

              <g className="node-group">
                <circle cx="220" cy="35" r="6" fill="#10b981" />
                <circle cx="220" cy="35" r="9" stroke="rgba(16,185,129,0.4)" strokeWidth="1" />
                <text x="220" y="24" fill="#cbd5e1" fontSize="9" textAnchor="middle" fontWeight="600">
                  Data Quality
                </text>
              </g>

              <g className="node-group">
                <circle cx="285" cy="60" r="5" fill="#a855f7" />
                <text x="285" y="77" fill="#94a3b8" fontSize="9" textAnchor="middle" fontWeight="600">
                  GIS / Spatial
                </text>
              </g>

              <g className="node-group">
                <circle cx="335" cy="40" r="6" fill="#38bdf8" />
                <circle cx="335" cy="40" r="10" stroke="rgba(56,189,248,0.5)" strokeWidth="1" />
                <text x="335" y="28" fill="#e2e8f0" fontSize="9" textAnchor="middle" fontWeight="600">
                  Python & AI
                </text>
              </g>
            </svg>

            {/* Live Telemetry Pill Badges */}
            <div className="telemetry-badges-row">
              <span className="telemetry-pill">
                <Database size={11} /> Multi-Signal Diagnostic
              </span>
              <span className="telemetry-pill">
                <Layers size={11} /> iGOT Karmayogi Synced
              </span>
              <span className="telemetry-pill">
                <CheckCircle2 size={11} /> Server Authoritative
              </span>
            </div>
          </div>

          {/* Active Persona Context Card */}
          <div className="persona-benefits">
            <div className={`benefit-chip ${activePersona === "officer" ? "active" : ""}`}>
              <div className="benefit-icon-box officer-icon">
                <ShieldCheck size={20} />
              </div>
              <div className="benefit-text">
                <div className="benefit-heading">
                  <strong>Statistical Cadres & Officers</strong>
                  <span className="cadre-tag">MoSPI / SSS / ISS</span>
                </div>
                <p>
                  Diagnostic skill gap auditing, official FRAC benchmark comparison, and
                  NSSTA-accredited iGOT Karmayogi learning assignments.
                </p>
              </div>
            </div>

            <div className={`benefit-chip ${activePersona === "general" ? "active" : ""}`}>
              <div className="benefit-icon-box scholar-icon">
                <GraduationCap size={20} />
              </div>
              <div className="benefit-text">
                <div className="benefit-heading">
                  <strong>Researchers, Scholars & Citizens</strong>
                  <span className="cadre-tag scholar">Open Access</span>
                </div>
                <p>
                  Explore official national statistical methodologies, practice with survey
                  guidelines, and benchmark personal data science capabilities.
                </p>
              </div>
            </div>
          </div>

          {/* Institutional Integrity & Accreditation Footnote */}
          <div className="brand-info">
            <span className="brand-info-item">National Statistical Learning Initiative</span>
            <span className="info-sep">•</span>
            <span className="brand-info-item">MoSPI & NSSTA Standards</span>
            <span className="info-sep">•</span>
            <span className="brand-info-item">Mission Karmayogi</span>
          </div>
        </div>

        {/* RIGHT CARD / AUTHENTICATION INTERACTION SECTION */}
        <div className="login-card">
          <div className="login-header">
            <div className="login-header-pretitle">Secure Access Portal</div>
            <h2>Portal Sign In</h2>
            <p>Select your user category to load your personalized competency workspace</p>
          </div>

          {/* DUAL PERSONA SELECTOR TABS */}
          <div className="persona-tabs" role="tablist" aria-label="User Category Selector">
            <button
              type="button"
              role="tab"
              aria-selected={activePersona === "officer"}
              className={`persona-tab ${activePersona === "officer" ? "active" : ""}`}
              onClick={() => selectPersona("officer")}
            >
              <Building2 size={18} />
              <div className="persona-tab-text">
                <strong>Government Officer</strong>
                <span>MoSPI / SSS / Cadre</span>
              </div>
            </button>

            <button
              type="button"
              role="tab"
              aria-selected={activePersona === "general"}
              className={`persona-tab ${activePersona === "general" ? "active" : ""}`}
              onClick={() => selectPersona("general")}
            >
              <GraduationCap size={18} />
              <div className="persona-tab-text">
                <strong>General Learner</strong>
                <span>Student / Scholar / Public</span>
              </div>
            </button>
          </div>

          {/* INTERACTIVE DEMO PRESETS */}
          <div className="quick-demo-box">
            <div className="demo-hint-title">
              <Sparkles size={14} className="sparkle-gold" />
              <span>Instant Demonstration Profiles (One-Click Fill):</span>
            </div>
            <div className="demo-pill-row">
              <button
                type="button"
                className={`demo-card-preset ${activePersona === "officer" ? "active" : ""} ${
                  isFilling && activePersona === "officer" ? "filling" : ""
                }`}
                onClick={() => handleDemoFill("officer")}
                title="Fill demo credentials for Statistical Officer Ananya Verma"
              >
                <div className="preset-avatar officer-avatar">AV</div>
                <div className="preset-info">
                  <span className="preset-name">Ananya Verma</span>
                  <span className="preset-role">Senior Statistical Officer · MoSPI</span>
                </div>
              </button>

              <button
                type="button"
                className={`demo-card-preset ${activePersona === "general" ? "active" : ""} ${
                  isFilling && activePersona === "general" ? "filling" : ""
                }`}
                onClick={() => handleDemoFill("general")}
                title="Fill demo credentials for Citizen Scholar Aarav Sharma"
              >
                <div className="preset-avatar scholar-avatar">AS</div>
                <div className="preset-info">
                  <span className="preset-name">Aarav Sharma</span>
                  <span className="preset-role">Citizen Data Science Scholar</span>
                </div>
              </button>
            </div>
          </div>

          {/* SIGN IN FORM */}
          <form onSubmit={handleSubmit} className="login-form-body">
            {/* EMAIL INPUT */}
            <div className="login-field">
              <label htmlFor="email">
                {activePersona === "officer"
                  ? "Government / Ministry Email Address"
                  : "Institutional / Personal Email Address"}
              </label>
              <div className="input-wrapper">
                <Mail size={18} className="field-icon" />
                <input
                  id="email"
                  type="email"
                  placeholder={
                    activePersona === "officer"
                      ? "ananya.verma@demo.gov.in"
                      : "aarav.sharma@learner.in"
                  }
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="username"
                  required
                />
              </div>
            </div>

            {/* PASSWORD INPUT */}
            <div className="login-field">
              <div className="password-label">
                <label htmlFor="password">Security Password</label>
                <button
                  type="button"
                  className="forgot-password"
                  onClick={() =>
                    alert("Password recovery: Please contact your designated MoSPI / NSSTA portal administrator.")
                  }
                >
                  Forgot Password?
                </button>
              </div>

              <div className="input-wrapper">
                <Lock size={18} className="field-icon" />
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your confidential password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? "Hide password text" : "Show password text"}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* WORKSTATION REMEMBER TOGGLE */}
            <div className="login-options">
              <label className="remember-me">
                <input type="checkbox" defaultChecked />
                <span>Keep session persistent on this verified workstation</span>
              </label>
            </div>

            {/* PRIMARY SUBMIT BUTTON */}
            <button type="submit" className="login-button">
              <span>
                {activePersona === "officer"
                  ? "Access Official Cadre Workspace"
                  : "Access Public Learning Workspace"}
              </span>
              <ArrowRight size={18} className="button-arrow" />
            </button>
          </form>

          {/* REGISTRATION REDIRECTION */}
          <div className="register-section">
            <span className="register-prompt">New to the National Statistical Learning Platform?</span>
            <button
              type="button"
              className="register-button"
              onClick={onRegister}
            >
              <UserPlus size={16} />
              <span>Create New Account (Cadre Officer or Public Citizen)</span>
            </button>
          </div>

          {/* COMPLIANCE & SECURITY FOOTER */}
          <div className="login-footer">
            <div className="security-guarantee">
              <ShieldCheck size={13} className="text-emerald" />
              <span>256-Bit TLS Secured · ISO 32000-1 Verification · WCAG 2.1 Compliant</span>
            </div>
            <div className="compliance-meta">
              <span>StatSkill AI Platform</span>
              <span className="dot-sep">•</span>
              <span>MoSPI Official Statistical Learning Framework</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}