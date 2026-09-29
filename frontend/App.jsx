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
  API_REFRESH_MS,
  API_TOKEN_KEY,
  apiFetchMe,
  apiGenerateMCQs,
  apiLogin,
  apiLogout,
  apiRegister,
  apiUpdateProfile,
} from "./services/api/client.js";
import {
  clearSession,
  safeUser,
  storeSession,
} from "./services/auth/authService.js";
import {
  KARMAYOGI_DATA,
  normalizeCompetencyPayload,
  runCompetencyEngine,
} from "./services/competency/competencyEngine.js";
import { notificationsFor } from "./i18n/index.js";

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

  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem("statSkillVisualTheme");
    return stored === "executive" || stored === "aurora" || stored === "solo"
      ? stored
      : "executive";
  });
  const [appearance, setAppearance] = useState(
    () => localStorage.getItem("statSkillAppearance") === "dark" ? "dark" : "light"
  );
  const [lang, setLang] = useState(() =>
    ["en", "hi", "ta", "te"].includes(localStorage.getItem("statSkillLanguage"))
      ? localStorage.getItem("statSkillLanguage")
      : "en"
  );

  const [user, setUser] = useState(() => safeUser());
  const [profileData, setProfileData] = useState(null);
  const [apiToken, setApiToken] = useState(
    () => localStorage.getItem(API_TOKEN_KEY) || ""
  );
  const [loggedIn, setLoggedIn] = useState(() =>
    Boolean(localStorage.getItem(API_TOKEN_KEY))
  );
  const [register, setRegister] = useState(false);
  const [active, setActive] = useState("Dashboard");
  const [menuOpen, setMenuOpen] = useState(false);
  const [notifOpen, setNotifOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);
  const [activeQuiz, setActiveQuiz] = useState(null);

  const notifications = notificationsFor(lang);

  const applyApiSnapshot = (snapshot) => {
    const data = snapshot?.data || snapshot;
    if (!data) return;
    const normalized = normalizeCompetencyPayload(data);
    setProfileData(data);
    const currentUser = data.user || data.profile || null;
    setUser(currentUser);
    setCompetencyData(normalized);
    if (currentUser) {
      localStorage.setItem("statSkillUser", JSON.stringify(currentUser));
    }
  };

  useEffect(() => {
    if (!loggedIn || !apiToken) return undefined;

    let mounted = true;
    const refreshUserData = async () => {
      try {
        const snapshot = await apiFetchMe(apiToken);
        if (mounted) applyApiSnapshot(snapshot);
      } catch (error) {
        console.warn("Unable to refresh user data:", error);
        if (mounted && /401|session|token/i.test(String(error.message || ""))) {
          clearSession();
          setApiToken("");
          setLoggedIn(false);
        }
      }
    };

    refreshUserData();
    const intervalId = window.setInterval(refreshUserData, API_REFRESH_MS);
    const handleFocus = () => {
      refreshUserData();
    };
    window.addEventListener("focus", handleFocus);

    return () => {
      mounted = false;
      window.clearInterval(intervalId);
      window.removeEventListener("focus", handleFocus);
    };
  }, [loggedIn, apiToken]);

  useEffect(() => {
    localStorage.setItem("statSkillVisualTheme", theme);
    localStorage.setItem("statSkillAppearance", appearance);
    localStorage.setItem("statSkillLanguage", lang);
    document.documentElement.dataset.themeMode = theme;
    document.documentElement.dataset.appearanceMode = appearance;
    document.body.classList.remove(
      "theme-solo",
      "theme-executive",
      "theme-aurora",
      "appearance-dark",
      "appearance-light"
    );
    document.body.classList.add(`theme-${theme}`, `appearance-${appearance}`);
  }, [theme, appearance, lang]);

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
      const token = result.access_token;
      storeSession(token, result.data?.user || result.data?.profile);
      setApiToken(token);
      applyApiSnapshot(result.data);
      setLoggedIn(true);
      setActive("Dashboard");
    } catch (error) {
      alert(error.message || "Invalid credentials. Please verify your email and password.");
    }
  };

  const handleRegister = async (formData) => {
    try {
      const result = await apiRegister(formData);
      const token = result.access_token;
      storeSession(token, result.data?.user || result.data?.profile);
      setApiToken(token);
      applyApiSnapshot(result.data);
      setLoggedIn(true);
      setRegister(false);
      setActive("Dashboard");
    } catch (error) {
      alert(error.message || "Registration failed.");
    }
  };

  const saveUserProfile = async (nextUser) => {
    setUser(nextUser);
    localStorage.setItem("statSkillUser", JSON.stringify(nextUser));
    if (!apiToken) return;
    try {
      const snapshot = await apiUpdateProfile(apiToken, { name: nextUser.name });
      applyApiSnapshot(snapshot);
    } catch (error) {
      alert(error.message || "Unable to save profile.");
    }
  };

  const logout = async () => {
    await apiLogout(apiToken);
    clearSession();
    setApiToken("");
    setProfileData(null);
    setLoggedIn(false);
    setMenuOpen(false);
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
        onLogout={logout}
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
    </div>
  );
}
