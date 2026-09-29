import React from "react";
import { AlertCircle } from "lucide-react";

export default function ConfirmDialog({
  isOpen,
  title = "Confirm Action",
  message = "Are you sure you wish to proceed?",
  confirmText = "Confirm",
  cancelText = "Cancel",
  onConfirm,
  onCancel,
}) {
  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0, 0, 0, 0.65)",
        backdropFilter: "blur(4px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 9999,
        padding: "16px",
      }}
    >
      <div
        style={{
          background: "var(--card-bg, #1a2234)",
          border: "1px solid var(--line, #334155)",
          borderRadius: "12px",
          padding: "24px",
          maxWidth: "440px",
          width: "100%",
          boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.5)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "12px" }}>
          <AlertCircle size={22} color="var(--amber, #f59e0b)" />
          <h3 style={{ margin: 0, fontSize: "16px", fontWeight: 700, color: "var(--text, #f1f5f9)" }}>
            {title}
          </h3>
        </div>
        <p style={{ margin: "0 0 20px 0", color: "var(--muted, #94a3b8)", fontSize: "13px", lineHeight: 1.5 }}>
          {message}
        </p>
        <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
          <button
            onClick={onCancel}
            className="btn btn-secondary"
            style={{ padding: "8px 16px", fontSize: "13px" }}
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            className="btn btn-primary"
            style={{ padding: "8px 16px", fontSize: "13px" }}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}
