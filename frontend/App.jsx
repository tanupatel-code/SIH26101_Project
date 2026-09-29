import React, { useEffect, useMemo, useState } from "react";
import Login from "./login.jsx";
import Register from "./register.jsx";
import QuizPlayer from "./QuizPlayer.jsx";
import Sidebar from "./components/layout/Sidebar.jsx";
import Header from "./components/layout/Header.jsx";
import HelpModal from "./components/common/HelpModal.jsx";

// Pages
import DashboardPage from "./pages/DashboardPage.jsx";
import CompetenciesPage from "./pages/CompetenciesPage.jsx";
import LearningPathPage from "./pages/LearningPathPage.jsx";
import AssessmentsPage from "./pages/AssessmentsPage.jsx";
import DocumentsPage from "./pages/DocumentsPage.jsx";
import CertificatesPage from "./pages/CertificatesPage.jsx";
import AnalyticsPage from "./pages/AnalyticsPage.jsx";
import DataSourcesPage from "./pages/DataSourcesPage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";

// Services & Engine
import {
  API_BASE_URL,
  apiGenerateMCQs,
  apiLogin,
  apiRegister,
  apiUpdateProfile,
  apiFetchMe,
} from "./services/api/client.js";
import {
  KARMAYOGI_DATA,
  normalizeCompetencyPayload,
  runCompetencyEngine,
} from "./services/competency/competencyEngine.js";
import { notificationsFor } from "./i18n/index.js";
import { useTheme } from "./hooks/useTheme.js";
import { useAuth } from "./hooks/useAuth.js";
import Toast from "./components/common/Toast.jsx";

// Design System Themes
import "./solo.css";
import "./executive.css";
import "./aurora.css";
import "./educational.css";

export default function App() {
  const [competencyData, setCompetencyData] = useState(() =>
    normalizeCompetencyPayload(KARMAYOGI_DATA)
  );
  const engine = useMemo(
    () => runCompetencyEngine(competencyData),
    [competencyData]
  );

  const { theme, setTheme, appearance, setAppearance, lang, setLang } = useTheme();
  const {
    user,
    setUser,
    apiToken,
    loggedIn,
    profileData,
    login,
    logout,
    applyApiSnapshot,
  } = useAuth(setCompetencyData);

  const [toast, setToast] = useState(null);
  const showToast = (message, type = "info") => setToast({ message, type });

  const [register, setRegister] = useState(false);
  const [active, setActive] = useState("Dashboard");
  const [menuOpen, setMenuOpen] = useState(false);
  const [notifOpen, setNotifOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);
  const [activeQuiz, setActiveQuiz] = useState(null);

  const notifications = notificationsFor(lang);

  const handleStartQuiz = async (config) => {
    const domain =
      typeof config === "string"
        ? config
        : config?.domain || "statisticalMethods";
    const title =
      typeof config === "object" && config?.title
        ? config.title
        : `Diagnostic Assessment: ${domain}`;

    try {
      const res = await apiGenerateMCQs(
        {
          domain,
          topic: title,
          num_questions: 5,
          difficulty: "Intermediate",
          bloom_level: "Understanding",
        },
        apiToken
      );

      const questions = res?.questions || res || [];
      if (!Array.isArray(questions) || questions.length === 0) {
        throw new Error("No questions returned for this domain.");
      }

      setActiveQuiz({
        quizId: `QUIZ-${domain.toUpperCase().slice(0, 4)}-${Date.now()}`,
        title,
        domain,
        domainName:
          engine?.competencies?.find((c) => c.key === domain)?.name ||
          "Statistical Assessment",
        questions,
      });
    } catch (err) {
      console.warn("Failed to generate quiz, loading fallback:", err);
      setActiveQuiz({
        quizId: `QUIZ-${domain.toUpperCase().slice(0, 4)}-FALLBACK`,
        title,
        domain,
        domainName: "Official Statistical Systems",
        questions: [
          {
            id: "fallback-q1",
            question:
              "Under India's Official Statistical System, why is stratified multi-stage sampling standardly preferred for nationwide household expenditure surveys?",
            options: [
              "It accounts for rural/urban heterogeneity and minimizes intra-cluster sampling variance",
              "It completely eliminates the requirement for auxiliary census baseline frames",
              "It automatically imputes non-response without statistical weight calibration",
              "It restricts data collection exclusively to urban metropolitan corporations",
            ],
            correct_index: 0,
            explanation:
              "Stratification creates internally homogeneous groups across rural/urban divides, minimizing overall sampling variance.",
          },
        ],
      });
    }
  };

  const handleLogin = async ({ email, password }) => {
    try {
      const result = await apiLogin(email, password);
      login(result);
      setActive("Dashboard");
      showToast("Signed in successfully.", "success");
    } catch (error) {
      showToast(error.message || "Invalid credentials. Please verify your email and password.", "error");
    }
  };

  const handleRegister = async (formData) => {
    try {
      const result = await apiRegister(formData);
      login(result);
      setRegister(false);
      setActive("Dashboard");
      showToast("Account registered successfully.", "success");
    } catch (error) {
      showToast(error.message || "Registration failed.", "error");
    }
  };

  const saveUserProfile = async (nextUser) => {
    setUser(nextUser);
    localStorage.setItem("statSkillUser", JSON.stringify(nextUser));
    if (!apiToken) return;
    try {
      const snapshot = await apiUpdateProfile(apiToken, { name: nextUser.name });
      applyApiSnapshot(snapshot);
      showToast("Profile updated successfully.", "success");
    } catch (error) {
      showToast(error.message || "Unable to save profile.", "error");
    }
  };

  const handleLogout = async () => {
    await logout();
    setMenuOpen(false);
    showToast("Signed out successfully.", "info");
  };

  if (!loggedIn) {
    return register ? (
      <Register
        onRegister={handleRegister}
        onBackToLogin={() => setRegister(false)}
      />
    ) : (
      <Login onLogin={handleLogin} onRegister={() => setRegister(true)} />
    );
  }

  const labelKey =
    active === "Dashboard"
      ? "dashboard"
      : active === "My Competencies"
      ? "competencies"
      : active === "Learning Path"
      ? "path"
      : active === "Assessments"
      ? "assessments"
      : active === "My Documents"
      ? "documents"
      : active === "Certificates"
      ? "certificates"
      : active === "Analytics"
      ? "analytics"
      : active === "Data Sources"
      ? "dataSources"
      : "settings";

  const pageData = profileData || competencyData || {};

  const renderPage = () => {
    switch (active) {
      case "Dashboard":
        return (
          <DashboardPage
            user={user}
            lang={lang}
            onNavigate={setActive}
            engine={engine}
            data={pageData}
          />
        );
      case "My Competencies":
        return <CompetenciesPage engine={engine} lang={lang} data={pageData} />;
      case "Learning Path":
        return (
          <LearningPathPage
            lang={lang}
            data={pageData}
            engine={engine}
            onNavigate={setActive}
            onStartQuiz={handleStartQuiz}
            apiToken={apiToken}
          />
        );
      case "Assessments":
        return (
          <AssessmentsPage
            lang={lang}
            data={pageData}
            engine={engine}
            onStartQuiz={handleStartQuiz}
          />
        );
      case "My Documents":
        return (
          <DocumentsPage
            lang={lang}
            data={pageData}
            apiToken={apiToken}
            onStartQuiz={handleStartQuiz}
          />
        );
      case "Certificates":
        return (
          <CertificatesPage
            lang={lang}
            data={pageData}
            onNavigate={setActive}
            apiToken={apiToken}
          />
        );
      case "Analytics":
        return <AnalyticsPage engine={engine} lang={lang} data={pageData} />;
      case "Data Sources":
        return <DataSourcesPage lang={lang} />;
      case "Settings":
        return (
          <SettingsPage
            user={user}
            lang={lang}
            setLang={setLang}
            theme={theme}
            setTheme={setTheme}
            appearance={appearance}
            setAppearance={setAppearance}
            onSaveUser={saveUserProfile}
          />
        );
      default:
        return (
          <DashboardPage
            user={user}
            lang={lang}
            onNavigate={setActive}
            engine={engine}
            data={pageData}
          />
        );
    }
  };

  return (
    <div className="layout">
      <Sidebar
        active={active}
        setActive={setActive}
        open={menuOpen}
        setOpen={setMenuOpen}
        lang={lang}
        user={user}
        onLogout={handleLogout}
        engine={engine}
      />

      {menuOpen && (
        <button
          className="overlay"
          aria-label="Close menu"
          onClick={() => setMenuOpen(false)}
        />
      )}

      <div className="main-area">
        <Header
          lang={lang}
          labelKey={labelKey}
          menuOpen={menuOpen}
          setMenuOpen={setMenuOpen}
          notifOpen={notifOpen}
          setNotifOpen={setNotifOpen}
          notifications={notifications}
          pageNotifications={pageData?.notifications || []}
          user={user}
          onOpenHelp={() => setHelpOpen(true)}
        />
        <main>{renderPage()}</main>
      </div>

      <HelpModal
        open={helpOpen}
        onClose={() => setHelpOpen(false)}
        lang={lang}
      />

      {activeQuiz && (
        <QuizPlayer
          quizId={activeQuiz.quizId}
          title={activeQuiz.title}
          domain={activeQuiz.domain}
          domainName={activeQuiz.domainName}
          questions={activeQuiz.questions}
          apiBaseUrl={API_BASE_URL}
          apiToken={apiToken}
          onClose={() => setActiveQuiz(null)}
          onCompleted={async () => {
            setActiveQuiz(null);
            if (apiToken) {
              const snap = await apiFetchMe(apiToken).catch(() => null);
              if (snap) applyApiSnapshot(snap);
            }
          }}
        />
      )}

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}
