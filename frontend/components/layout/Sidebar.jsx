import React from "react";
import { BarChart3, ChevronRight, X } from "lucide-react";
import { NAV } from "../../constants/navigation.js";
import { tr } from "../../i18n/index.js";
import Progress from "../common/Progress.jsx";
import { isOfficerUser } from "../../services/auth/authService.js";

export default function Sidebar({
  active,
  setActive,
  open,
  setOpen,
  lang,
  user = {},
  onLogout,
  engine = {},
}) {
  const isOfficer = isOfficerUser(user);

  return (
    <aside className={`sidebar ${open ? "open" : ""}`} aria-label="Main Navigation">
      <div className="brand">
        <div className="brand-mark">
          <BarChart3 size={20} />
        </div>
        <div>
          <strong>StatSkill Portal</strong>
          <span>
            {user?.projectId && !String(user.projectId).toUpperCase().includes("SIH")
              ? user.projectId
              : isOfficer
              ? "Official Statistics Cadre"
              : "Open Statistics Track"}{" "}
            · {user?.department || (isOfficer ? "MoSPI" : "National Statistical System")}
          </span>
        </div>
      </div>

      <div className="sidebar-status">
        <span className="live-dot" /> {tr(lang, "online")}
      </div>

      <nav>
        {NAV.map((item) => {
          const Icon = item.icon;
          const key =
            item.id === "Dashboard"
              ? "dashboard"
              : item.id === "My Competencies"
              ? "competencies"
              : item.id === "Learning Path"
              ? "path"
              : item.id === "Assessments"
              ? "assessments"
              : item.id === "My Documents"
              ? "documents"
              : item.id === "Certificates"
              ? "certificates"
              : item.id === "Analytics"
              ? "analytics"
              : item.id === "Data Sources"
              ? "dataSources"
              : "settings";

          return (
            <button
              key={item.id}
              className={active === item.id ? "active" : ""}
              onClick={() => {
                setActive(item.id);
                setOpen(false);
              }}
              aria-current={active === item.id ? "page" : undefined}
            >
              <Icon size={17} />
              <span>{tr(lang, key)}</span>
              {active === item.id && <ChevronRight size={13} />}
            </button>
          );
        })}
      </nav>

      <div className="sidebar-spacer" />

      <div className="sidebar-player">
        <div className="small-label">{tr(lang, "player").toUpperCase()}</div>
        <strong>{user?.name || "Learner"}</strong>
        <span>
          {user?.role ||
            (isOfficer
              ? "Senior Statistical Officer (SSO)"
              : "Citizen Data Analyst & Research Scholar")}
        </span>
        <Progress value={engine?.overallScore || 0} color="cyan" />
        <div className="player-bottom">
          <span>Readiness: {engine?.overallScore || 0}%</span>
          <span>{user?.department || (isOfficer ? "MoSPI" : "Academic / Citizen")}</span>
        </div>
      </div>

      <button className="logout-btn" onClick={onLogout} aria-label={tr(lang, "signOut")}>
        <X size={15} /> {tr(lang, "signOut")}
      </button>
    </aside>
  );
}
