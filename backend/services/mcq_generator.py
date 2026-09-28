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


def generate_mcqs_from_text(
    text: str,
    num_questions: int = 5,
    difficulty: str = "Intermediate",
    bloom_level: str = "Understanding",
    target_domain: str | None = None,
) -> list[dict[str, Any]]:
    """
    Generates dynamic MCQs from input text or selected statistical concepts.
    Adapts questions to the specified difficulty and Bloom's taxonomy level.
    """
    # Try calling LLM if GEMINI_API_KEY or OPENAI_API_KEY is available
    llm_mcqs = try_llm_mcq_generation(text, num_questions, difficulty, bloom_level, target_domain)
    if llm_mcqs and len(llm_mcqs) >= 1:
        return llm_mcqs[:num_questions]

    # Built-in contextual statistical question engine
    extracted_terms = extract_keywords_from_text(text) if text else []
    
    # Filter or prioritize questions by domain or extracted terms
    pool = list(OFFICIAL_STATS_CONCEPTS)
    if target_domain:
        matched = [q for q in pool if q["domain"] == target_domain]
        if matched:
            pool = matched

    # If text has specific keywords, prioritize related concepts
    if extracted_terms:
        def relevance_score(q: dict[str, Any]) -> int:
            q_text = (q["question"] + " " + q["topic"]).lower()
            return sum(1 for term in extracted_terms if term in q_text)
        pool = sorted(pool, key=relevance_score, reverse=True)

    # If document has sentences that can form custom questions
    custom_doc_mcqs = generate_document_specific_mcqs(text, difficulty, bloom_level, target_domain)
    combined_pool = custom_doc_mcqs + pool

    # Ensure we return the requested number of questions
    selected_questions: list[dict[str, Any]] = []
    seen_texts = set()

    for item in combined_pool:
        q_text = item["question"]
        if q_text in seen_texts:
            continue
        seen_texts.add(q_text)

        # Clone and format question
        q_copy = dict(item)
        q_copy["id"] = f"MCQ-{len(selected_questions) + 1:03d}"
        q_copy["difficulty"] = difficulty
        if "bloom_level" not in q_copy:
            q_copy["bloom_level"] = bloom_level
        selected_questions.append(q_copy)

        if len(selected_questions) >= num_questions:
            break

    # If still need more, duplicate with variation
    while len(selected_questions) < num_questions and pool:
        base = pool[len(selected_questions) % len(pool)]
        cloned = dict(base)
        cloned["id"] = f"MCQ-{len(selected_questions) + 1:03d}"
        cloned["difficulty"] = difficulty
        selected_questions.append(cloned)

    return selected_questions[:num_questions]


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
    domain: str | None
) -> list[dict[str, Any]] | None:
    """Invokes Gemini or OpenAI API if API keys are configured."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not gemini_key and not openai_key:
        return None

    prompt = f"""
You are an expert psychometrician and statistical education designer for India's Official Statistical System (MoSPI/NSSTA).
Generate exactly {num_questions} multiple-choice questions based on the following learning material.
Difficulty Level: {difficulty}
Bloom's Taxonomy Level: {bloom_level}
Target Competency Domain: {domain or 'Official Statistics'}

LEARNING MATERIAL:
{text[:4000]}

Format output as a valid JSON array of objects with keys:
- "question": string
- "topic": string
- "options": list of 4 strings
- "correct_index": integer (0, 1, 2, or 3)
- "bloom_level": string
- "domain": string
- "explanation": string (clear educational rationale for the correct answer and why others are wrong)
"""

    try:
        import httpx
        if gemini_key:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"response_mime_type": "application/json"}
            }
            res = httpx.post(url, json=payload, timeout=20.0)
            if res.status_code == 200:
                data = res.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(raw_text)
                if isinstance(parsed, list):
                    return parsed
        elif openai_key:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"}
            }
            res = httpx.post(url, json=payload, headers=headers, timeout=20.0)
            if res.status_code == 200:
                data = res.json()
                raw_text = data["choices"][0]["message"]["content"]
                parsed = json.loads(raw_text)
                if isinstance(parsed, dict) and "questions" in parsed:
                    return parsed["questions"]
                elif isinstance(parsed, list):
                    return parsed
    except Exception as exc:
        print(f"LLM API generation notice (falling back to local statistical engine): {exc}")

    return None
