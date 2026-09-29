import React from "react";

export default function PageHeading({ kicker, title, subtitle, actions }) {
  return (
    <div className="page-heading system-card">
      <div>
        {kicker && <div className="kicker">{kicker}</div>}
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {actions && <div className="heading-actions">{actions}</div>}
    </div>
  );
}
