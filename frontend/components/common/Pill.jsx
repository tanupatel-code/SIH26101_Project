import React from "react";

export default function Pill({ children, tone = "neutral", className = "" }) {
  return <span className={`pill ${tone} ${className}`}>{children}</span>;
}
