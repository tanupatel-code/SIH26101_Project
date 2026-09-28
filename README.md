# StatSkill AI — Intelligent Capacity Building & Learning Ecosystem

**Problem Statement ID:** 26101  
**Problem Statement Title:** *Develop an AI-enabled learning platform that identifies competency gaps, recommends personalized training through integration with the iGOT Karmayogi ecosystem, and is capable of generating Quizzes and Multiple Choice Questions (MCQs) from uploaded learning materials to strengthen capacity building in India's Official Statistical System.*  
**Target Ministry / Cadre:** Ministry of Statistics and Programme Implementation (MoSPI) & National Statistical Systems Training Academy (NSSTA)  
**System Version:** 3.0.0 (Production-Ready Architecture)  
**Test Suite Status:** ✅ **90 of 90 Tests Passed (100% Pass Rate)**  
**Static Type Safety:** ✅ **0 Typing Issues (Mypy Checked)**  

---

## 1. Project Overview & Identity

StatSkill AI is a specialized, end-to-end AI-powered learning and diagnostic platform tailored specifically for India's Official Statistical System. The platform implements a **continuous closed-loop capacity building cycle**:

```
 ┌──────────┐     ┌──────────┐     ┌─────────────┐
 │  ASSESS  │ ──> │ DIAGNOSE │ ──> │ PERSONALISE │
 └──────────┘     └──────────┘     └─────────────┘
       ▲                                  │
       │                                  ▼
 ┌──────────┐     ┌──────────┐     ┌─────────────┐
 │ IMPROVE  │ <── │ REASSESS │ <── │    LEARN    │
 └──────────┘     └──────────┘     └─────────────┘
```

1. **Assess:** Diagnostic assessments measuring performance against official National Statistical benchmarks.
2. **Diagnose:** 4-signal multi-factor competency calculation identifying exact domain deficits (e.g., Price Indices, National Accounts).
3. **Personalise:** Dynamic filtering and matching of official iGOT Karmayogi courses targeted specifically to the diagnosed deficits.
4. **Learn:** Official FRAC-accredited training with learning hour and credit tracking.
5. **Reassess:** Automatic quiz and MCQ generation from user-uploaded training materials aligned to Bloom's Taxonomy.
6. **Improve:** Immediate, dynamic recalculation of officer competency scores and readiness percentages upon assessment submission.

---

## 2. Structured Folder Hierarchy

The project is structured into modular, production-ready domains:

```
SIH26101_Project/
├── docker-compose.yml              # 1-Command full-stack container orchestration
├── .dockerignore                  # Docker build exclusions (node_modules, cache)
├── .env.example                   # Master environment configuration template
├── START_BACKEND.bat              # One-click Windows FastAPI backend launcher
├── START_FRONTEND.bat             # One-click Windows React/Vite frontend launcher
├── CHECK_NODE.bat                 # Node.js environment diagnostic tool
├── README.md                      # Primary project overview & navigation guide
│
├── deploy/                        # 🚀 Production Deployment Architecture
│   ├── Dockerfile.backend         # Python 3.12 slim container with healthchecks
│   ├── Dockerfile.frontend        # Multi-stage Node.js build to Nginx SPA
│   ├── docker-compose.yml         # Container configuration copy
│   ├── nginx.conf                 # Production reverse proxy (SPA + API routing)
│   ├── deploy.sh                  # Linux / Cloud VPS deployment automation
│   ├── deploy.bat                 # Windows Server deployment automation
│   └── .env.production.example    # Production environment template
│
├── scripts/                       # 🧪 Automated Testing & Smoke Tools
│   ├── run_all_tests.bat          # Runs Mypy, full 90-test Pytest, & frontend build
│   ├── run_all_tests.sh           # Linux/macOS equivalent test runner
│   ├── run_type_checks.bat        # Runs Mypy + Type Case Pytest suite
│   ├── run_type_checks.sh         # Linux/macOS type check runner
│   └── verify_deployment.py       # Live deployment health & smoke verification CLI
│
├── docs/                          # 📚 Comprehensive Documentation Suite
│   ├── DEPLOYMENT_GUIDE.md        # Full production deployment guide (Docker, VPS, SSL)
│   ├── ARCHITECTURE.md            # Closed loop, FRAC engine & RAG MCQ design
│   ├── API_SPECIFICATION.md       # Complete REST API schemas and parameters
│   ├── TEST_EXECUTION_REPORT.md   # Detailed 90-test execution report
│   └── SYSTEM_CHANGES_DOCUMENTATION.md # Version changelog & feature breakdown
│
├── backend/                       # ⚙️ FastAPI Python Backend
│   ├── __init__.py                # Package marker
│   ├── main.py                    # API route handlers & session management
│   ├── statskill.json             # 50-officer synthetic MoSPI cadre dataset
│   ├── demo.json                  # Ananya Verma demo profile credentials
│   ├── requirements.txt           # Python backend dependencies (includes mypy)
│   ├── .env.example               # Backend environment variables
│   ├── services/                  # Business Logic Engines
│   │   ├── __init__.py            # Package marker
│   │   ├── competency_service.py  # 4-signal competency engine & reassessment loop
│   │   ├── document_parser.py     # PDF, DOCX, PPTX & text extractor and chunker
│   │   ├── igot_service.py        # iGOT Karmayogi catalog & gap recommendation engine
│   │   └── mcq_generator.py       # Bloom's taxonomy MCQ generator (Online + Local)
│   ├── tests/                     # 🛡️ Test Suites (90 Tests Total)
│   │   ├── __init__.py            # Package marker
│   │   ├── test_components.py     # 25 Component isolation tests
│   │   ├── test_e2e_system.py     # 30 End-to-end integration tests
│   │   ├── test_type_cases.py     # 25 Type case & schema validation tests
│   │   └── test_deployment_readiness.py # 10 Production deployment health tests
│   └── uploads/                   # Stored learning documents uploaded by users
│
└── frontend/                      # 🎨 React 19 + Vite Frontend SPA
    ├── index.html                 # HTML shell with StatSkill AI title
    ├── package.json               # Frontend package definition (React 19, Vite)
    ├── vite.config.js             # Vite configuration with port 5173
    ├── .env.example               # Environment template pointing to backend:8000
    ├── .env                       # Active environment configuration
    ├── main.jsx                   # React application entry point
    ├── App.jsx                    # Primary platform container and navigation
    ├── DocumentStudio.jsx         # Document upload and AI MCQ synthesis interface
    ├── QuizPlayer.jsx             # Interactive quiz runner with Bloom tags & rationales
    ├── IgotHub.jsx                # iGOT Karmayogi gap-to-course recommendation interface
    ├── login.jsx & register.jsx   # Authentication interfaces
    ├── educational.css            # Styles for Bloom tags, quizzes, scorecards
    └── App.css & themes           # Multi-theme design system (Cyber, Executive, Aurora)
```

---

## 3. Quick Start & Execution

### Option A: 1-Command Docker Deployment (Recommended for Production)
```bash
docker compose up --build -d
```
- **Web App:** `http://localhost` (or `http://localhost:5173`)
- **Backend API Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`

### Option B: Local Windows Launchers (Recommended for Developers)
1. Double-click `START_BACKEND.bat` (Starts FastAPI on `http://127.0.0.1:8000`)
2. Double-click `START_FRONTEND.bat` (Starts Vite on `http://localhost:5173`)

### Option C: Manual Command-Line

#### Terminal 1 — Backend:
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 — Frontend:
```bash
cd frontend
npm install
npm run dev
```

---

## 4. Dual-Audience Login Credentials (Officer & General Learner)

The platform includes a pre-loaded 50-officer Indian Statistical Service / Subordinate Statistical Service cadre dataset:

| Role / Profile | Email | Password | Identifier | Key Features |
| :--- | :--- | :--- | :---: | :--- |
| **Senior Statistical Officer (SSO)** | `ananya.verma@demo.gov.in` | `Demo@12345` | `USR-001` | Full profile with critical skill gaps in Price Indices & National Accounts, active enrollments, and quiz history. |
| **Director / Admin** | `rajesh.kumar@statskill.demo` | `demo123` | `USR-002` | High-level cadre oversight, broad competency score. |
| **Junior Statistical Officer (JSO)** | Any user in `statskill.json` | `demo123` | `USR-003` to `USR-050` | Individual statistical cadre profiles across Indian states. |

| **General Learner (Scholar)** | `aarav.sharma@learner.in` | `Learner@12345` | `PUB-001` | Independent researcher/student workspace with public microdata and capacity roadmap. |

*Quick Tip: On the login page, switch between "Government Officer" and "General Learner" tabs, and use the 1-Click Demo Fill buttons.*

---

## 5. Verification & Testing Suites

StatSkill AI is backed by 90 automated tests and static type validation:

### 1. Run All Tests, Type Checking, and Production Build:
```bash
# Windows
scripts\run_all_tests.bat

# Linux / macOS
bash scripts/run_all_tests.sh
```

### 2. Run Type Case & Schema Tests Only:
```bash
# Windows
scripts\run_type_checks.bat

# Manual
python -m mypy --explicit-package-bases --ignore-missing-imports backend/
python -m pytest backend/tests/test_type_cases.py -v
```

### 3. Verify Live Deployment (Smoke Test):
```bash
python scripts/verify_deployment.py --url http://localhost:8000
```

### Test Suite Breakdown (90 Tests Total):
- **Component Isolation Tests (25):** `backend/tests/test_components.py`
- **End-to-End System Tests (30):** `backend/tests/test_e2e_system.py`
- **Type Case & Schema Validation Tests (25):** `backend/tests/test_type_cases.py`
- **Deployment Readiness Tests (10):** `backend/tests/test_deployment_readiness.py`

---

## 6. Official Statistical Domains (MoSPI / NSSTA FRAC Alignment)

1. **Statistical Methods & Sampling** (Benchmark: 3.5, Weight: 1.15) — Probability sampling, NSSO design, stratification, weighting.
2. **System of National Accounts (SNA 2008)** (Benchmark: 3.5, Weight: 1.10) — GDP compilation, GVA, supply-use tables.
3. **Price Indices & Deflators** (Benchmark: 3.5, Weight: 1.05) — CPI (Rural/Urban), WPI, Laspeyres vs Paasche indices, IIP.
4. **Data Quality & Validation** (Benchmark: 3.5, Weight: 1.05) — Imputation protocols, non-sampling errors, UN NQAF standards.
5. **GIS & Spatial Statistics** (Benchmark: 3.0, Weight: 1.00) — Geo-referencing, thematic mapping, Moran's I spatial autocorrelation.
6. **Python for Statistical Automation** (Benchmark: 3.0, Weight: 1.00) — Pandas, automated data pipelines, automated tabulation.
7. **Machine Learning in Official Statistics** (Benchmark: 3.0, Weight: 0.95) — Nowcasting, administrative data record linkage.

---

## 7. Deep-Dive Documentation Links

- 📖 [Production Deployment Guide](file:///c:/Users/madhv/Downloads/SIH26101_Project/docs/DEPLOYMENT_GUIDE.md)
- 🏗️ [System Architecture & FRAC Framework](file:///c:/Users/madhv/Downloads/SIH26101_Project/docs/ARCHITECTURE.md)
- 🔌 [Complete REST API Specification](file:///c:/Users/madhv/Downloads/SIH26101_Project/docs/API_SPECIFICATION.md)
- 📊 [Full 90-Test Execution Report](file:///c:/Users/madhv/Downloads/SIH26101_Project/docs/TEST_EXECUTION_REPORT.md)
- 📝 [System Changes & Version Changelog](file:///c:/Users/madhv/Downloads/SIH26101_Project/docs/SYSTEM_CHANGES_DOCUMENTATION.md)

---
*StatSkill AI — Official Statistical System Capacity Building & iGOT Ecosystem Integration.*
