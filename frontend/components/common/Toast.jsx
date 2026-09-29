import React, { useEffect } from "react";
import { CheckCircle2, AlertCircle, Info, X } from "lucide-react";

export default function Toast({
  message,
  type = "info", // "success" | "error" | "info"
  onClose,
  duration = 4000,
}) {
  useEffect(() => {
    if (!duration || !onClose) return undefined;
    const timer = setTimeout(() => {
      onClose();
    }, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  if (!message) return null;

  const icons = {
    success: <CheckCircle2 size={18} color="var(--green, #10b981)" />,
    error: <AlertCircle size={18} color="var(--red, #ef4444)" />,
    info: <Info size={18} color="var(--cyan, #06b6d4)" />,
  };

  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        position: "fixed",
        bottom: "24px",
        right: "24px",
        zIndex: 9999,
        display: "flex",
        alignItems: "center",
        gap: "12px",
        padding: "12px 18px",
        borderRadius: "8px",
        background: "var(--card-bg, #1a2234)",
        color: "var(--text, #f1f5f9)",
        border: "1px solid var(--line, #334155)",
        boxShadow: "0 10px 25px -5px rgba(0,0,0,0.3)",
        fontSize: "13px",
        maxWidth: "420px",
        animation: "slideInUp 0.25s ease-out",
      }}
    >
      {icons[type] || icons.info}
      <span style={{ flex: 1, lineHeight: 1.4 }}>{message}</span>
      {onClose && (
        <button
          onClick={onClose}
          aria-label="Dismiss message"
          style={{
            background: "transparent",
            border: "none",
            color: "var(--muted, #94a3b8)",
            cursor: "pointer",
            padding: "2px",
            display: "flex",
          }}
        >
          <X size={15} />
        </button>
      )}
    </div>
  );
}
