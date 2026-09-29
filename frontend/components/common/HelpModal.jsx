import React from "react";
import { HelpCircle, X } from "lucide-react";
import { tr } from "../../i18n/index.js";

export default function HelpModal({ open, onClose, lang }) {
  if (!open) return null;

  return (
    <div className="app-modal-overlay" onClick={onClose} role="dialog" aria-modal="true">
      <div className="app-modal-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="app-modal-header">
          <div>
            <div className="system-label" style={{ color: "#0f2e5a" }}>
              MISSION KARMAYOGI · MOSPI KNOWLEDGE BASE
            </div>
            <h3>{tr(lang, "userGuide")}</h3>
            <p>National Statistical Capacity & Competency Intelligence Platform</p>
          </div>
          <button className="icon-btn" onClick={onClose} aria-label="Close user guide">
            <X size={16} />
          </button>
        </div>

        <div className="app-modal-body">
          <div
            className="credential-seal-banner"
            style={{ background: "#eff6ff", borderColor: "#bfdbfe", color: "#1e40af" }}
          >
            <div
              className="credential-seal-icon"
              style={{ background: "#dbeafe", color: "#1d4ed8" }}
            >
              <HelpCircle size={26} />
            </div>
            <div className="credential-seal-text">
              <strong style={{ color: "#1e3a8a" }}>
                National Statistical Systems Training Academy (NSSTA)
              </strong>
              <span style={{ color: "#2563eb" }}>
                Official Statistical Capacity Building & Competency Diagnostics Framework
              </span>
            </div>
          </div>

          <div className="lesson-checklist">
            <div className="lesson-check-item">
              <div>
                <strong>1. Competency Scoring Model</strong>
                <span>
                  Synthesizes 50% assessment scores, 25% course completions, 15% self-assessment, and 10% learning effort.
                </span>
              </div>
            </div>
            <div className="lesson-check-item">
              <div>
                <strong>2. iGOT Karmayogi Dynamic Recommendations</strong>
                <span>
                  Identifies critical skill gaps against official benchmarks and surfaces accredited courses to bridge them.
                </span>
              </div>
            </div>
            <div className="lesson-check-item">
              <div>
                <strong>3. Official Microdata Portals</strong>
                <span>
                  Provides integrated access to MoSPI, PLFS, NSS, CPI, and Census catalogs for authentic study.
                </span>
              </div>
            </div>
            <div className="lesson-check-item">
              <div>
                <strong>4. Credential Verification</strong>
                <span>
                  All issued certificates are verifiable against the MoSPI SSL/TLS 1.3 National Credential Registry.
                </span>
              </div>
            </div>
          </div>

          <div className="credential-hash-box">
            <span>MoSPI Institutional Support & Helpdesk</span>
            <p style={{ margin: "4px 0 0", fontSize: "0.85rem", color: "#334155" }}>
              Email: <strong>support-statskill@mospi.gov.in</strong> · Toll Free: <strong>1800-11-2334</strong> · New Delhi, India
            </p>
          </div>
        </div>

        <div className="app-modal-footer">
          <button className="primary-btn" onClick={onClose}>
            Got it
          </button>
        </div>
      </div>
    </div>
  );
}
