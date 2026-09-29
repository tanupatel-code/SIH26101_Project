import React, { useEffect, useState } from "react";
import { ExternalLink, Search } from "lucide-react";
import { tr } from "../i18n/index.js";
import {
  EmptyState,
  LoadingState,
  PageHeading,
  SystemCard,
} from "../components/common/index.js";
import { apiGetDataSources } from "../services/api/client.js";

export default function DataSourcesPage({ lang }) {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterDomain, setFilterDomain] = useState("all");
  const [search, setSearch] = useState("");

  useEffect(() => {
    let mounted = true;
    apiGetDataSources()
      .then((data) => {
        if (mounted) {
          setSources(data?.data_sources || []);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (mounted) {
          setError(err.message);
          setLoading(false);
        }
      });
    return () => {
      mounted = false;
    };
  }, []);

  const domains = [
    { key: "all", label: "All Data Sources" },
    { key: "statisticalMethods", label: "Surveys & Sampling (PLFS/HCES/ASUSE)" },
    { key: "priceIndices", label: "Price Indices (CPI)" },
    { key: "nationalAccounts", label: "National Accounts (GDP/NAS)" },
    { key: "dataQuality", label: "Industrial & Enterprise Records (ASI/IIP)" },
    { key: "gis", label: "Geospatial & Remote Sensing" },
    { key: "python", label: "Open Government Data APIs" },
  ];

  const filtered = sources.filter((ds) => {
    const matchesDomain = filterDomain === "all" || ds.domain === filterDomain;
    const q = search.toLowerCase();
    const matchesSearch =
      !search ||
      (ds.name || "").toLowerCase().includes(q) ||
      (ds.division || "").toLowerCase().includes(q) ||
      (ds.description || "").toLowerCase().includes(q) ||
      (ds.key_variables || []).some((v) => v.toLowerCase().includes(q));
    return matchesDomain && matchesSearch;
  });

  return (
    <div className="stack">
      <PageHeading
        kicker="NATIONAL STATISTICAL SYSTEM ARCHITECTURE"
        title={tr(lang, "dataSources")}
        subtitle="Primary statistical surveys, price indices, administrative registers, and microdata catalogs coordinated by MoSPI & National Statistical Office (NSO)."
        actions={
          <div className="search">
            <Search size={15} />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search surveys, indicators, divisions..."
              aria-label="Search data sources"
            />
          </div>
        }
      />

      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", margin: "4px 0" }}>
        {domains.map((d) => (
          <button
            key={d.key}
            type="button"
            className={filterDomain === d.key ? "primary-btn" : "secondary-btn"}
            onClick={() => setFilterDomain(d.key)}
            style={{ fontSize: "11px", padding: "6px 12px" }}
          >
            {d.label}
          </button>
        ))}
      </div>

      {loading && <LoadingState message="Loading official statistical registry..." />}

      {error && (
        <SystemCard style={{ padding: "20px", color: "#dc2626" }}>
          <strong>Error loading data sources:</strong> {error}
        </SystemCard>
      )}

      {!loading && !error && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(440px, 1fr))",
            gap: "16px",
          }}
        >
          {filtered.map((ds) => (
            <SystemCard
              key={ds.id}
              style={{
                display: "flex",
                flexDirection: "column",
                padding: "20px",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                  gap: "10px",
                  marginBottom: "8px",
                }}
              >
                <div>
                  <span
                    className="edu-badge cadre-nssta"
                    style={{ marginBottom: "6px", display: "inline-block" }}
                  >
                    {ds.id}
                  </span>
                  <h3
                    style={{
                      margin: "4px 0 2px",
                      fontSize: "1.05rem",
                      fontWeight: "700",
                      color: "#0f172a",
                    }}
                  >
                    {ds.name}
                  </h3>
                  <span style={{ fontSize: "0.78rem", color: "#64748b" }}>
                    {ds.division}
                  </span>
                </div>
                <span
                  className="edu-badge bloom-understanding"
                  style={{ whiteSpace: "nowrap" }}
                >
                  {ds.frequency}
                </span>
              </div>

              <p
                style={{
                  fontSize: "0.84rem",
                  color: "#334155",
                  lineHeight: "1.5",
                  margin: "8px 0 12px",
                }}
              >
                {ds.description}
              </p>

              <div style={{ margin: "6px 0" }}>
                <span
                  style={{
                    fontSize: "0.74rem",
                    fontWeight: "600",
                    textTransform: "uppercase",
                    color: "#64748b",
                    display: "block",
                    marginBottom: "4px",
                  }}
                >
                  Key Variables & Metadata
                </span>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                  {(ds.key_variables || []).map((v, i) => (
                    <span
                      key={i}
                      style={{
                        fontSize: "0.74rem",
                        background: "#f1f5f9",
                        color: "#334155",
                        padding: "2px 8px",
                        borderRadius: "4px",
                        border: "1px solid #e2e8f0",
                      }}
                    >
                      {v}
                    </span>
                  ))}
                </div>
              </div>

              {ds.learning_use_case && (
                <div
                  style={{
                    background: "#f8fafc",
                    border: "1px solid #e2e8f0",
                    borderRadius: "8px",
                    padding: "10px",
                    margin: "10px 0",
                  }}
                >
                  <span
                    style={{
                      fontSize: "0.74rem",
                      fontWeight: "700",
                      color: "#0f2e5a",
                      display: "block",
                      marginBottom: "2px",
                    }}
                  >
                    Capacity Building Application
                  </span>
                  <p
                    style={{
                      margin: 0,
                      fontSize: "0.78rem",
                      color: "#475569",
                    }}
                  >
                    {ds.learning_use_case}
                  </p>
                </div>
              )}

              <div
                style={{
                  marginTop: "auto",
                  paddingTop: "12px",
                  borderTop: "1px solid #e2e8f0",
                  display: "flex",
                  gap: "8px",
                  justifyContent: "flex-end",
                }}
              >
                {ds.microdata_catalog && (
                  <a
                    href={ds.microdata_catalog}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="secondary-btn"
                    style={{
                      fontSize: "11px",
                      textDecoration: "none",
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "5px",
                    }}
                  >
                    Microdata Catalog <ExternalLink size={12} />
                  </a>
                )}
                {ds.access_url && (
                  <a
                    href={ds.access_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="primary-btn"
                    style={{
                      fontSize: "11px",
                      textDecoration: "none",
                      display: "inline-flex",
                      alignItems: "center",
                      gap: "5px",
                    }}
                  >
                    MoSPI Portal <ExternalLink size={12} />
                  </a>
                )}
              </div>
            </SystemCard>
          ))}
          {filtered.length === 0 && (
            <EmptyState
              title="No statistical datasets match your filter"
              message={`No sources found for '${search}' in ${filterDomain}.`}
            />
          )}
        </div>
      )}
    </div>
  );
}
