import React, { useState } from "react";
import {
  CheckCircle2,
  Moon,
  Save,
  ShieldCheck,
  Sun,
  Upload,
} from "lucide-react";
import { copy, tr } from "../i18n/index.js";
import {
  PageHeading,
  SystemCard,
} from "../components/common/index.js";

export default function SettingsPage({
  user = {},
  lang,
  setLang,
  theme,
  setTheme,
  appearance,
  setAppearance,
  onSaveUser,
}) {
  const [name, setName] = useState(user.name || "");
  const [photo, setPhoto] = useState(user.photo || "");
  const [saved, setSaved] = useState(false);

  const save = () => {
    const next = { ...user, name: name.trim() || user.name, photo };
    localStorage.setItem("statSkillUser", JSON.stringify(next));
    if (onSaveUser) onSaveUser(next);
    setSaved(true);
    setTimeout(() => setSaved(false), 1800);
  };

  const updatePhoto = (event) => {
    const file = event.target.files?.[0];
    if (!file || !file.type.startsWith("image/")) return;
    const reader = new FileReader();
    reader.onload = () => setPhoto(String(reader.result));
    reader.readAsDataURL(file);
  };

  return (
    <div className="stack">
      <PageHeading
        kicker={tr(lang, "systemConfiguration").toUpperCase()}
        title={tr(lang, "settings")}
        subtitle={tr(lang, "visualSummary")}
      />
      <div className="settings-grid">
        <SystemCard>
          <div className="system-label">{tr(lang, "profile").toUpperCase()}</div>
          <h2>{tr(lang, "profile")}</h2>
          <div className="profile-photo-editor">
            <div className="profile-photo-preview">
              {photo ? (
                <img src={photo} alt="Profile preview" />
              ) : (
                <span>{(name || user.name || "A")[0].toUpperCase()}</span>
              )}
            </div>
            <div className="profile-photo-actions">
              <strong>{copy(lang, "profilePhoto")}</strong>
              <span>{copy(lang, "profileHint")}</span>
              <div>
                <label className="photo-upload">
                  <Upload size={13} /> {copy(lang, "changePhoto")}
                  <input type="file" accept="image/*" onChange={updatePhoto} />
                </label>
                {photo && (
                  <button
                    type="button"
                    className="photo-remove"
                    onClick={() => setPhoto("")}
                  >
                    {copy(lang, "removePhoto")}
                  </button>
                )}
              </div>
            </div>
          </div>
          <label className="field-label">
            {tr(lang, "displayName")}
            <input value={name} onChange={(e) => setName(e.target.value)} />
          </label>
          <label className="field-label">
            {tr(lang, "email")}
            <input value={user.email || ""} readOnly aria-readonly="true" />
          </label>
          <label className="field-label">
            {tr(lang, "department")}
            <input
              value={user.department || "MoSPI"}
              readOnly
              aria-readonly="true"
            />
          </label>
          <button className="primary-btn" onClick={save}>
            <Save size={14} /> {tr(lang, "save")}
          </button>
          {saved && (
            <div className="save-note">
              <CheckCircle2 size={14} /> {tr(lang, "save")}
            </div>
          )}
        </SystemCard>

        <SystemCard className="theme-choice-card">
          <div className="system-label">{tr(lang, "visualSystem").toUpperCase()}</div>
          <h2>{tr(lang, "theme")}</h2>
          <div className="theme-options">
            <button
              type="button"
              className={`theme-option ${theme === "solo" ? "active" : ""}`}
              onClick={() => setTheme("solo")}
            >
              <span className="theme-dot solo" />
              <span>{tr(lang, "solo")}</span>
            </button>
            <button
              type="button"
              className={`theme-option ${theme === "executive" ? "active" : ""}`}
              onClick={() => setTheme("executive")}
            >
              <span className="theme-dot executive" />
              <span>{tr(lang, "executive")}</span>
            </button>
            <button
              type="button"
              className={`theme-option ${theme === "aurora" ? "active" : ""}`}
              onClick={() => setTheme("aurora")}
            >
              <span className="theme-dot aurora" />
              <span>{tr(lang, "aurora")}</span>
            </button>
          </div>

          <div className="setting-row">
            <div>
              <strong>{tr(lang, "language")}</strong>
              <span>{copy(lang, "languageHint")}</span>
            </div>
            <div className="language-buttons">
              {[
                ["en", "EN"],
                ["hi", "हिं"],
                ["ta", "த"],
                ["te", "తె"],
              ].map(([code, label]) => (
                <button
                  type="button"
                  key={code}
                  className={lang === code ? "active" : ""}
                  onClick={() => setLang(code)}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          <div className="setting-row">
            <div>
              <strong>{tr(lang, "appearance")}</strong>
              <span>{copy(lang, "appearanceHint")}</span>
            </div>
            <button
              type="button"
              className="theme-switch"
              onClick={() => setAppearance((v) => (v === "dark" ? "light" : "dark"))}
            >
              {appearance === "dark" ? <Sun size={15} /> : <Moon size={15} />}{" "}
              {appearance === "dark" ? tr(lang, "dark") : tr(lang, "light")}
            </button>
          </div>
        </SystemCard>
      </div>

      <SystemCard className="security-card">
        <ShieldCheck size={22} />
        <div>
          <div className="system-label">
            {tr(lang, "securityStatus").toUpperCase()}
          </div>
          <h2>{tr(lang, "demoEnvironment")}</h2>
          <p>{tr(lang, "connectProduction")}</p>
        </div>
      </SystemCard>
    </div>
  );
}
