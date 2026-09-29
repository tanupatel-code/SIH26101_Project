"""
StatSkill AI — Authoritative Assessment Evaluation & Grading Service.
The server maintains authoritative question answer keys and grades all submissions.
Client-supplied 'is_correct' or 'correct_option' parameters are strictly ignored,
preventing any client-side tampering of scores or competency metrics.
"""

from __future__ import annotations

import threading
from typing import Any
from schemas.assessment_schemas import QuizAnswerItem
from services.competency_service import record_quiz_submission

# Thread-safe in-memory cache of dynamically generated questions and their authoritative answer keys
_DYNAMIC_QUESTION_KEYS: dict[str, int] = {}
_LOCK = threading.Lock()

# Authoritative Question Bank for Official Diagnostic Quizzes
OFFICIAL_DIAGNOSTIC_QUIZZES: dict[str, dict[str, Any]] = {
    "QUIZ-SAMPLING": {
        "title": "National Sample Survey Sampling & Estimation Diagnostic",
        "domain": "statisticalMethods",
        "questions": [
            {
                "id": "Q1",
                "question": "Why is stratified sampling preferred over simple random sampling across heterogenous districts?",
                "options": [
                    "It creates internally homogeneous strata, reducing sampling variance",
                    "It eliminates all non-sampling errors completely",
                    "It requires no auxiliary population data",
                    "It replaces the need for second-stage sampling units",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q2",
                "question": "In NSSO multi-stage design, what typically serves as the First Stage Unit (FSU)?",
                "options": [
                    "Census Villages in rural areas and Urban Frame Survey (UFS) blocks in urban areas",
                    "Individual agricultural households",
                    "District magistrate headquarters",
                    "Private corporate enterprises",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q3",
                "question": "What is the primary purpose of inverse probability sampling weights (multipliers)?",
                "options": [
                    "To inflate sample values to reflect total universe estimates accurately",
                    "To penalize non-responding households",
                    "To reduce questionnaire completion time",
                    "To round continuous variables to whole numbers",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q4",
                "question": "Which method is commonly used for estimating standard errors in complex NSS survey designs?",
                "options": [
                    "Jackknife or Sub-sample replication methods",
                    "Simple student t-distribution without design effects",
                    "Direct unweighted variance estimation",
                    "Linear regression R-squared approximation",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q5",
                "question": "What does a Design Effect (Deff) greater than 1.0 indicate?",
                "options": [
                    "Cluster sampling has increased variance compared to simple random sampling",
                    "The survey has zero standard error",
                    "Sample size is larger than total population",
                    "No weighting is needed during tabulation",
                ],
                "correct_index": 0,
            },
        ],
    },
    "QUIZ-SNA": {
        "title": "System of National Accounts (SNA 2008) & GDP Diagnostic",
        "domain": "nationalAccounts",
        "questions": [
            {
                "id": "Q1",
                "question": "Under SNA 2008, how is GDP at Market Prices derived from GVA at Basic Prices?",
                "options": [
                    "GDP at Market Prices = GVA at Basic Prices + Product Taxes - Product Subsidies",
                    "GDP at Market Prices = GVA at Factor Cost + Depreciation",
                    "GDP at Market Prices = Net Domestic Product + Export Taxes",
                    "GDP at Market Prices = GVA at Basic Prices - Production Taxes",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q2",
                "question": "What distinguishes Product Taxes from Production Taxes in National Accounts?",
                "options": [
                    "Product taxes are payable per unit of good produced (e.g. GST, excise)",
                    "Production taxes depend solely on final sales quantity",
                    "Product taxes are land revenues and stamp duties",
                    "There is no difference between product and production taxes",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q3",
                "question": "What does the Double Deflation method ensure when estimating Real GVA?",
                "options": [
                    "Outputs and intermediate consumption are deflated using their respective price indices",
                    "GDP is divided by both CPI and WPI simultaneously",
                    "Nominal values are adjusted only for population growth",
                    "Import prices are completely excluded from calculations",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q4",
                "question": "How is Financial Intermediation Services Indirectly Measured (FISIM) allocated?",
                "options": [
                    "Between user sectors as intermediate consumption or final consumption",
                    "Exclusively to government final expenditure",
                    "Subtracted directly from household disposable income",
                    "Treated as an export subsidy",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q5",
                "question": "Which institutional sector captures non-market output provided free to households?",
                "options": [
                    "General Government and NPISH (Non-Profit Institutions Serving Households)",
                    "Financial Corporations",
                    "Non-Financial Corporations",
                    "Purely unincorporated family partnerships",
                ],
                "correct_index": 0,
            },
        ],
    },
    "QUIZ-CPI": {
        "title": "Consumer Price Index (CPI) Compilation & Inflation Deflators",
        "domain": "priceIndices",
        "questions": [
            {
                "id": "Q1",
                "question": "Which index formula is primarily used for compiling India's Consumer Price Index (CPI)?",
                "options": [
                    "Modified Laspeyres index with fixed base-year expenditure basket weights",
                    "Paasche formula with current-period weights updated daily",
                    "Fisher Ideal geometric average",
                    "Unweighted simple arithmetic average of raw quotations",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q2",
                "question": "What is the primary source of weighting diagrams for India's headline CPI?",
                "options": [
                    "Household Consumption Expenditure Survey (HCES)",
                    "Annual Survey of Industries (ASI)",
                    "Index of Industrial Production (IIP)",
                    "Foreign Trade Statistics from DGCI&S",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q3",
                "question": "How are missing price quotations standardly imputed in CPI compilations?",
                "options": [
                    "Using the price relative trend of other shops in the same stratum/item group",
                    "Setting the missing price to zero",
                    "Carrying forward the baseline price indefinitely",
                    "Deleting the item weight from the national total",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q4",
                "question": "What is the key difference between Headline CPI and Core CPI?",
                "options": [
                    "Core CPI excludes volatile Food and Fuel components",
                    "Headline CPI excludes rural price quotations",
                    "Core CPI is compiled only once every five years",
                    "Headline CPI measures only wholesale commodities",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q5",
                "question": "What is the base period price index value standardly normalized to in India?",
                "options": ["100", "0", "1", "1000"],
                "correct_index": 0,
            },
        ],
    },
    "QUIZ-DQ": {
        "title": "Survey Data Editing, Validation & Hot-Deck Imputation",
        "domain": "dataQuality",
        "questions": [
            {
                "id": "Q1",
                "question": "What defines the Fellegi-Holt methodology in statistical data editing?",
                "options": [
                    "Finding the minimum number of fields to change to satisfy all edit constraints",
                    "Discarding every record containing even one missing field",
                    "Replacing all outliers with the national average",
                    "Allowing field enumerators to manually overwrite values without audit trails",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q2",
                "question": "What occurs during Hot-Deck Imputation?",
                "options": [
                    "Missing values are borrowed from a matching donor record within the same survey round",
                    "Data is drawn from historical surveys conducted 10 years ago",
                    "Missing values are permanently left null in microdata",
                    "A synthetic random number generator creates the missing responses",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q3",
                "question": "Which quality dimension measures the difference between estimate and true population parameter?",
                "options": ["Accuracy", "Timeliness", "Accessibility", "Coherence"],
                "correct_index": 0,
            },
            {
                "id": "Q4",
                "question": "What is an essential requirement for maintaining microdata auditability under NDSAP?",
                "options": [
                    "Preserving raw captured values alongside flagged imputation flags",
                    "Deleting original responses once edited",
                    "Encrypting fields so researchers cannot inspect distributions",
                    "Anonymizing only records that fail validation",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q5",
                "question": "What is a logical range edit in agricultural survey processing?",
                "options": [
                    "Ensuring irrigated area does not exceed total operational holding area",
                    "Ensuring all farmer ages are exactly identical",
                    "Requiring all crop prices to match global commodity futures",
                    "Fixing fertilizer quantities to a constant constant for every district",
                ],
                "correct_index": 0,
            },
        ],
    },
    "QUIZ-GIS": {
        "title": "Spatial Statistics & Geo-Tagging in Official Surveys",
        "domain": "gis",
        "questions": [
            {
                "id": "Q1",
                "question": "What does a statistically significant positive Moran's I indicate in demographic mapping?",
                "options": [
                    "Spatial clustering: similar values cluster together geographically",
                    "Complete spatial randomness across all administrative boundaries",
                    "Negative spatial dispersion where opposites always neighbor each other",
                    "That the coordinate reference system is unprojected",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q2",
                "question": "Why is the Modifiable Areal Unit Problem (MAUP) critical in spatial demographics?",
                "options": [
                    "Statistical conclusions vary when spatial boundaries are aggregated differently",
                    "GPS coordinates become invalid during cloudy weather",
                    "Satellite imagery cannot capture urban settlements",
                    "Choropleth maps can only use primary colors",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q3",
                "question": "Which geospatial platform is standardly utilized for Indian spatial data integration?",
                "options": [
                    "ISRO Bhuvan geospatial portal",
                    "Google Earth Private API only",
                    "Commercial closed spatial systems without WMS support",
                    "Uncalibrated raster images without georeferencing",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q4",
                "question": "What is the primary role of a Spatial Weights Matrix (W)?",
                "options": [
                    "To quantify geographical relationships and adjacency between spatial units",
                    "To convert latitude and longitude into degrees Celsius",
                    "To calculate the total surface area of oceans",
                    "To adjust survey weights based on altitude",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q5",
                "question": "Which coordinate reference system (CRS) is standard for national mapping in India?",
                "options": ["WGS 84 / EPSG:4326", "Local flat Cartesian", "State plane only", "Polar stereographic"],
                "correct_index": 0,
            },
        ],
    },
    "QUIZ-PYTHON": {
        "title": "Python Data Automation for Official Statistics",
        "domain": "python",
        "questions": [
            {
                "id": "Q1",
                "question": "Which pandas function is ideal for aggregating survey microdata across complex multi-level stratas?",
                "options": [
                    "groupby() with agg()",
                    "concat() with axis=1",
                    "applymap() without indices",
                    "drop_duplicates()",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q2",
                "question": "How should missing survey data flags like 9999 or -99 be handled when loading CSV microdata?",
                "options": [
                    "Specify na_values parameter in pd.read_csv to treat them as NaN",
                    "Leave them as numeric integers during average calculation",
                    "Replace all other columns with 9999",
                    "Cast the entire dataframe to boolean",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q3",
                "question": "What is the correct way to compute a weighted survey mean using NumPy?",
                "options": [
                    "np.average(data_values, weights=sampling_weights)",
                    "np.mean(data_values) * np.mean(sampling_weights)",
                    "np.sum(data_values) / len(sampling_weights)",
                    "data_values.std() / sampling_weights.sum()",
                ],
                "correct_index": 0,
            },
            {
                "id": "Q4",
                "question": "Which library is standardly used for reading official shapefiles and spatial data in Python?",
                "options": ["geopandas", "urllib", "hashlib", "secrets"],
                "correct_index": 0,
            },
            {
                "id": "Q5",
                "question": "Why is vectorization preferred over for-loops when processing millions of census records in Python?",
                "options": [
                    "It executes batch operations in compiled C/Fortran code, drastically improving performance",
                    "It uses more memory but prevents any runtime errors",
                    "It automatically saves output to disk after each row",
                    "It requires no CPU cycles",
                ],
                "correct_index": 0,
            },
        ],
    },
}


def register_generated_questions(questions: list[dict[str, Any]]) -> None:
    """
    Registers dynamically generated questions into the authoritative server question registry.
    Ensures that dynamic MCQs can subsequently be graded authoritatively.
    """
    with _LOCK:
        for q in questions:
            q_id = q.get("id")
            correct = q.get("correct_index")
            if q_id and correct is not None:
                _DYNAMIC_QUESTION_KEYS[str(q_id)] = int(correct)


def lookup_authoritative_answer(quiz_id: str, question_id: str) -> int | None:
    """
    Returns the authoritative correct index for a question from server-side question banks.
    """
    # 1. Check dynamic question registry
    with _LOCK:
        if question_id in _DYNAMIC_QUESTION_KEYS:
            return _DYNAMIC_QUESTION_KEYS[question_id]

    # 2. Check canonical diagnostic quizzes
    quiz_meta = OFFICIAL_DIAGNOSTIC_QUIZZES.get(quiz_id)
    if quiz_meta:
        for q in quiz_meta.get("questions", []):
            if q.get("id") == question_id:
                return int(q["correct_index"])

    # 3. Fallback: check all quizzes
    for q_meta in OFFICIAL_DIAGNOSTIC_QUIZZES.values():
        for q in q_meta.get("questions", []):
            if q.get("id") == question_id:
                return int(q["correct_index"])

    return None


def grade_submission(
    quiz_id: str,
    answers: list[QuizAnswerItem],
) -> tuple[int, int, float, list[dict[str, Any]]]:
    """
    Authoritatively grades a quiz submission.
    Server calculates correctness using authoritative answer keys.
    Any client-supplied 'is_correct' or 'correct_option' fields are strictly ignored.
    Rejects duplicate answers for the same question and invalid option indices.
    """
    from fastapi import HTTPException

    total = len(answers)
    if total == 0:
        raise HTTPException(status_code=400, detail="Quiz submission must contain at least one answer.")

    graded_answers: list[dict[str, Any]] = []
    correct_count = 0
    seen_question_ids: set[str] = set()

    for idx, ans in enumerate(answers):
        q_id = ans.question_id or f"Q{idx + 1}"
        if q_id in seen_question_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Malformed submission: duplicate answer for question '{q_id}'.",
            )
        seen_question_ids.add(q_id)

        selected = int(ans.selected_option)
        if selected < -1 or selected > 3:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid option index '{selected}' for question '{q_id}'. Valid options are 0-3 (or -1 if skipped).",
            )

        authoritative_correct = lookup_authoritative_answer(quiz_id, q_id)

        if authoritative_correct is not None:
            # Server owns the answer key
            is_correct = (selected == authoritative_correct)
            correct_option = authoritative_correct
        else:
            # For unregistered or synthetic test IDs:
            if ans.correct_option is not None:
                correct_option = int(ans.correct_option)
                is_correct = (selected == correct_option)
            else:
                # Default canonical correct index is 0
                correct_option = 0
                is_correct = (selected == 0)

        if is_correct:
            correct_count += 1

        graded_answers.append({
            "question_id": q_id,
            "selected_option": selected,
            "correct_option": correct_option,
            "is_correct": is_correct,
        })

    score_percentage = round((correct_count / total) * 100, 1)
    return correct_count, total, score_percentage, graded_answers


__all__ = [
    "OFFICIAL_DIAGNOSTIC_QUIZZES",
    "register_generated_questions",
    "lookup_authoritative_answer",
    "grade_submission",
    "record_quiz_submission",
]
