import React from "react";
import { FolderOpen } from "lucide-react";
import SystemCard from "./SystemCard.jsx";

export default function EmptyState({
  title = "No records found",
  message = "No data is currently available in this section.",
  icon: Icon = FolderOpen,
  action = null,
}) {
  return (
    <SystemCard className="empty-panel state-panel">
      <div className="state-icon">
        <Icon size={32} />
      </div>
      <h3>{title}</h3>
      <p>{message}</p>
      {action && <div className="state-action mt-3">{action}</div>}
    </SystemCard>
  );
}
