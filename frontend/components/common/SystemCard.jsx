import React from "react";

export default function SystemCard({ children, className = "" }) {
  return <section className={`system-card ${className || "bare-card"}`}>{children}</section>;
}
