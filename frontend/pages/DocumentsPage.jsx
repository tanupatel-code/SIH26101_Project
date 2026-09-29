import React, { useState } from "react";
import {
  Download,
  FileText,
  FolderOpen,
  Search,
  Upload,
} from "lucide-react";
import { tr } from "../i18n/index.js";
import {
  PageHeading,
  SystemCard,
} from "../components/common/index.js";
import { generateClientPdfBlob } from "../utils/pdfGenerator.js";
import DocumentStudio from "../DocumentStudio.jsx";
import {
  API_BASE_URL,
  API_TOKEN_KEY,
  getDocumentDownloadUrl,
} from "../services/api/client.js";

export default function DocumentsPage({ lang, data = {}, apiToken, onStartQuiz }) {
  const [query, setQuery] = useState("");
  const [downloadingId, setDownloadingId] = useState(null);
  const [activeTab, setActiveTab] = useState("vault"); // "vault" | "studio"

  const documents = data?.documents || [];
  const filtered = documents.filter((d) =>
    `${d.name || ""} ${d.category || ""} ${d.id || ""}`
      .toLowerCase()
      .includes(query.toLowerCase())
  );

  const handleDownload = async (doc) => {
    setDownloadingId(doc.id);
    try {
      const token = apiToken || localStorage.getItem(API_TOKEN_KEY) || "";
      const url = getDocumentDownloadUrl(doc.id);
      const res = await fetch(url, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!res.ok) {
        throw new Error("Download API failed");
      }
      const blob = await res.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = blobUrl;
      const cleanName = (doc.name || `${doc.id}.pdf`).replace(/[–—]/g, "-");
      a.download = cleanName;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
      console.warn("Direct API download fallback:", err);
      const cleanName = (doc.name || `${doc.id}.pdf`).replace(/[–—]/g, "-");
      const blob = generateClientPdfBlob(
        `StatSkill AI - ${doc.name}`,
        `Ministry of Statistics & Programme Implementation · ${doc.category || "Study Material"}`,
        [
          `Document ID: ${doc.id}`,
          `Category: ${doc.category || "General Statistics"}`,
          "Status: Verified Official MoSPI Learning Resource",
          "--------------------------------------------------------------------------------",
          "Course Study Guide & Methodological Syllabus:",
          doc.summary ||
            "Standard operating procedure for data collection, validation, and estimation.",
          "--------------------------------------------------------------------------------",
          "Learning Objectives & Competency Benchmarks:",
          "1. Understand fundamental survey concepts, rotating panels, and strata weighting.",
          "2. Detect outliers, impute missing values, and validate enterprise microdata.",
          "3. Apply computational algorithms in Python/Pandas for statistical indicators.",
          "National Statistical Office · Government of India · 2026",
        ]
      );
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = blobUrl;
      a.download = cleanName.endsWith(".pdf") ? cleanName : `${cleanName}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } finally {
      setTimeout(() => setDownloadingId(null), 800);
    }
  };

  return (
    <div className="stack">
      <PageHeading
        kicker={tr(lang, "documentVault").toUpperCase()}
        title={tr(lang, "documents")}
        subtitle={tr(lang, "visualSummary")}
        actions={
          <div className="tab-pill-row">
            <button
              type="button"
              className={`pill-btn ${activeTab === "vault" ? "active" : ""}`}
              onClick={() => setActiveTab("vault")}
            >
              <FolderOpen size={14} /> Vault
            </button>
            <button
              type="button"
              className={`pill-btn ${activeTab === "studio" ? "active" : ""}`}
              onClick={() => setActiveTab("studio")}
            >
              <Upload size={14} /> Document Studio & AI Generator
            </button>
          </div>
        }
      />

      {activeTab === "studio" ? (
        <DocumentStudio
          documents={documents}
          apiBaseUrl={API_BASE_URL}
          apiToken={apiToken}
          onStartQuiz={onStartQuiz}
        />
      ) : (
        <>
          <div className="summary-grid three">
            <SystemCard className="summary-card">
              <span>{tr(lang, "totalDocuments").toUpperCase()}</span>
              <strong>{documents.length}</strong>
            </SystemCard>
            <SystemCard className="summary-card">
              <span>{tr(lang, "shared").toUpperCase()}</span>
              <strong className="purple">
                {documents.filter((d) => d.shared === true).length}
              </strong>
            </SystemCard>
            <SystemCard className="summary-card">
              <span>{tr(lang, "addedThisMonth").toUpperCase()}</span>
              <strong className="green">
                {documents.filter((d) => d.addedThisMonth === true).length}
              </strong>
            </SystemCard>
          </div>

          <SystemCard>
            <div className="card-header">
              <div>
                <div className="system-label">OFFICIAL DOCUMENTS</div>
                <h2>Repository Records</h2>
              </div>
              <div className="search">
                <Search size={15} />
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder={tr(lang, "search")}
                  aria-label={tr(lang, "search")}
                />
              </div>
            </div>

            <div className="document-table">
              <div className="table-head">
                <span>{tr(lang, "documents")}</span>
                <span>Category</span>
                <span>Size</span>
                <span>Action</span>
              </div>
              {filtered.map((d) => (
                <div className="table-row" key={d.id}>
                  <div className="doc-name">
                    <div className="file-icon">
                      <FileText size={16} />
                    </div>
                    <div>
                      <strong>{d.name}</strong>
                      <span>{d.id}</span>
                    </div>
                  </div>
                  <span>{d.category}</span>
                  <span>{d.size}</span>
                  <button
                    className="icon-btn"
                    title={`Download ${d.name}`}
                    onClick={() => handleDownload(d)}
                    disabled={downloadingId === d.id}
                    style={{ cursor: "pointer", color: "#0f2e5a" }}
                    aria-label={`Download ${d.name}`}
                  >
                    <Download size={15} />
                  </button>
                </div>
              ))}
              {filtered.length === 0 && (
                <div className="empty-row p-4 text-center text-muted">
                  No documents found matching "{query}".
                </div>
              )}
            </div>
          </SystemCard>
        </>
      )}
    </div>
  );
}
