import React from "react";
import { Bell, HelpCircle, Menu, X } from "lucide-react";
import { tr } from "../../i18n/index.js";

export default function Header({
  lang,
  labelKey,
  menuOpen,
  setMenuOpen,
  notifOpen,
  setNotifOpen,
  notifications = [],
  pageNotifications = [],
  user = {},
  onOpenHelp,
}) {
  const notifList = pageNotifications?.length ? pageNotifications : notifications;

  return (
    <header className="topbar">
      <div className="topbar-left">
        <button
          className="menu-btn"
          onClick={() => setMenuOpen((v) => !v)}
          aria-label={menuOpen ? "Close menu" : "Open menu"}
          aria-expanded={menuOpen}
        >
          <Menu size={18} />
        </button>
        <div>
          <div className="eyebrow">STATSKILL / {tr(lang, labelKey).toUpperCase()}</div>
          <strong>{tr(lang, labelKey)}</strong>
        </div>
      </div>

      <div className="topbar-actions">
        <div className="status-chip">
          <span className="live-dot" /> {tr(lang, "live")}
        </div>

        <button
          className="icon-btn"
          title={tr(lang, "help")}
          onClick={onOpenHelp}
          aria-label={tr(lang, "help")}
        >
          <HelpCircle size={16} />
        </button>

        <div className="notification-wrap">
          <button
            className="icon-btn"
            title={tr(lang, "notifications")}
            onClick={() => setNotifOpen((v) => !v)}
            aria-label={tr(lang, "notifications")}
            aria-expanded={notifOpen}
          >
            <Bell size={16} />
            {notifList.length > 0 && <span className="notif-dot" />}
          </button>

          {notifOpen && (
            <div className="notification-popover" role="dialog" aria-label="Notifications">
              <div className="notification-head">
                <strong>{tr(lang, "notifications")}</strong>
                <button
                  className="icon-btn"
                  onClick={() => setNotifOpen(false)}
                  aria-label="Close notifications"
                >
                  <X size={14} />
                </button>
              </div>
              {notifList.length === 0 ? (
                <div className="notification-item empty">
                  <span>{tr(lang, "noNotifications")}</span>
                </div>
              ) : (
                notifList.map((n, i) => (
                  <div className="notification-item" key={n.id || i}>
                    <span className={`mini-icon ${n.color || "cyan"}`}>
                      <Bell size={13} />
                    </span>
                    <div>
                      <strong>{n.title}</strong>
                      <span>{n.time || "—"}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        <div className="profile-chip">
          <div className="avatar-sm">{(user?.name || "A")[0].toUpperCase()}</div>
          <div className="profile-chip-info">
            <strong className="profile-chip-name">{user?.name || "Investigator"}</strong>
            <span className="profile-chip-role">{user?.role || tr(lang, "role")}</span>
          </div>
        </div>
      </div>
    </header>
  );
}
