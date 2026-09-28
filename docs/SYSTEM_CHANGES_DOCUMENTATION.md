# StatSkill AI — System Changes & Implementation Documentation
**Problem Statement ID:** 26101  
**Problem Statement Title:** *Develop an AI enabled learning platform that identifies competency gaps, recommends personalized training through integration with the iGOT Karmayogi ecosystem, and capable of generating Quizzes and Multiple choice questions (MCQs) from uploaded learning materials to strengthen capacity building in India's Official Statistical System.*  
**Implementation Version:** 3.0.0 (Production-Ready Architecture)  
**Date:** September 2026  

---

## 1. Architectural Overview & Changes Summary

Prior to this implementation, the codebase was a mock prototype displaying static values from a JSON file with no document ingestion, no question generation, no interactive quiz taking, and no iGOT Karmayogi integration.

We have now engineered a **complete, closed-loop, dynamic learning and capacity-building platform** adhering strictly to the Problem Statement (ID 26101) and the StatSkill AI capacity-building architecture (`ASSESS → DIAGNOSE → PERSONALISE → LEARN → REASSESS → IMPROVE`).

---

## 2. Backend Architecture & New Services

### 2.1 Document Parser (`backend/services/document_parser.py`)
- **Supported Formats:** PDF (`pypdf`), Word Document (`python-docx`), PowerPoint (`xml.etree` slide extractor), plain text, Markdown, and CSV.
- **Key Functions:**
  - `extract_document_text(filename, content)`: Inspects file headers, decodes text across multiple encodings (`utf-8`, `utf-8-sig`, `latin-1`), strips noise, and normalizes whitespaces.
  - `chunk_document(text, chunk_size=1200, overlap=200)`: Implements semantic paragraph chunking with boundary retention for high-relevance question generation.

### 2.2 AI MCQ & Quiz Generation Engine (`backend/services/mcq_generator.py`)
- **Cognitive Level Alignment:** Full support for Bloom's Taxonomy categories: *Recall, Understanding, Application, Analysis*.
- **Question Schema:** Each generated question strictly conforms to:
  - `id`: Unique identifier (e.g., `MCQ-001`)
  - `question`: Rigorous, academically formulated question statement
  - `options`: Exactly 4 mutually exclusive, plausible options
  - `correct_index`: 0 to 3
  - `bloom_level`: Cognitive level tag
  - `domain`: Official Statistical System domain key
  - `explanation`: In-depth educational rationale explaining the correct concept and common misconceptions.
- **Dual-Mode Engine:**
  - **Online Cloud LLM Mode:** Automatically detects `GEMINI_API_KEY` or `OPENAI_API_KEY` in environment variables and invokes structured JSON generation prompts.
  - **Local Statistical Concept Intelligence:** Zero-downtime offline generator with MoSPI/NSSTA domain heuristics (Sampling, SNA 2008, CPI/WPI, Data Quality, Moran's I GIS).

### 2.3 iGOT Karmayogi Ecosystem Service (`backend/services/igot_service.py`)
- **Accreditation & Provider Metadata:** Aligned with the National Statistical Systems Training Academy (NSSTA), MoSPI, NITI Aayog, and NIC.
- **FRAC Taxonomy:** Every course includes official FRAC competency codes (e.g., `FRAC-STAT-METH-02`, `FRAC-STAT-SNA-01`, `FRAC-STAT-PRICE-03`).
- **Dynamic Gap-Targeted Recommendation Engine:**
  - `recommend_courses_for_gaps(critical_skills, user_courses)`: Analyzes the officer's current diagnosed competency deficits and filters the course repository to recommend courses specifically designed to bridge those exact gaps.
  - Automatically excludes courses the officer has already completed.

### 2.4 Competency Engine & Reassessment Loop (`backend/services/competency_service.py`)
- **Expanded Official Statistical Domains:**
  1. `statisticalMethods`: Statistical Methods & Sampling (Benchmark: 3.5, Weight: 1.15)
  2. `nationalAccounts`: System of National Accounts, SNA 2008 & GDP Compilation (Benchmark: 3.5, Weight: 1.10)
  3. `priceIndices`: Price Statistics, CPI, WPI & IIP Deflators (Benchmark: 3.5, Weight: 1.05)
  4. `dataQuality`: Survey Data Quality, Validation & Imputation Protocols (Benchmark: 3.5, Weight: 1.05)
  5. `gis`: GIS, Geo-referencing & Spatial Statistics (Benchmark: 3.0, Weight: 1.00)
  6. `python`: Python for Statistical Automation (Benchmark: 3.0, Weight: 1.00)
  7. `machineLearning`: Machine Learning & AI in Governance (Benchmark: 3.0, Weight: 0.95)
- **Closed-Loop Quiz Submission:**
  - `record_quiz_submission()`: Immediately records the new assessment attempt, recomputes the domain score using the 4-signal weighted formula (`quiz*0.50 + course*0.25 + self*0.15 + effort*0.10`), updates the critical skills list, and recalculates overall dashboard competency.

---

## 3. New API Endpoints in `backend/main.py`

| HTTP Method | Route | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/documents/upload` | Multipart file upload (PDF/DOCX/PPTX/TXT), extracts text, chunks document, and registers in user vault. | Yes (Bearer) |
| `GET` | `/api/documents` | Retrieves all ingested learning materials for the authenticated user. | Yes (Bearer) |
| `POST` | `/api/mcq/generate` | Generates Bloom's taxonomy MCQs from uploaded document ID, text, or statistical topic. | Optional |
| `GET` | `/api/assessments/available` | Returns official NSSTA diagnostic quizzes ready to attempt. | No |
| `POST` | `/api/assessments/submit` | Grades quiz responses, records attempt, and **dynamically recalculates officer competency scores**. | Yes (Bearer) |
| `GET` | `/api/igot/courses` | Retrieves the official iGOT Karmayogi course catalog with domain/level filtering. | No |
| `GET` | `/api/igot/recommendations` | Returns personalized iGOT courses prioritized to bridge active skill gaps. | Yes (Bearer) |
| `POST` | `/api/igot/enroll` | Enrolls user in iGOT module, adds 4 learning hours, and recalculates readiness. | Yes (Bearer) |
| `GET` | `/api/competencies/framework` | Returns official MoSPI FRAC competency definitions and benchmarks. | No |

---

## 4. Frontend Educational System & UI Enhancements

### 4.1 Interactive Quiz Player (`frontend/QuizPlayer.jsx`)
- Complete interactive assessment runner with:
  - Active countdown timer (15:00 min with warning color state).
  - Bloom's taxonomy badge and cadre indicator.
  - Interactive radio option buttons with keyboard and click support.
  - Instant scorecard with percentage grade and pass/improvement badge.
  - **Question-by-Question Diagnostic Review:** Shows officer's answer, correct answer, and **detailed educational rationale/explanation** for every question.
  - Seamless callback updating the parent dashboard in real-time.

### 4.2 Document Studio (`frontend/DocumentStudio.jsx`)
- Modern drag-and-drop file upload dropzone.
- Automatic document metadata extraction: word count, chunk count, category tag, and summary.
- **AI Quiz Synthesis Modal:** Configurable question count (3, 5, 10), difficulty level, Bloom's cognitive level, and target statistical domain.
- Launches generated questions directly into the `QuizPlayer`.

### 4.3 iGOT Karmayogi Learning Hub (`frontend/IgotHub.jsx`)
- Direct visual connection between the officer's diagnosed gaps (e.g. *Price Statistics: Gap 1.5*) and the exact iGOT course recommended to bridge it.
- Full course directory with category filters.
- Real enrollment pipeline with learning hour tracking and direct links to the official portal (`https://igotkarmayogi.gov.in`).

### 4.4 Educational Styling System (`frontend/educational.css`)
- Custom Bloom's Taxonomy badges (`.bloom-analysis`, `.bloom-application`, `.bloom-understanding`, `.bloom-recall`).
- Scorecard progress circles and feedback banners.
- Question review cards with color-coded borders for correct vs. incorrect answers.
- Drag-and-drop dropzone hover animations.

---

## 5. Startup Script Enhancements

- **`START_BACKEND.bat`**: Upgraded to dynamically detect available Python installations (`py` launcher or `python` on PATH), eliminating hardcoded `py -3.14` errors and ensuring seamless execution on any developer machine.
- **`START_FRONTEND.bat`**: Runs `npm install` and `npm run dev` with automated path resolution for `npm.cmd`.
