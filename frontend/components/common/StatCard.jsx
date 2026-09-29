import React from "react";
import SystemCard from "./SystemCard.jsx";
import Progress from "./Progress.jsx";

export default function StatCard({ label, value, suffix, meta, color = "cyan", icon: Icon }) {
  return (
    <SystemCard className={`stat-card ${color}`}>
      <div className="stat-card-top">
        <span>{label}</span>
        {Icon && (
          <span className="stat-icon">
            <Icon size={18} />
          </span>
        )}
      </div>
      <div className="stat-value">
        {value}
        {suffix && <small>{suffix}</small>}
      </div>
      {meta && <div className="stat-meta">{meta}</div>}
      <Progress value={typeof value === "number" ? value : 0} color={color} />
    </SystemCard>
  );
}
