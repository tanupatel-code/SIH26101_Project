import React from "react";

export default function Progress({ value, color = "cyan" }) {
  const width = Math.max(0, Math.min(100, Number(value) || 0));
  return (
    <div className="progress" role="progressbar" aria-valuenow={width} aria-valuemin={0} aria-valuemax={100}>
      <span className={`progress-fill ${color} p-${width}`} />
    </div>
  );
}
