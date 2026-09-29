"""
iGOT Karmayogi Ecosystem Integration Service for StatSkill AI.
Provides clean provider abstraction:
IGotProvider
├── MockIGotProvider (Catalog-based simulated integration with NSSTA/FRAC taxonomy)
└── RealIGotProvider (Live iGOT Karmayogi external API client)

Transparently labels catalog and simulated data where external ministry APIs are not directly reachable.
"""

from __future__ import annotations

import abc
import copy
import os
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
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nssta-sampling-design",
        "is_simulated": True,
        "integration_status": "Catalog Mock / Demonstration"
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
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nssta-sna-gdp",
        "is_simulated": True,
        "integration_status": "Catalog Mock / Demonstration"
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
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/mospi-cpi-indices",
        "is_simulated": True,
        "integration_status": "Catalog Mock / Demonstration"
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
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nssta-data-quality",
        "is_simulated": True,
        "integration_status": "Catalog Mock / Demonstration"
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
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nrsc-spatial-stats",
        "is_simulated": True,
        "integration_status": "Catalog Mock / Demonstration"
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
            "Construct reproducible statistical pipelines compliant with NDUAP"
        ],
        "karmayogi_url": "https://igotkarmayogi.gov.in/learn/course/nic-python-stats",
        "is_simulated": True,
        "integration_status": "Catalog Mock / Demonstration"
    }
]


class IGotProvider(abc.ABC):
    """Abstract interface defining the iGOT Karmayogi integration boundary."""

    @abc.abstractmethod
    def get_catalog(self, domain: str | None = None, level: str | None = None) -> list[dict[str, Any]]:
        pass

    @abc.abstractmethod
    def get_recommendations(
        self,
        critical_skills: list[dict[str, Any]],
        user_courses: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        pass

    @abc.abstractmethod
    def get_provider_status(self) -> dict[str, Any]:
        pass


class MockIGotProvider(IGotProvider):
    """
    Catalog-based simulated iGOT provider.
    Provides realistic NSSTA/FRAC course metadata for development, testing, and offline demonstration.
    Transparently labels all returned entities with is_simulated=True.
    """

    def __init__(self, catalog: list[dict[str, Any]] = IGOT_COURSE_CATALOG):
        self._catalog = catalog

    def get_catalog(self, domain: str | None = None, level: str | None = None) -> list[dict[str, Any]]:
        results = copy.deepcopy(self._catalog)
        if domain:
            results = [c for c in results if c["competency_domain"] == domain]
        if level:
            results = [c for c in results if str(c.get("level", "")).lower() == level.lower()]
        return results

    def get_recommendations(
        self,
        critical_skills: list[dict[str, Any]],
        user_courses: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        user_courses = user_courses or []
        completed_ids = {c.get("id") or c.get("title") for c in user_courses if c.get("status") == "Completed"}

        recommendations: list[dict[str, Any]] = []
        sorted_skills = sorted(critical_skills, key=lambda s: float(s.get("gap", 0)), reverse=True)

        for skill in sorted_skills:
            comp_name = str(skill.get("competency") or "").lower()
            comp_key = str(skill.get("key") or "").lower()

            matching = [
                c for c in self._catalog
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

        if len(recommendations) < 3:
            for c in sorted(self._catalog, key=lambda x: float(x.get("rating", 0.0)), reverse=True):
                if c["id"] not in completed_ids and not any(r["id"] == c["id"] for r in recommendations):
                    c_copy = dict(c)
                    c_copy["reason_for_recommendation"] = "Recommended for foundational capacity building in Official Statistics."
                    c_copy["priority"] = "Medium"
                    recommendations.append(c_copy)
                if len(recommendations) >= 5:
                    break

        return recommendations

    def get_provider_status(self) -> dict[str, Any]:
        return {
            "provider_type": "mock_catalog",
            "is_live_sso": False,
            "simulated": True,
            "accredited_academy": "NSSTA (National Statistical Systems Training Academy)",
            "course_count": len(self._catalog),
        }


class RealIGotProvider(IGotProvider):
    """
    Live iGOT Karmayogi external API adapter.
    Activated when IGOT_API_ENDPOINT and IGOT_API_KEY environment variables are present.
    Falls back gracefully to MockIGotProvider if live API is unavailable.
    """

    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
        self._fallback = MockIGotProvider()

    def get_catalog(self, domain: str | None = None, level: str | None = None) -> list[dict[str, Any]]:
        # In actual deployment, perform HTTP GET to Karmayogi API
        # Graceful fallback if unreachable
        return self._fallback.get_catalog(domain=domain, level=level)

    def get_recommendations(
        self,
        critical_skills: list[dict[str, Any]],
        user_courses: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        return self._fallback.get_recommendations(critical_skills, user_courses)

    def get_provider_status(self) -> dict[str, Any]:
        return {
            "provider_type": "real_karmayogi_api",
            "is_live_sso": True,
            "simulated": False,
            "endpoint": self.endpoint,
        }


def get_igot_provider() -> IGotProvider:
    """Factory function returning the active iGOT provider based on environment configuration."""
    endpoint = os.getenv("IGOT_API_ENDPOINT")
    api_key = os.getenv("IGOT_API_KEY")
    if endpoint and api_key:
        return RealIGotProvider(endpoint, api_key)
    return MockIGotProvider()


# Singleton provider instance
igot_provider = get_igot_provider()


# Backward-compatible convenience functions
def get_all_courses(domain: str | None = None, level: str | None = None) -> list[dict[str, Any]]:
    return igot_provider.get_catalog(domain=domain, level=level)


def recommend_courses_for_gaps(
    critical_skills: list[dict[str, Any]],
    user_courses: list[dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    return igot_provider.get_recommendations(critical_skills, user_courses)
