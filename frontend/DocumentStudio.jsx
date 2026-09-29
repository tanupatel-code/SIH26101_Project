import React, { useState, useRef } from "react";
import {
  BookOpen,
  CheckCircle2,
  Download,
  FileCheck2,
  FileText,
  FolderOpen,
  HelpCircle,
  PlayCircle,
  Plus,
  Search,
  Sparkles,
  Upload,
  X,
} from "lucide-react";

export default function DocumentStudio({
  documents = [],
  apiBaseUrl = (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_BASE_URL ? import.meta.env.VITE_API_BASE_URL.replace(/\/$/, "") : "http://localhost:8000"),
  apiToken = "",
  onDocumentUploaded,
  onStartQuiz,
}) {
  const [query, setQuery] = useState("");
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [generatorModalOpen, setGeneratorModalOpen] = useState(false);
  const [generating, setGenerating] = useState(false);

  // MCQ Generator parameters
  const [numQuestions, setNumQuestions] = useState(5);
  const [difficulty, setDifficulty] = useState("Intermediate");
  const [bloomLevel, setBloomLevel] = useState("Understanding");
  const [targetDomain, setTargetDomain] = useState("statisticalMethods");

  const fileInputRef = useRef(null);

  const handleFileUpload = async (file) => {
    if (!file) return;
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${apiBaseUrl}/api/documents/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${apiToken}`,
        },
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to upload document.");
      }

      if (onDocumentUploaded) {
        onDocumentUploaded(data.document);
      }
      alert(`Document '${file.name}' uploaded and parsed successfully! Ready for AI Quiz generation.`);
    } catch (err) {
      alert(`Upload error: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const openGeneratorForDoc = (doc) => {
    setSelectedDoc(doc);
    if (doc.category === "National Accounts") setTargetDomain("nationalAccounts");
    else if (doc.category === "Price Indices") setTargetDomain("priceIndices");
    else if (doc.category === "Data Quality") setTargetDomain("dataQuality");
    else if (doc.category === "GIS & Spatial") setTargetDomain("gis");
    else setTargetDomain("statisticalMethods");
    setGeneratorModalOpen(true);
  };

  const handleGenerateQuiz = async () => {
    setGenerating(true);
    try {
      const payload = {
        document_id: selectedDoc?.id || null,
        document_text: selectedDoc?.extractedText || selectedDoc?.summary || null,
        num_questions: Number(numQuestions),
        difficulty: difficulty,
        bloom_level: bloomLevel,
        domain: targetDomain,
      };

      const response = await fetch(`${apiBaseUrl}/api/mcq/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiToken}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to generate AI quiz.");
      }

      setGeneratorModalOpen(false);
      if (onStartQuiz) {
        onStartQuiz({
          quizId: `QUIZ-GEN-${Date.now()}`,
          title: `AI Diagnostic: ${selectedDoc ? selectedDoc.name : targetDomain}`,
          domain: targetDomain,
          domainName: targetDomain === "nationalAccounts" ? "National Accounts" : targetDomain === "priceIndices" ? "Price Statistics" : "Official Statistics",
          questions: data.questions,
        });
      }
    } catch (err) {
      alert(`Generation error: ${err.message}`);
    } finally {
      setGenerating(false);
    }
  };

  const filteredDocs = documents.filter((d) =>
    `${d.name || ""} ${d.category || ""} ${d.summary || ""}`
      .toLowerCase()
      .includes(query.toLowerCase())
  );

  return (
    <div className="stack">
      {/* Page Heading */}
      <div className="page-heading system-card">
        <div>
          <div className="kicker">DOCUMENT INTELLIGENCE & INGESTION</div>
          <h1>Learning Materials & AI Quiz Generator</h1>
          <p>
            Upload MoSPI manuals, survey protocols, or statistical training notes to extract key concepts and automatically generate Bloom's taxonomy quizzes.
          </p>
        </div>
        <button
          className="primary-btn"
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
        >
          <Upload size={14} /> {uploading ? "Ingesting..." : "Upload New Material"}
        </button>
      </div>

      <input
        type="file"
        ref={fileInputRef}
        style={{ display: "none" }}
        accept=".pdf,.docx,.doc,.pptx,.ppt,.txt,.md,.csv"
        onChange={(e) => {
          if (e.target.files && e.target.files[0]) {
            handleFileUpload(e.target.files[0]);
          }
        }}
      />

      {/* Drag & Drop Upload Zone */}
      <div
        className={`doc-dropzone ${dragOver ? "dragover" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="doc-dropzone-icon">
          <Upload size={24} />
        </div>
        <h3 style={{ margin: "0 0 6px", fontSize: "1.05rem", color: "#f8fafc" }}>
          {uploading ? "Ingesting and chunking document..." : "Drag & Drop Learning Materials Here"}
        </h3>
        <p style={{ margin: 0, fontSize: "0.85rem", color: "#94a3b8" }}>
          Supports official training formats: PDF, Word (DOCX), PowerPoint (PPTX), and Markdown/Text.
        </p>
      </div>

      {/* Search & Filter */}
      <section className="system-card">
        <div className="card-header">
          <div>
            <div className="system-label">OFFICIAL MATERIAL VAULT</div>
            <h2>Ingested Learning Materials ({documents.length})</h2>
          </div>
          <div className="search">
            <Search size={15} />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search documents by keyword or domain..."
            />
          </div>
        </div>

        {/* Documents Table */}
        <div className="document-table">
          <div className="table-head">
            <span>Material Title & Summary</span>
            <span>Category</span>
            <span>Size / Words</span>
            <span>AI Actions</span>
          </div>
          {filteredDocs.map((doc, idx) => (
            <div className="table-row" key={doc.id || idx}>
              <div className="doc-name">
                <div className="file-icon">
                  <FileText size={18} />
                </div>
                <div>
                  <strong>{doc.name}</strong>
                  <span style={{ fontSize: "0.82rem", color: "#94a3b8", display: "block" }}>
                    {doc.summary || doc.id || "Official training publication"}
                  </span>
                </div>
              </div>
              <div>
                <span className="edu-badge cadre-nssta">{doc.category || "General"}</span>
              </div>
              <span style={{ fontSize: "0.88rem", color: "#cbd5e1" }}>
                {doc.size || "120 KB"} {doc.wordCount ? `· ${doc.wordCount} words` : ""}
              </span>
              <div>
                <button
                  type="button"
                  className="primary-btn"
                  style={{ fontSize: "0.82rem", padding: "6px 12px" }}
                  onClick={() => openGeneratorForDoc(doc)}
                >
                  <Sparkles size={13} /> Generate AI Quiz
                </button>
              </div>
            </div>
          ))}
          {filteredDocs.length === 0 && (
            <div style={{ padding: 24, textAlign: "center", color: "#94a3b8" }}>
              No learning materials found. Upload a PDF or DOCX file to get started.
            </div>
          )}
        </div>
      </section>

      {/* AI MCQ Generator Modal */}
      {generatorModalOpen && (
        <div className="quiz-overlay">
          <div className="quiz-container" style={{ maxWidth: 580 }}>
            <div className="quiz-header">
              <div>
                <span className="edu-badge bloom-analysis">AI Quiz Synthesis</span>
                <h2 style={{ fontSize: "1.1rem", margin: "4px 0 0", color: "#f8fafc" }}>
                  Generate Quiz from: {selectedDoc?.name || "Topic"}
                </h2>
              </div>
              <button className="icon-btn" onClick={() => setGeneratorModalOpen(false)}>
                <X size={18} />
              </button>
            </div>

            <div className="quiz-body" style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div>
                <label className="field-label" style={{ fontWeight: 600, color: "#e2e8f0" }}>
                  Number of Questions
                </label>
                <select
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(Number(e.target.value))}
                  style={{ width: "100%", padding: "10px", borderRadius: 8, background: "#060f1c", border: "1px solid rgba(255,255,255,0.15)", color: "#fff" }}
                >
                  <option value={3}>3 Questions (Quick Knowledge Check)</option>
                  <option value={5}>5 Questions (Standard Diagnostic)</option>
                  <option value={10}>10 Questions (Comprehensive Exam)</option>
                </select>
              </div>

              <div>
                <label className="field-label" style={{ fontWeight: 600, color: "#e2e8f0" }}>
                  Difficulty Level
                </label>
                <div style={{ display: "flex", gap: 10 }}>
                  {["Beginner", "Intermediate", "Advanced"].map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      className={`theme-option ${difficulty === lvl ? "active" : ""}`}
                      onClick={() => setDifficulty(lvl)}
                      style={{ flex: 1, padding: "8px 12px" }}
                    >
                      {lvl}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="field-label" style={{ fontWeight: 600, color: "#e2e8f0" }}>
                  Bloom's Taxonomy Objective
                </label>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                  {["Recall", "Understanding", "Application", "Analysis"].map((b) => (
                    <button
                      key={b}
                      type="button"
                      className={`theme-option ${bloomLevel === b ? "active" : ""}`}
                      onClick={() => setBloomLevel(b)}
                      style={{ padding: "8px 10px", fontSize: "0.85rem" }}
                    >
                      {b}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="field-label" style={{ fontWeight: 600, color: "#e2e8f0" }}>
                  Target Official Statistical Domain
                </label>
                <select
                  value={targetDomain}
                  onChange={(e) => setTargetDomain(e.target.value)}
                  style={{ width: "100%", padding: "10px", borderRadius: 8, background: "#060f1c", border: "1px solid rgba(255,255,255,0.15)", color: "#fff" }}
                >
                  <option value="statisticalMethods">Statistical Methods & Sampling</option>
                  <option value="nationalAccounts">National Accounts (SNA & GDP)</option>
                  <option value="priceIndices">Price Statistics (CPI/WPI/IIP)</option>
                  <option value="dataQuality">Data Quality & Survey Validation</option>
                  <option value="gis">GIS & Spatial Statistics</option>
                  <option value="python">Python for Data Automation</option>
                </select>
              </div>
            </div>

            <div className="quiz-footer">
              <button
                type="button"
                className="secondary-btn"
                onClick={() => setGeneratorModalOpen(false)}
              >
                Cancel
              </button>
              <button
                type="button"
                className="primary-btn"
                disabled={generating}
                onClick={handleGenerateQuiz}
              >
                {generating ? "Generating Questions..." : "Generate & Launch Quiz"} <Sparkles size={14} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
