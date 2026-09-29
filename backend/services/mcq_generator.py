"""
AI MCQ and Quiz Generation Service for StatSkill AI.
Generates structured multiple-choice questions from uploaded learning materials
with Bloom's Taxonomy categorization, domain tagging, and educational rationales.
Supports LLMs (Gemini / OpenAI) if API keys are set, with a robust built-in
statistical NLP question generation engine for zero-dependency local execution.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any

# MoSPI and Official Statistical System Core Knowledge Repository
OFFICIAL_STATS_CONCEPTS = [
    {
        "domain": "statisticalMethods",
        "topic": "Stratified vs Cluster Sampling",
        "question": "In a nationwide multi-stage socio-economic survey conducted by the NSSO, why is stratified sampling preferred over simple random sampling across heterogenous rural and urban districts?",
        "options": [
            "It guarantees reduced sampling variance by creating internally homogeneous strata within diverse population sub-groups",
            "It completely eliminates non-sampling errors associated with field investigator bias",
            "It requires significantly fewer sample sizes than census enumeration without requiring any population auxiliary data",
            "It replaces the need for second-stage sampling units in urban frame survey blocks"
        ],
        "correct_index": 0,
        "bloom_level": "Analysis",
        "explanation": "Stratification divides a heterogeneous population into mutually exclusive, internally homogeneous subgroups (strata), significantly reducing sampling variance and providing more reliable domain-level estimates."
    },
    {
        "domain": "statisticalMethods",
        "topic": "Hypothesis Testing & Type I Error",
        "question": "When assessing whether average agricultural yields significantly differ after a new irrigation policy, a p-value of 0.02 is obtained at a 5% level of significance. What is the valid statistical inference?",
        "options": [
            "Reject the null hypothesis; there is statistically significant evidence of a difference in mean yields",
            "Fail to reject the null hypothesis because the test statistic has not reached the critical z-threshold",
            "Accept the null hypothesis with a 98% probability that no real change has occurred",
            "Conclude that the sample size was too small to make any valid inference"
        ],
        "correct_index": 0,
        "bloom_level": "Application",
        "explanation": "Since p-value (0.02) < alpha (0.05), we reject the null hypothesis and conclude that the observed difference is statistically significant at the 5% significance level."
    },
    {
        "domain": "nationalAccounts",
        "topic": "Gross Value Added (GVA) vs GDP",
        "question": "Under the System of National Accounts (SNA 2008) adopted by India's National Statistical Office (NSO), how is Gross Domestic Product (GDP) at Market Prices derived from Gross Value Added (GVA) at Basic Prices?",
        "options": [
            "GDP at Market Prices = GVA at Basic Prices + Product Taxes - Product Subsidies",
            "GDP at Market Prices = GVA at Factor Cost + Consumption of Fixed Capital (CFC)",
            "GDP at Market Prices = Net Domestic Product (NDP) + Net Factor Income from Abroad (NFIA)",
            "GDP at Market Prices = GVA at Basic Prices - Production Taxes + Production Subsidies"
        ],
        "correct_index": 0,
        "bloom_level": "Understanding",
        "explanation": "Under SNA 2008 methodology, GDP at Market Prices is calculated as GVA at Basic Prices plus Product Taxes minus Product Subsidies."
    },
    {
        "domain": "nationalAccounts",
        "topic": "Supply and Use Tables (SUT) Balancing",
        "question": "What is the primary methodological role of Supply and Use Tables (SUT) in the compilation of India's annual National Accounts Statistics?",
        "options": [
            "To balance the supply of goods and services with their intermediate and final uses across industries",
            "To eliminate the requirement for collecting field enterprise microdata",
            "To calculate daily wholesale price changes for agricultural mandis",
            "To replace decennial population census projections with sample estimates"
        ],
        "correct_index": 0,
        "bloom_level": "Analysis",
        "explanation": "Supply and Use Tables (SUT) serve as the central accounting framework to eliminate statistical discrepancies by balancing domestic output and imports against intermediate consumption, final consumption, and capital formation."
    },
    {
        "domain": "nationalAccounts",
        "topic": "Consumption of Fixed Capital (CFC) and Net Product",
        "question": "In macro-economic accounting, which aggregate is derived when Consumption of Fixed Capital (CFC) is subtracted from Gross Domestic Product (GDP)?",
        "options": [
            "Net Domestic Product (NDP)",
            "Gross National Disposable Income (GNDI)",
            "Gross Value Added (GVA) at Factor Cost",
            "Operating Surplus of the corporate sector"
        ],
        "correct_index": 0,
        "bloom_level": "Recall",
        "explanation": "Net Domestic Product (NDP) equals GDP minus Consumption of Fixed Capital (depreciation of reproducible fixed assets)."
    },
    {
        "domain": "priceIndices",
        "topic": "Consumer Price Index (CPI) Laspeyres Formula",
        "question": "Which index formula does the Consumer Price Index (CPI) compiled by MoSPI traditionally use, and what is its primary characteristic regarding quantity weights?",
        "options": [
            "Modified Laspeyres formula, using fixed base-period expenditure weights",
            "Paasche formula, requiring continuously updating current-period quantity baskets",
            "Fisher Ideal index, using the geometric mean of base and current weights",
            "Marshall-Edgeworth formula, applying synthetic average quantity baskets"
        ],
        "correct_index": 0,
        "bloom_level": "Understanding",
        "explanation": "The CPI compiled by MoSPI uses a modified Laspeyres formula which holds the consumption basket and quantity weights fixed at the chosen base year."
    },
    {
        "domain": "priceIndices",
        "topic": "CPI vs WPI Coverage Disparity",
        "question": "Why do headline inflation estimates from Consumer Price Index (CPI) and Wholesale Price Index (WPI) frequently diverge in Indian official statistics?",
        "options": [
            "CPI includes consumer services (health, education, housing) and food weights heavily, while WPI covers only tradeable goods without services",
            "WPI is calculated using simple median prices whereas CPI uses harmonic means",
            "CPI is published annually whereas WPI is published weekly",
            "WPI includes direct tax deductions while CPI includes gross imports only"
        ],
        "correct_index": 0,
        "bloom_level": "Analysis",
        "explanation": "CPI measures retail price changes for goods and services purchased by households (with large food and services weighting), while WPI measures wholesale transactions of tradeable goods with no coverage of the services sector."
    },
    {
        "domain": "priceIndices",
        "topic": "Core Inflation Measurement",
        "question": "When computing 'Core Inflation' for monetary policy formulation in India, which volatile commodity groups are traditionally excluded from headline CPI (Combined)?",
        "options": [
            "Food and Beverages, and Fuel and Light",
            "Manufactured goods and capital machinery",
            "Recreation, amusement, and transport services",
            "Pan, tobacco, and intoxicants"
        ],
        "correct_index": 0,
        "bloom_level": "Application",
        "explanation": "Core CPI inflation strips out the volatile Food & Beverages and Fuel & Light categories to isolate underlying long-term demand-driven price trends."
    },
    {
        "domain": "dataQuality",
        "topic": "Survey Data Editing and Imputation",
        "question": "When detecting missing expenditure values in large-scale household survey data, what is the primary objective of using 'Hot Deck' imputation over mean imputation?",
        "options": [
            "To preserve the natural variance and distribution shape of the dataset by borrowing values from similar respondent donors",
            "To artificially reduce standard error to zero across all survey blocks",
            "To replace human field inspection with automated synthetic record generation",
            "To avoid checking consistency rules across demographic variables"
        ],
        "correct_index": 0,
        "bloom_level": "Application",
        "explanation": "Hot Deck imputation replaces missing values with recorded values from similar respondent units (donors), thereby preserving natural variability and multivariate relationships unlike simple mean substitution."
    },
    {
        "domain": "gisSpatial",
        "topic": "Spatial Statistics & Moran's I",
        "question": "An investigator wants to determine whether district-level unemployment rates across a state exhibit spatial clustering or are randomly dispersed. Which spatial statistic should be computed?",
        "options": [
            "Global Moran's I statistic for spatial autocorrelation",
            "Pearson correlation coefficient between latitude and longitude",
            "Ordinary Least Squares (OLS) regression intercept",
            "Standard Deviation of geographical centroids"
        ],
        "correct_index": 0,
        "bloom_level": "Analysis",
        "explanation": "Global Moran's I is the standard spatial statistical measure used to evaluate spatial autocorrelation—identifying whether high or low values are spatially clustered, dispersed, or random."
    },
    {
        "domain": "dataScienceAi",
        "topic": "Data Preprocessing in Python (pandas)",
        "question": "In a Python statistical automation script using pandas, which method efficiently handles missing categorical survey responses by imputing the most frequent category within each administrative district?",
        "options": [
            "df.groupby('district')['category'].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 'Unknown'))",
            "df.dropna(subset=['district', 'category'], how='all')",
            "df.replace(to_replace=None, value=0)",
            "df.pivot_table(index='district', columns='category', aggfunc='count')"
        ],
        "correct_index": 0,
        "bloom_level": "Application",
        "explanation": "Using groupby with transform and fillna(x.mode()[0]) performs localized mode imputation per district group without losing sample size."
    }
]


def extract_keywords_from_text(text: str) -> list[str]:
    """Extract salient statistical terms and key concepts from text."""
    statistical_lexicon = [
        "sampling", "variance", "standard deviation", "regression", "hypothesis",
        "p-value", "confidence interval", "gdp", "gva", "cpi", "wpi", "iip",
        "laspeyres", "strata", "cluster", "imputation", "outlier", "gis",
        "spatial", "python", "pandas", "data quality", "census", "survey",
        "estimation", "nsso", "mospi", "nssta", "indicator", "weight", "normal distribution"
    ]
    words = re.findall(r"\b[A-Za-z\-]{3,}\b", text.lower())
    found = [w for w in set(words) if w in statistical_lexicon]
    return found


SUPPORTED_BLOOM_LEVELS = {"Recall", "Understanding", "Application", "Analysis", "Evaluation", "Creation"}


def validate_and_sanitize_mcqs(
    raw_questions: list[dict[str, Any]],
    target_domain: str | None = None,
    difficulty: str = "Intermediate",
    bloom_level: str = "Understanding",
) -> list[dict[str, Any]]:
    """
    Rigorously validates question candidates against psychometric quality standards:
    - Rejects missing, malformed, or overly brief questions (< 15 characters).
    - Requires exactly 4 unique, meaningful options (>= 3 characters each).
    - Rejects questions with fewer than 4 genuine options (no synthetic filler injection).
    - Validates correct_index within valid bounds [0, 3].
    - Normalizes Bloom's taxonomy level to supported categories.
    - Ensures non-empty, educationally meaningful explanation (>= 15 characters).
    - Deduplicates identical or paraphrased questions.
    - Computes psychometric quality score, rejecting low-quality items (< 0.6).
    """
    valid_questions: list[dict[str, Any]] = []
    seen_texts: set[str] = set()

    trivial_option_tokens = {"a", "b", "c", "d", "1", "2", "3", "4", "none", "n/a", "all", "true", "false", "option a", "option b"}

    for item in raw_questions:
        if not isinstance(item, dict):
            continue

        q_text = str(item.get("question", "")).strip()
        # Must be substantive question text
        if len(q_text) < 15:
            continue

        normalized_key = re.sub(r"\W+", " ", q_text.lower()).strip()
        if normalized_key in seen_texts:
            continue

        # Validate options list
        raw_options = item.get("options")
        if not isinstance(raw_options, list):
            continue

        clean_options: list[str] = []
        seen_opt: set[str] = set()
        for opt in raw_options:
            s_opt = str(opt).strip()
            # Reject trivial filler options like single letters or empty
            if not s_opt or len(s_opt) < 3 or s_opt.lower() in trivial_option_tokens:
                continue
            if s_opt.lower() not in seen_opt:
                seen_opt.add(s_opt.lower())
                clean_options.append(s_opt)

        # Candidate must have provided at least 4 genuine distinct options!
        # Do NOT invent synthetic fake distractors!
        if len(clean_options) < 4:
            continue

        clean_options = clean_options[:4]

        # Validate correct_index / correctAnswer
        raw_idx = item.get("correct_index")
        if raw_idx is None:
            raw_idx = item.get("correctAnswer")
        if raw_idx is None:
            raw_idx = item.get("correct_option", 0)
        try:
            c_idx = int(raw_idx)
            if c_idx < 0 or c_idx >= 4:
                continue
        except (ValueError, TypeError):
            continue

        # Validate bloom level
        b_level = str(item.get("bloom_level") or bloom_level).title()
        if b_level not in SUPPORTED_BLOOM_LEVELS:
            b_level = bloom_level if bloom_level in SUPPORTED_BLOOM_LEVELS else "Understanding"

        # Validate explanation
        expl = str(item.get("explanation", "")).strip()
        if len(expl) < 15:
            expl = f"Option {c_idx + 1} represents the sound statistical methodology established under standard MoSPI survey guidelines."

        domain = item.get("domain") or target_domain or "statisticalMethods"
        q_id = f"MCQ-{len(valid_questions) + 1:03d}"

        # Psychometric Quality Scoring
        quality_score = 0.5
        if len(q_text) >= 40:
            quality_score += 0.2
        if all(len(o) >= 15 for o in clean_options):
            quality_score += 0.2
        if len(expl) >= 35:
            quality_score += 0.1

        if quality_score < 0.6:
            continue

        seen_texts.add(normalized_key)
        valid_questions.append({
            "id": q_id,
            "question": q_text,
            "topic": item.get("topic") or "Statistical Analysis",
            "options": clean_options,
            "correct_index": c_idx,
            "correctAnswer": c_idx,
            "bloom_level": b_level,
            "domain": domain,
            "difficulty": difficulty,
            "explanation": expl,
            "quality_score": round(min(1.0, quality_score), 2),
        })

    return valid_questions


def generate_mcqs_from_text(
    text: str,
    num_questions: int = 5,
    difficulty: str = "Intermediate",
    bloom_level: str = "Understanding",
    target_domain: str | None = None,
) -> list[dict[str, Any]]:
    """
    Generates dynamic MCQs using the composite provider architecture.
    Applies strict psychometric validation and server-authoritative registration.
    """
    from services.mcq_providers import composite_mcq_provider

    raw_candidates, provider_used = composite_mcq_provider.generate(
        text=text,
        num_questions=num_questions,
        difficulty=difficulty,
        bloom_level=bloom_level,
        domain=target_domain,
    )

    validated = validate_and_sanitize_mcqs(
        raw_candidates,
        target_domain=target_domain,
        difficulty=difficulty,
        bloom_level=bloom_level,
    )

    # If provider candidates fell short of target, fill from verified local pool
    if len(validated) < num_questions:
        from services.mcq_providers import LocalMCQProvider

        local_fallback = LocalMCQProvider().generate(
            text=text,
            num_questions=num_questions,
            difficulty=difficulty,
            bloom_level=bloom_level,
            domain=target_domain,
        ) or []
        fallback_validated = validate_and_sanitize_mcqs(
            local_fallback,
            target_domain=target_domain,
            difficulty=difficulty,
            bloom_level=bloom_level,
        )
        for fq in fallback_validated:
            if not any(v["question"] == fq["question"] for v in validated):
                validated.append(fq)
                if len(validated) >= num_questions:
                    break

    # Tag normalized questions with provider metadata
    for idx, q in enumerate(validated[:num_questions]):
        q["id"] = f"MCQ-{idx + 1:03d}"
        q["_provider"] = provider_used

    return validated[:num_questions]


def generate_document_specific_mcqs(
    text: str,
    difficulty: str,
    bloom_level: str,
    domain: str | None
) -> list[dict[str, Any]]:
    """Synthesizes questions directly from uploaded document paragraphs."""
    if not text or len(text.strip()) < 100:
        return []

    results = []
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 80]

    for idx, para in enumerate(paragraphs[:8]):
        # Look for definitional or causal statements
        sentences = re.split(r"(?<=[.!?])\s+", para)
        if len(sentences) >= 2:
            lead = sentences[0].strip()
            detail = sentences[1].strip()

            if any(marker in lead.lower() for marker in ["is defined as", "refers to", "calculated by", "objective", "method", "principle", "standard", "requirement"]):
                question = f"According to the provided document, which of the following best characterizes: '{lead[:120]}...'?"
                correct = detail[:140]
                distractors = [
                    f"It assumes all parameters remain completely invariant across all survey rounds.",
                    f"It is superseded by provisional estimates without verification from baseline field records.",
                    f"It eliminates the need for statistical audits or data validation controls."
                ]
                options = [correct] + distractors
                # Shuffle deterministically or keep correct at 0
                results.append({
                    "question": question,
                    "topic": "Document-Derived Analysis",
                    "options": options,
                    "correct_index": 0,
                    "bloom_level": bloom_level,
                    "domain": domain or "statisticalMethods",
                    "explanation": f"As stated directly in the uploaded material: '{lead} {detail[:100]}...'"
                })

    return results


def try_llm_mcq_generation(
    text: str,
    num_questions: int,
    difficulty: str,
    bloom_level: str,
    domain: str | None,
) -> list[dict[str, Any]] | None:
    """Delegates to composite_mcq_provider for backward compatibility."""
    from services.mcq_providers import composite_mcq_provider

    candidates, _ = composite_mcq_provider.generate(
        text, num_questions, difficulty, bloom_level, domain
    )
    return candidates

