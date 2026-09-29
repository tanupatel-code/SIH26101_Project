import React, { useState } from "react";
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
} from "lucide-react";
import "./login.css";
import "./auth-themes.css";

export default function Login({ onLogin, onRegister }) {
  React.useEffect(() => {
    // Default to clean executive light mode with crisp white background
    const theme = localStorage.getItem("statSkillVisualTheme") || "executive";
    const appearance = localStorage.getItem("statSkillAppearance") || "light";
    document.documentElement.dataset.themeMode = theme;
    document.documentElement.dataset.appearanceMode = appearance;
    document.body.classList.remove("theme-solo", "theme-executive", "theme-aurora", "appearance-dark", "appearance-light");
    document.body.classList.add(`theme-${theme === "pro" ? "executive" : theme}`, `appearance-${appearance}`);
  }, []);

  const [activePersona, setActivePersona] = useState("officer"); // "officer" or "general"
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const selectPersona = (persona) => {
    setActivePersona(persona);
  };

  const handleDemoFill = (type) => {
    if (type === "officer") {
      setActivePersona("officer");
      setEmail("ananya.verma@demo.gov.in");
      setPassword("Demo@12345");
    } else {
      setActivePersona("general");
      setEmail("aarav.sharma@learner.in");
      setPassword("Learner@12345");
    }
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
      {/* Subtle National Tricolor Ribbon at top */}
      <div className="gov-tricolor-bar"></div>

      <div className="login-container">
        {/* LEFT BRAND SECTION */}
        <div className="login-brand-section">
          <div className="gov-emblem-badge">
            <span className="gov-india-text">भारत सरकार | Government of India</span>
            <span className="gov-ministry-text">Ministry of Statistics & Programme Implementation</span>
          </div>

          <div className="brand-logo">
            <BarChart3 size={32} />
          </div>

          <h1>StatSkill AI</h1>
          <p className="brand-subtitle">
            National Statistical Capacity & Competency Intelligence Platform
          </p>

          <div className="brand-description">
            <p>
              An intelligent, closed-loop diagnostic and learning ecosystem empowering both
              <strong> Official Statistical Cadres (MoSPI / NSSTA)</strong> and
              <strong> General Learners, Researchers & Citizens</strong> to master India's Official Statistical Frameworks.
            </p>
          </div>

          <div className="persona-benefits">
            <div className={`benefit-chip ${activePersona === "officer" ? "active" : ""}`}>
              <ShieldCheck size={16} />
              <div>
                <strong>Statistical Cadres & Officers</strong>
                <span>Official FRAC competency tracking, gap diagnosis & iGOT NSSTA modules</span>
              </div>
            </div>
            <div className={`benefit-chip ${activePersona === "general" ? "active" : ""}`}>
              <GraduationCap size={16} />
              <div>
                <strong>General Public & Research Scholars</strong>
                <span>Open learning pathways, diagnostic quizzes & survey manual studies</span>
              </div>
            </div>
          </div>

          <div className="brand-info">
            <span>Problem Statement ID: 26101</span>
            <span>•</span>
            <span>MoSPI & NSSTA</span>
            <span>•</span>
            <span>Mission Karmayogi</span>
          </div>
        </div>

        {/* RIGHT CARD SECTION */}
        <div className="login-card">
          <div className="login-header">
            <h2>Portal Sign In</h2>
            <p>Select your user profile type to access your personalized learning workspace</p>
          </div>

          {/* DUAL PERSONA SELECTOR TABS */}
          <div className="persona-tabs">
            <button
              type="button"
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
              className={`persona-tab ${activePersona === "general" ? "active" : ""}`}
              onClick={() => selectPersona("general")}
            >
              <GraduationCap size={18} />
              <div className="persona-tab-text">
                <strong>General Learner</strong>
                <span>Student / Researcher / Public</span>
              </div>
            </button>
          </div>

          {/* QUICK DEMO PRESET BUTTONS */}
          <div className="quick-demo-box">
            <span className="demo-hint-title">
              <Sparkles size={14} /> Quick Demonstration Accounts:
            </span>
            <div className="demo-pill-row">
              <button
                type="button"
                className={`demo-pill ${activePersona === "officer" ? "active" : ""}`}
                onClick={() => handleDemoFill("officer")}
              >
                Officer: Ananya Verma (SSO)
              </button>
              <button
                type="button"
                className={`demo-pill ${activePersona === "general" ? "active" : ""}`}
                onClick={() => handleDemoFill("general")}
              >
                General: Aarav Sharma (Scholar)
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            {/* EMAIL */}
            <div className="login-field">
              <label htmlFor="email">
                {activePersona === "officer" ? "Government Email Address" : "Email Address"}
              </label>
              <div className="input-wrapper">
                <Mail size={18} />
                <input
                  id="email"
                  type="email"
                  placeholder={
                    activePersona === "officer"
                      ? "officer.name@mospi.gov.in"
                      : "learner@university.ac.in"
                  }
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* PASSWORD */}
            <div className="login-field">
              <div className="password-label">
                <label htmlFor="password">Password</label>
                <button
                  type="button"
                  className="forgot-password"
                  onClick={() => alert("Password reset functionality: Please contact system administrator.")}
                >
                  Forgot Password?
                </button>
              </div>

              <div className="input-wrapper">
                <Lock size={18} />
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label="Toggle password visibility"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* REMEMBER ME & ROLE NOTICE */}
            <div className="login-options">
              <label className="remember-me">
                <input type="checkbox" defaultChecked />
                <span>Keep me signed in on this workstation</span>
              </label>
            </div>

            {/* LOGIN BUTTON */}
            <button type="submit" className="login-button">
              <span>
                {activePersona === "officer"
                  ? "Access Official Cadre Portal"
                  : "Access Public Learning Workspace"}
              </span>
              <ArrowRight size={18} />
            </button>
          </form>

          {/* REGISTER */}
          <div className="register-section">
            <span>New to the National Statistical Learning Platform?</span>
            <button
              type="button"
              className="register-button"
              onClick={onRegister}
            >
              <UserPlus size={16} />
              Register Account (Officer or General Citizen)
            </button>
          </div>

          <div className="login-footer">
            <span>StatSkill AI</span>
            <span>•</span>
            <span>MoSPI National Statistical Learning Framework</span>
            <span>•</span>
            <span>NIC Standards Compliant</span>
          </div>
        </div>
      </div>
    </div>
  );
}