import React from "react";
import { Activity } from "lucide-react";
import SystemCard from "./SystemCard.jsx";

export default function LoadingState({ message = "Loading data..." }) {
  return (
    <SystemCard className="empty-panel state-panel">
      <div className="state-icon spin">
        <Activity size={32} />
      </div>
      <h3>{message}</h3>
      <p>Synchronizing with National Statistical System Directory.</p>
    </SystemCard>
  );
}
