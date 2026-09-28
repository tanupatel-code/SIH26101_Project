"""
iGOT Karmayogi Ecosystem Integration Service for StatSkill AI.
Provides realistic alignment with Mission Karmayogi's FRAC model
(Framework for Roles, Activities, and Competencies) and the
National Statistical Systems Training Academy (NSSTA / MoSPI) course catalog.
"""

from __future__ import annotations

import copy
from typing import Any

# Official iGOT Karmayogi Course Catalog for India's Official Statistical System
IGOT_COURSE_CATALOG: list[dict[str, Any]] = [
    {
        "id": "iGOT-NSSTA-STAT-101",
        "title": "Sampling Techniques & Multi-Stage Survey Design",
        "provider": "National Statistical Systems Training Academy (NSSTA)",
        "competency_domain": "statisticalMethods",
        "competency_name": "Statistical Methods & Inference",
        "duration": "14 Hours",
        "level": "Intermediate",
        "target_cadres": ["Statistical Investigator", "Junior Statistical Officer", "Senior Statistical Officer"],
        "rating": 4.8,
        "enrolled_count": 3420,
        "frac_competency_code": "FRAC-STAT-METH-02",
        "learning_outcomes": [
            "Formulate stratified multi-stage designs for national sample surveys",
            "Calculate sampling weights and multiplier factors",
            "Compute standard errors and design effects across diverse strata"
        ],
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nssta-sampling-design"
    },
    {
        "id": "iGOT-NSSTA-SNA-201",
        "title": "System of National Accounts (SNA 2008) & GDP Compilation",
        "provider": "Central Statistics Office (CSO) / NSSTA",
        "competency_domain": "nationalAccounts",
        "competency_name": "National Accounts & Macroeconomic Statistics",
        "duration": "18 Hours",
        "level": "Advanced",
        "target_cadres": ["Senior Statistical Officer", "Assistant Director", "Deputy Director"],
        "rating": 4.9,
        "enrolled_count": 2150,
        "frac_competency_code": "FRAC-STAT-SNA-01",
        "learning_outcomes": [
            "Distinguish between Gross Value Added (GVA) and GDP at market prices",
            "Apply supply and use tables (SUT) to balance macroeconomic aggregates",
            "Compile institutional sector accounts for government and household sectors"
        ],
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nssta-sna-gdp"
    },
    {
        "id": "iGOT-MOSPI-CPI-102",
        "title": "Compilation of Consumer Price Index (CPI) & Inflation Metrics",
        "provider": "Price Statistics Division, MoSPI",
        "competency_domain": "priceIndices",
        "competency_name": "Price Indices & Economic Deflators",
        "duration": "10 Hours",
        "level": "Intermediate",
        "target_cadres": ["Statistical Investigator", "Junior Statistical Officer"],
        "rating": 4.7,
        "enrolled_count": 4890,
        "frac_competency_code": "FRAC-STAT-PRICE-03",
        "learning_outcomes": [
            "Collect and validate high-frequency urban and rural price quotations",
            "Implement modified Laspeyres formula with base-year item weights",
            "Detect seasonal price spikes and apply quality adjustment procedures"
        ],
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/mospi-cpi-indices"
    },
    {
        "id": "iGOT-NSSTA-DQ-103",
        "title": "Data Quality Assurance, Auditing & Validation Protocols",
        "provider": "National Statistical Systems Training Academy (NSSTA)",
        "competency_domain": "dataQuality",
        "competency_name": "Data Quality & Survey Validation",
        "duration": "12 Hours",
        "level": "Intermediate",
        "target_cadres": ["Statistical Investigator", "Junior Statistical Officer", "Field Investigator"],
        "rating": 4.8,
        "enrolled_count": 5210,
        "frac_competency_code": "FRAC-STAT-QUAL-01",
        "learning_outcomes": [
            "Execute computer-assisted field editing and range check rules",
            "Deploy modern Hot-Deck and cold-deck statistical imputation routines",
            "Draft data audit certificates for public release of microdata"
        ],
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nssta-data-quality"
    },
    {
        "id": "iGOT-ISRO-GIS-301",
        "title": "Spatial Statistics & Geo-tagging in National Census and Surveys",
        "provider": "National Remote Sensing Centre (NRSC) / MoSPI",
        "competency_domain": "gisSpatial",
        "competency_name": "GIS & Spatial Statistics",
        "duration": "16 Hours",
        "level": "Advanced",
        "target_cadres": ["Junior Statistical Officer", "Senior Statistical Officer", "Data Analyst"],
        "rating": 4.9,
        "enrolled_count": 1840,
        "frac_competency_code": "FRAC-STAT-GIS-04",
        "learning_outcomes": [
            "Geo-reference Enumeration Blocks (EB) with handheld mobile devices",
            "Compute spatial autocorrelation metrics including Moran's I and Getis-Ord Gi*",
            "Produce thematic choropleth maps for policy decision support"
        ],
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nrsc-spatial-stats"
    },
    {
        "id": "iGOT-NIC-PY-202",
        "title": "Python & Data Science for Official Statistical Automation",
        "provider": "National Informatics Centre (NIC) & MoSPI",
        "competency_domain": "dataScienceAi",
        "competency_name": "Data Science & Automation",
        "duration": "20 Hours",
        "level": "Intermediate",
        "target_cadres": ["Statistical Investigator", "Junior Statistical Officer", "Data Analyst"],
        "rating": 4.9,
        "enrolled_count": 6730,
        "frac_competency_code": "FRAC-STAT-CODE-02",
        "learning_outcomes": [
            "Automate recurring tabular reports using Python pandas and openpyxl",
            "Perform regression modeling and time-series decomposition",
            "Construct reproducible reproducible statistical pipelines compliant with NDUAP"
        ],
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nic-python-stats"
    }
]


def get_all_courses(domain: str | None = None, level: str | None = None) -> list[dict[str, Any]]:
    """Return all iGOT Karmayogi catalog courses with optional filtering."""
    results = copy.deepcopy(IGOT_COURSE_CATALOG)
    if domain:
        results = [c for c in results if c["competency_domain"] == domain]
    if level:
        results = [c for c in results if str(c.get("level", "")).lower() == level.lower()]
    return results


def recommend_courses_for_gaps(
    critical_skills: list[dict[str, Any]],
    user_courses: list[dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    """
    Dynamically recommends prioritized iGOT courses based on the officer's
    diagnosed competency gaps.
    """
    user_courses = user_courses or []
    completed_ids = {c.get("id") or c.get("title") for c in user_courses if c.get("status") == "Completed"}

    recommendations: list[dict[str, Any]] = []
    # Sort critical skills by gap descending
    sorted_skills = sorted(critical_skills, key=lambda s: float(s.get("gap", 0)), reverse=True)

    for skill in sorted_skills:
        comp_name = str(skill.get("competency") or "").lower()
        comp_key = str(skill.get("key") or "").lower()

        # Find matching iGOT courses
        matching = [
            c for c in IGOT_COURSE_CATALOG
            if c["id"] not in completed_ids and (
                str(c.get("competency_domain", "")).lower() in comp_key or
                comp_key in str(c.get("competency_domain", "")).lower() or
                str(c.get("competency_name", "")).lower() in comp_name or
                comp_name in str(c.get("competency_name", "")).lower()
            )
        ]

        for course in matching:
            if course not in recommendations:
                c_copy = dict(course)
                gap_val = float(skill.get("gap", 0))
                c_copy["reason_for_recommendation"] = f"Targets your diagnosed gap in {skill.get('competency', 'this domain')} (Gap: {gap_val:.2f})"
                c_copy["priority"] = skill.get("priority", "High")
                recommendations.append(c_copy)

    # If no specific gaps or all matched, append highest-rated catalog courses
    if len(recommendations) < 3:
        for c in sorted(IGOT_COURSE_CATALOG, key=lambda x: float(x.get("rating", 0.0)), reverse=True):
            if c["id"] not in completed_ids and not any(r["id"] == c["id"] for r in recommendations):
                c_copy = dict(c)
                c_copy["reason_for_recommendation"] = "Recommended for foundational capacity building in Official Statistics."
                c_copy["priority"] = "Medium"
                recommendations.append(c_copy)
            if len(recommendations) >= 5:
                break

    return recommendations
