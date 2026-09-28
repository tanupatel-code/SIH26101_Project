# StatSkill AI — Localhost Setup & Deployment Guide
> **Repository:** [https://github.com/tanupatel-code/SIH26101_Project.git](https://github.com/tanupatel-code/SIH26101_Project.git)  
> **MoSPI · Smart India Hackathon (SIH 2024)** · Problem Statement SIH26101  
> **Architecture:** FastAPI (Python 3.12) on Port `8000` + Vite & React 19 on Port `5173`

---

## 0. Prerequisites Checklist

| Tool / Runtime | Minimum Version | Recommended | Verification Command |
|---|---|---|---|
| **Python** | 3.10+ | 3.12.x | `python --version` |
| **Node.js & npm** | Node 18+, npm 9+ | Node 20+ LTS | `node -v && npm -v` |
| **Git CLI** | 2.30+ | Latest stable | `git --version` |
| **Docker (Optional)** | 24.0+ with Compose v2 | Docker Desktop | `docker compose version` |

---

## 1. Clone the GitHub Repository

Open your terminal (PowerShell, Command Prompt, or Bash/Zsh) and clone the repository:

```bash
git clone https://github.com/tanupatel-code/SIH26101_Project.git
cd SIH26101_Project
```

### Directory Architecture Overview
```text
SIH26101_Project/
|-- backend/                  # FastAPI Application, Services & SQLite/JSON Store
|   |-- main.py               # Central REST API application entry point
|   |-- requirements.txt      # Python dependencies (FastAPI, pypdf, pytest, etc.)
|   |-- .env.example          # Backend environment template
|   |-- statskill.json        # User profile, competencies & document repository
|   |-- data_sources.json     # 16 Official MoSPI surveys, registers & indices
|   `-- tests/                # 92 Automated pytest test suites
|-- frontend/                 # Vite + React 19 Frontend User Interface
|   |-- App.jsx               # Root application router & UI workflows
|   |-- package.json          # Node dependencies
|   |-- .env.example          # Frontend environment template
|   `-- vite.config.js        # Vite build & development server configuration
|-- docs/                     # Technical specifications, architecture & guides
|   |-- LOCAL_SETUP_GUIDE.pdf # Printable PDF setup manual
|   |-- LOCAL_SETUP_GUIDE.html# HTML document source
|   `-- LOCAL_SETUP_GUIDE.md  # Markdown setup guide
|-- START_BACKEND.bat         # 1-Click Windows Backend Launcher
|-- START_FRONTEND.bat        # 1-Click Windows Frontend Launcher
`-- docker-compose.yml        # Multi-container orchestration definition
```

---

## 2. Configure Backend Environment (`.env`)

The backend reads configuration from `SIH26101_Project/backend/.env`. Create this file by copying the template:

### Windows PowerShell:
```powershell
Copy-Item backend\.env.example backend\.env
```

### Windows Command Prompt (CMD):
```cmd
copy backend\.env.example backend\.env
```

### macOS / Linux (Bash or Zsh):
```bash
cp backend/.env.example backend/.env
```

### Expected `backend/.env` Content:
```env
# StatSkill AI Backend Environment Settings
STATSKILL_ADMIN_KEY=dev-admin-key
STATSKILL_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:80
GEMINI_API_KEY=
OPENAI_API_KEY=
```
> **Note on LLM API Keys:** `GEMINI_API_KEY` and `OPENAI_API_KEY` are entirely **optional**. When omitted, StatSkill AI uses its deterministic MoSPI and NSSTA question generation algorithms and official course curricula offline without cloud dependencies.

---

## 3. Set Up Python Environment & Install Dependencies

It is best practice to create an isolated Python virtual environment:

### Step A: Create and Activate Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
*(If you see an execution policy error in PowerShell, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

**Windows Command Prompt (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step B: Upgrade pip and Install Dependencies
From the repository root (`SIH26101_Project`):
```bash
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

---

## 4. Configure Frontend Environment (`.env`)

The frontend requires an active `.env` file at `SIH26101_Project/frontend/.env`:

### Windows PowerShell:
```powershell
Copy-Item frontend\.env.example frontend\.env
```

### Windows CMD / macOS / Linux:
```bash
# Windows CMD:
copy frontend\.env.example frontend\.env

# macOS / Linux:
cp frontend/.env.example frontend/.env
```

### Expected `frontend/.env` Content:
```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 5. Install Frontend Dependencies & Verify Build

From the repository root (`SIH26101_Project`):

```bash
cd frontend
npm install
npm run build
cd ..
```
*(Verify that the build finishes with 0 errors and generates `dist/assets/`)*

---

## 6. Launch Application on Localhost

Open **two separate terminal windows** from the project root directory:

### Terminal 1: Start Backend (FastAPI API on Port 8000)
```bash
# Ensure virtual environment is active (.venv)
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- **Backend API URL:** [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

### Terminal 2: Start Frontend (Vite Dev Server on Port 5173)
```bash
cd frontend
npm run dev
```
- **Frontend Portal URL:** [http://localhost:5173](http://localhost:5173)

### Windows 1-Click Launchers (Alternative)
On Windows, you can simply double-click the included batch files in the root folder:
1. Double-click `START_BACKEND.bat`
2. Double-click `START_FRONTEND.bat`

---

## 7. Pre-Configured Test Accounts & Login

Navigate to [http://localhost:5173/](http://localhost:5173/) in your web browser.

You can log in using either the **1-click quick-fill buttons** on the login screen or enter credentials manually:

| User Persona | Official Email | Password | 1-Click UI Shortcut |
|---|---|---|---|
| **Senior Statistical Officer (SSO)**<br>Ananya Verma, JSO / Cadre Officer | `ananya.verma@demo.gov.in` | `Demo@12345` | Click **"Quick Fill Demo Officer (SSO)"** |
| **General Citizen / Public Learner**<br>Aarav Sharma / Open Learner Track | `aarav.sharma@gmail.com` | `Demo@12345` | Click **"Quick Fill Citizen / General Public"** |
| **Custom Registration**<br>Any self-registered account | *Your email* | *Your password* | Click **"Sign Up / Register"** |

---

## 8. Verification & Automated Testing Suite

Verify full system health and test coverage by running pytest from the repository root:

```bash
python -m pytest backend/tests -v
```
*(All **92 tests** will run across unit services, type case edge cases, e2e user lifecycles, and deployment readiness)*

### Feature Smoke Test Checklist:
1. **My Documents**: Sidebar &rarr; `My Documents` &rarr; Confirms 8 diverse official MoSPI study resources across Survey Methodology, National Accounts, Price Indices, and GIS.
2. **Document Downloads**: Click download icon on any document &rarr; Downloads valid, openable document immediately.
3. **Official Certificate**: Sidebar &rarr; `Certificates` &rarr; Click `Verify Credential` on any active accreditation &rarr; Click `Download Official Certificate` &rarr; Downloads a 100% standards-compliant ISO 32000-1 / PDF 1.4 certificate that opens cleanly in Adobe Acrobat and Google Chrome.
4. **Data Sources**: Sidebar &rarr; `Data Sources` &rarr; Browse 16 official statistical registries with domain filtering (Survey, Price, Macro, Admin).
5. **Course Analytics**: Sidebar &rarr; `Analytics` &rarr; Displays full radar charts, domain learning effort, and learning velocity.
6. **iGOT Learning Path**: Sidebar &rarr; `Learning Path` &rarr; Launch diagnostic module workspaces and quizzes.

---

## 9. Alternative: 1-Command Docker Deployment

If Docker Desktop is installed, start the entire stack in isolated containers:

```bash
docker compose up --build -d
```
- Frontend: [http://localhost:5173](http://localhost:5173) or [http://localhost:80](http://localhost:80)
- Backend: [http://localhost:8000](http://localhost:8000)
- Teardown: `docker compose down`

---

## 10. Troubleshooting & FAQs

| Issue Encountered | Root Cause | Immediate Resolution |
|---|---|---|
| **Port 8000 or 5173 already in use** | A previous background process is still bound to the port. | Windows PowerShell:<br>`Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess \| Stop-Process -Force`<br>macOS/Linux: `kill $(lsof -t -i:8000)` |
| **PowerShell script execution disabled** | Windows default ExecutionPolicy. | Run in PowerShell:<br>`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| **CORS error in browser console** | Backend started with mismatched origins. | Verify `STATSKILL_CORS_ORIGINS` in `backend/.env` contains `http://localhost:5173`. |
| **ModuleNotFoundError** | Dependencies installed in global Python rather than virtual environment. | Ensure `.venv` is activated (`.venv\Scripts\Activate.ps1`) before executing `pip install -r backend/requirements.txt`. |
