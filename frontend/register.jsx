import React, { useState } from "react";
import {
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
  BarChart3,
  UserPlus,
  Building2,
  GraduationCap,
  ShieldCheck,
} from "lucide-react";
import "./register.css";
import "./auth-themes.css";

export default function Register({ onRegister, onBackToLogin }) {
  React.useEffect(() => {
    const theme = localStorage.getItem("statSkillVisualTheme") || "executive";
    const appearance = localStorage.getItem("statSkillAppearance") || "light";
    document.documentElement.dataset.themeMode = theme;
    document.documentElement.dataset.appearanceMode = appearance;
    document.body.classList.remove("theme-solo", "theme-executive", "theme-aurora", "appearance-dark", "appearance-light");
    document.body.classList.add(`theme-${theme === "pro" ? "executive" : theme}`, `appearance-${appearance}`);
  }, []);

  const [accountType, setAccountType] = useState("officer"); // "officer" or "general"
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "Junior Statistical Officer (JSO)",
    department: "MoSPI",
    accountType: "officer",
  });

  const handleAccountTypeChange = (type) => {
    setAccountType(type);
    if (type === "officer") {
      setFormData((prev) => ({
        ...prev,
        accountType: "officer",
        role: "Junior Statistical Officer (JSO)",
        department: "MoSPI",
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        accountType: "general",
        role: "Citizen Data Analyst & Research Scholar",
        department: "University / Public Research",
      }));
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
      alert("Please fill all required fields.");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    if (formData.password.length < 6) {
      alert("Password must be at least 6 characters.");
      return;
    }

    if (onRegister) {
      onRegister({
        ...formData,
        role: formData.role || (accountType === "officer" ? "Junior Statistical Officer (JSO)" : "Citizen Data Analyst & Research Scholar"),
        department: formData.department || (accountType === "officer" ? "MoSPI" : "Public"),
        projectId: accountType === "officer" ? "SIH26101" : "PUBLIC-LEARNER",
      });
    }
  };

  return (
    <div className="register-page">
      <div className="gov-tricolor-bar"></div>

      {/* LEFT BRANDING SECTION */}
      <div className="register-brand">
        <div className="register-brand-lockup">
          <div className="gov-emblem-badge">
            <span className="gov-india-text">भारत सरकार | Government of India</span>
            <span className="gov-ministry-text">Ministry of Statistics & Programme Implementation</span>
          </div>

          <div className="register-brand-icon">
            <BarChart3 size={32} />
          </div>

          <div className="register-brand-content">
            <h1>StatSkill AI</h1>
            <p className="register-tagline">
              National Statistical Capacity & Competency Portal
            </p>

            <p className="register-description">
              Create your official account to access personalized competency gap diagnostics,
              accredited iGOT Karmayogi modules, and AI-assisted multiple choice assessments
              derived directly from India's official statistical manuals.
            </p>

            <div className="register-benefits-list">
              <div className="reg-benefit-item">
                <ShieldCheck size={18} />
                <span>MoSPI / NSSTA FRAC-accredited competency benchmarking</span>
              </div>
              <div className="reg-benefit-item">
                <GraduationCap size={18} />
                <span>Public citizen analytics track & university research pathways</span>
              </div>
            </div>

            <div className="register-project">
              SIH Problem Statement 26101
              <span>•</span>
              MoSPI & NSSTA
            </div>
          </div>
        </div>
      </div>

      {/* RIGHT REGISTRATION SECTION */}
      <div className="register-form-section">
        <div className="register-form-container">
          <div className="register-heading">
            <h2>Create Account</h2>
            <p>Select your user category to configure your custom learning curriculum</p>
          </div>

          {/* ACCOUNT TYPE SELECTION TABS */}
          <div className="register-persona-tabs">
            <button
              type="button"
              className={`reg-tab ${accountType === "officer" ? "active" : ""}`}
              onClick={() => handleAccountTypeChange("officer")}
            >
              <Building2 size={18} />
              <div>
                <strong>Statistical Cadre Officer</strong>
                <span>MoSPI / Central / State Govt</span>
              </div>
            </button>

            <button
              type="button"
              className={`reg-tab ${accountType === "general" ? "active" : ""}`}
              onClick={() => handleAccountTypeChange("general")}
            >
              <GraduationCap size={18} />
              <div>
                <strong>General Learner</strong>
                <span>Student / Scholar / Citizen</span>
              </div>
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {/* FULL NAME */}
            <div className="register-field">
              <label>Full Name *</label>
              <div className="register-input-wrapper">
                <User size={18} className="register-input-icon" />
                <input
                  type="text"
                  name="name"
                  placeholder="e.g. Dr. Ramesh Kumar"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            {/* EMAIL */}
            <div className="register-field">
              <label>
                {accountType === "officer" ? "Official Government Email *" : "Email Address *"}
              </label>
              <div className="register-input-wrapper">
                <Mail size={18} className="register-input-icon" />
                <input
                  type="email"
                  name="email"
                  placeholder={
                    accountType === "officer"
                      ? "officer.name@mospi.gov.in"
                      : "student@university.ac.in"
                  }
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            {/* ROLE / DESIGNATION */}
            <div className="register-field">
              <label>
                {accountType === "officer" ? "Cadre Designation / Post" : "Learner Category / Role"}
              </label>
              <div className="register-input-wrapper">
                {accountType === "officer" ? (
                  <select
                    name="role"
                    value={formData.role}
                    onChange={handleChange}
                    className="register-select"
                  >
                    <option value="Junior Statistical Officer (JSO)">Junior Statistical Officer (JSO)</option>
                    <option value="Senior Statistical Officer (SSO)">Senior Statistical Officer (SSO)</option>
                    <option value="Statistical Investigator Grade-I">Statistical Investigator Grade-I</option>
                    <option value="Statistical Investigator Grade-II">Statistical Investigator Grade-II</option>
                    <option value="Assistant Director (ISS)">Assistant Director (ISS)</option>
                    <option value="Deputy Director / Director">Deputy Director / Director</option>
                  </select>
                ) : (
                  <select
                    name="role"
                    value={formData.role}
                    onChange={handleChange}
                    className="register-select"
                  >
                    <option value="Citizen Data Analyst & Research Scholar">Citizen Data Analyst & Research Scholar</option>
                    <option value="University Student / Post-Graduate">University Student / Post-Graduate</option>
                    <option value="Civil Services Aspirant (UPSC / State PSC)">Civil Services Aspirant (UPSC / State PSC)</option>
                    <option value="Public Policy & Economic Researcher">Public Policy & Economic Researcher</option>
                    <option value="Independent Data Enthusiast">Independent Data Enthusiast</option>
                  </select>
                )}
              </div>
            </div>

            {/* DEPARTMENT / INSTITUTION */}
            <div className="register-field">
              <label>
                {accountType === "officer" ? "Ministry / Department / Division" : "Institution / University / City"}
              </label>
              <div className="register-input-wrapper">
                <Building2 size={18} className="register-input-icon" />
                <input
                  type="text"
                  name="department"
                  placeholder={
                    accountType === "officer"
                      ? "e.g. MoSPI, National Accounts Division"
                      : "e.g. Delhi University / Mumbai"
                  }
                  value={formData.department}
                  onChange={handleChange}
                />
              </div>
            </div>

            {/* PASSWORD */}
            <div className="register-field">
              <label>Password (Min. 6 characters) *</label>
              <div className="register-input-wrapper">
                <Lock size={18} className="register-input-icon" />
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Create a strong password"
                  value={formData.password}
                  onChange={handleChange}
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

            {/* CONFIRM PASSWORD */}
            <div className="register-field">
              <label>Confirm Password *</label>
              <div className="register-input-wrapper">
                <Lock size={18} className="register-input-icon" />
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  name="confirmPassword"
                  placeholder="Re-enter password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  aria-label="Toggle password visibility"
                >
                  {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {/* REGISTER BUTTON */}
            <button type="submit" className="register-submit-button">
              <UserPlus size={18} />
              <span>Complete Registration</span>
              <ArrowRight size={18} />
            </button>
          </form>

          {/* LOGIN LINK */}
          <div className="register-login-section">
            <span>Already have an account?</span>
            <button
              type="button"
              onClick={onBackToLogin}
              className="back-login-button"
            >
              Sign In Here
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
