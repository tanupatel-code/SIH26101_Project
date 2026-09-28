import os
import sys
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>StatSkill AI - Complete Localhost Setup & Deployment Guide</title>
<style>
  @page {
    size: A4;
    margin: 14mm 14mm 14mm 14mm;
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.5;
    font-size: 12px;
    margin: 0;
    padding: 0;
  }
  
  .header-cover {
    border-bottom: 2.5px solid #0f2e5a;
    padding-bottom: 12px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
  .header-title-block h1 {
    font-size: 21px;
    font-weight: 800;
    color: #0f2e5a;
    margin: 0 0 3px 0;
    letter-spacing: -0.4px;
  }
  .header-title-block h2 {
    font-size: 13px;
    font-weight: 600;
    color: #475569;
    margin: 0 0 6px 0;
  }
  .repo-tag {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-weight: 600;
  }
  .badge-gov {
    background: #0f2e5a;
    color: #ffffff;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: right;
  }

  .summary-banner {
    background: #f8fafc;
    border-left: 3.5px solid #0284c7;
    border-radius: 0 5px 5px 0;
    padding: 8px 12px;
    margin-bottom: 16px;
    font-size: 11.5px;
  }
  .summary-banner strong {
    color: #0f172a;
  }

  .section-block {
    margin-bottom: 16px;
    page-break-inside: avoid;
  }

  h3.section-header {
    font-size: 14px;
    font-weight: 700;
    color: #0f2e5a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 4px;
    margin: 16px 0 8px 0;
    display: flex;
    align-items: center;
    gap: 6px;
    page-break-after: avoid;
  }
  .step-num {
    background: #0f2e5a;
    color: white;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 10.5px;
    font-weight: bold;
    flex-shrink: 0;
  }

  p {
    margin: 0 0 6px 0;
  }
  
  .path-badge {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    color: #0f2e5a;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: Consolas, monospace;
    font-size: 11px;
    font-weight: 600;
  }

  pre.code-block {
    background: #0f172a;
    color: #f8fafc;
    padding: 8px 11px;
    border-radius: 5px;
    font-family: Consolas, "Courier New", monospace;
    font-size: 10.5px;
    line-height: 1.4;
    overflow-x: auto;
    margin: 5px 0 9px 0;
    border: 1px solid #334155;
    page-break-inside: avoid;
  }
  .code-title {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 2px;
    display: flex;
    justify-content: space-between;
  }
  .code-title span.os {
    color: #0284c7;
  }

  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0 10px 0;
    font-size: 11px;
    page-break-inside: avoid;
  }
  table.data-table th {
    background: #f1f5f9;
    color: #0f2e5a;
    font-weight: 700;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
  }
  table.data-table td {
    padding: 5px 8px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }
  table.data-table tr:nth-child(even) td {
    background: #f8fafc;
  }

  .callout-box {
    border-radius: 5px;
    padding: 7px 11px;
    margin: 8px 0;
    font-size: 11px;
    page-break-inside: avoid;
  }
  .callout-box.tip {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #065f46;
  }
  .callout-box.important {
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #92400e;
  }

  ul, ol {
    margin: 0 0 6px 0;
    padding-left: 18px;
  }
  li {
    margin-bottom: 3px;
  }

  .grid-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  .footer-note {
    margin-top: 20px;
    border-top: 1px solid #cbd5e1;
    padding-top: 8px;
    font-size: 10px;
    color: #64748b;
    display: flex;
    justify-content: space-between;
  }
</style>
</head>
<body>

<div class="header-cover">
  <div class="header-title-block">
    <h1>StatSkill AI — Localhost Setup & Deployment Guide</h1>
    <h2>Step-by-Step Engineering Runbook for Development & Localhost Execution</h2>
    <div class="repo-tag">Repository: https://github.com/tanupatel-code/SIH26101_Project.git</div>
  </div>
  <div class="badge-gov">
    MoSPI · SIH 2024<br>
    <span style="font-size: 8.5px; font-weight: normal; opacity: 0.85;">National Statistical Office</span>
  </div>
</div>

<div class="summary-banner">
  <strong>System Architecture:</strong> StatSkill AI is a statistical competency assessment and microdata analytics portal for MoSPI. The system pairs a high-performance <strong>FastAPI (Python)</strong> backend on port <code>8000</code> with a responsive <strong>Vite + React 19</strong> frontend on port <code>5173</code>.
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">0</span> System Prerequisites</h3>
  <table class="data-table">
    <thead>
      <tr>
        <th>Tool / Runtime</th>
        <th>Minimum Version</th>
        <th>Recommended</th>
        <th>Verification Command</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Python</strong></td>
        <td>3.10+</td>
        <td>3.12.x</td>
        <td><code>python --version</code></td>
      </tr>
      <tr>
        <td><strong>Node.js & npm</strong></td>
        <td>Node 18+, npm 9+</td>
        <td>Node 20+ LTS</td>
        <td><code>node -v && npm -v</code></td>
      </tr>
      <tr>
        <td><strong>Git CLI</strong></td>
        <td>2.30+</td>
        <td>Latest stable</td>
        <td><code>git --version</code></td>
      </tr>
      <tr>
        <td><strong>Docker (Optional)</strong></td>
        <td>24.0+ with Compose v2</td>
        <td>Docker Desktop</td>
        <td><code>docker compose version</code></td>
      </tr>
    </tbody>
  </table>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">1</span> Clone the Repository from GitHub</h3>
  <p>Open your terminal (PowerShell, Command Prompt, or Bash/Zsh) and clone the repository:</p>
  <div class="code-title">Terminal / Shell <span>All Platforms</span></div>
  <pre class="code-block">git clone https://github.com/tanupatel-code/SIH26101_Project.git
cd SIH26101_Project</pre>

  <p><strong>Directory Architecture:</strong></p>
  <pre class="code-block">SIH26101_Project/
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
|-- START_BACKEND.bat         # 1-Click Windows Backend Launcher
|-- START_FRONTEND.bat        # 1-Click Windows Frontend Launcher
`-- docker-compose.yml        # Multi-container orchestration definition</pre>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">2</span> Configure Backend Environment (.env)</h3>
  <p>Create the backend environment file in <span class="path-badge">SIH26101_Project/backend/.env</span>:</p>

  <div class="code-title">Windows PowerShell <span class="os">PowerShell</span></div>
  <pre class="code-block">Copy-Item backend\.env.example backend\.env</pre>

  <div class="code-title">Windows CMD / macOS / Linux</div>
  <pre class="code-block"># Windows Command Prompt:
copy backend\.env.example backend\.env

# macOS / Linux (Bash/Zsh):
cp backend/.env.example backend/.env</pre>

  <p>Verify that <span class="path-badge">backend/.env</span> contains:</p>
  <pre class="code-block">STATSKILL_ADMIN_KEY=dev-admin-key
STATSKILL_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:80
GEMINI_API_KEY=
OPENAI_API_KEY=</pre>
  
  <div class="callout-box tip">
    <strong>Offline Operation:</strong> <code>GEMINI_API_KEY</code> and <code>OPENAI_API_KEY</code> are optional. When omitted, StatSkill AI uses its built-in MoSPI/NSSTA question generation algorithms and official course curricula offline without needing cloud API keys.
  </div>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">3</span> Set Up Python Environment & Install Backend Dependencies</h3>
  <p>A Python virtual environment isolates dependencies cleanly:</p>

  <div class="grid-2col">
    <div>
      <div class="code-title">Windows (PowerShell)</div>
      <pre class="code-block">python -m venv .venv
.venv\Scripts\Activate.ps1</pre>
    </div>
    <div>
      <div class="code-title">macOS / Linux (Bash/Zsh)</div>
      <pre class="code-block">python3 -m venv .venv
source .venv/bin/activate</pre>
    </div>
  </div>

  <p style="font-size: 10.5px; color: #64748b; margin-top: -3px;"><em>PowerShell Tip: If script execution is restricted, run: <code>Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass</code></em></p>

  <p>Upgrade pip and install the required dependencies:</p>
  <div class="code-title">Terminal / Shell (from project root)</div>
  <pre class="code-block">python -m pip install --upgrade pip
pip install -r backend/requirements.txt</pre>

  <div class="callout-box important">
    <strong>Installed Packages:</strong> FastAPI (0.115.14), Uvicorn, Pydantic v2, pypdf (5.0+) for PDF generation, python-multipart for uploads, and pytest.
  </div>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">4</span> Configure Frontend Environment (.env)</h3>
  <p>Create the frontend environment file in <span class="path-badge">SIH26101_Project/frontend/.env</span>:</p>

  <div class="code-title">Windows PowerShell / CMD / Bash</div>
  <pre class="code-block"># Windows PowerShell:
Copy-Item frontend\.env.example frontend\.env

# Windows CMD:
copy frontend\.env.example frontend\.env

# macOS / Linux:
cp frontend/.env.example frontend/.env</pre>

  <p>Verify that <span class="path-badge">frontend/.env</span> contains:</p>
  <pre class="code-block">VITE_API_BASE_URL=http://localhost:8000</pre>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">5</span> Install Frontend Dependencies & Verify Build</h3>
  <p>Navigate to the frontend directory, install npm packages, and verify production build:</p>
  <div class="code-title">Terminal / Shell (from project root)</div>
  <pre class="code-block">cd frontend
npm install
npm run build
cd ..</pre>
  <p style="font-size: 11px; color: #15803d; font-weight: 600;">✓ Output: <code>built in ~2s</code> with 0 errors.</p>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">6</span> Launch Application on Localhost</h3>
  <p>Start both backend and frontend servers in separate terminal tabs:</p>

  <p><strong>Terminal 1: Start Backend API (FastAPI on Port 8000)</strong></p>
  <div class="code-title">Terminal 1 (from SIH26101_Project root)</div>
  <pre class="code-block"># Ensure virtual environment is active (.venv)
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000</pre>
  <p style="font-size: 11px; color: #475569;">Backend URL: <strong>http://localhost:8000</strong> · Interactive Swagger API Docs: <strong>http://localhost:8000/docs</strong></p>

  <p><strong>Terminal 2: Start Frontend UI (Vite on Port 5173)</strong></p>
  <div class="code-title">Terminal 2 (from SIH26101_Project root)</div>
  <pre class="code-block">cd frontend
npm run dev</pre>
  <p style="font-size: 11px; color: #475569;">Frontend Portal URL: <strong>http://localhost:5173</strong></p>

  <div class="callout-box tip">
    <strong>Windows 1-Click Launchers:</strong> Alternatively, double-click <span class="path-badge">START_BACKEND.bat</span> and <span class="path-badge">START_FRONTEND.bat</span> in the project root folder.
  </div>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">7</span> Portal Access & Pre-Configured Test Accounts</h3>
  <p>Open your browser and navigate to: <strong style="color: #0284c7;">http://localhost:5173/</strong></p>
  <p>Log in using either the 1-click login shortcuts or manual credentials:</p>

  <table class="data-table">
    <thead>
      <tr>
        <th>User Persona</th>
        <th>Official Email</th>
        <th>Password</th>
        <th>1-Click UI Shortcut</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Senior Statistical Officer (SSO)</strong><br><span style="font-size: 10px; color: #64748b;">Ananya Verma, JSO / Cadre Officer</span></td>
        <td><code>ananya.verma@demo.gov.in</code></td>
        <td><code>Demo@12345</code></td>
        <td>Click <strong>"Quick Fill Demo Officer (SSO)"</strong></td>
      </tr>
      <tr>
        <td><strong>General Citizen / Public Learner</strong><br><span style="font-size: 10px; color: #64748b;">Aarav Sharma / Open Learner Track</span></td>
        <td><code>aarav.sharma@gmail.com</code></td>
        <td><code>Demo@12345</code></td>
        <td>Click <strong>"Quick Fill Citizen / General Public"</strong></td>
      </tr>
      <tr>
        <td><strong>Custom New Registration</strong><br><span style="font-size: 10px; color: #64748b;">Self-registered officer or student</span></td>
        <td><em>Your custom email</em></td>
        <td><em>Your custom password</em></td>
        <td>Click <strong>"Sign Up / Register"</strong></td>
      </tr>
    </tbody>
  </table>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">8</span> Verification & Validation Runbook</h3>
  <p>Run the 92-test automated suite to confirm system integrity:</p>
  <div class="code-title">Terminal / Shell (from project root)</div>
  <pre class="code-block">python -m pytest backend/tests -v</pre>
  <p style="font-size: 11px; color: #15803d; font-weight: 600;">✓ Result: <strong>92 passed</strong> (Components, Type Safety, Deployment Readiness, E2E Workflows).</p>

  <p><strong>Key Feature Smoke Tests:</strong></p>
  <table class="data-table">
    <thead>
      <tr>
        <th>Feature</th>
        <th>Navigation Path</th>
        <th>Expected Output</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Document Vault</strong></td>
        <td>Sidebar &rarr; <strong>My Documents</strong></td>
        <td>8 distinct official MoSPI study resources across Survey Methodology, National Accounts, Price Indices, and GIS.</td>
      </tr>
      <tr>
        <td><strong>Document Download</strong></td>
        <td>Click download icon on any document</td>
        <td>Downloads clean, openable PDF/DOCX material.</td>
      </tr>
      <tr>
        <td><strong>Official Certificate</strong></td>
        <td>Sidebar &rarr; <strong>Certificates</strong> &rarr; Click <strong>"Verify Credential"</strong></td>
        <td>Opens modal; clicking <strong>"Download Official Certificate"</strong> downloads valid PDF 1.4 file that opens in Acrobat and Chrome.</td>
      </tr>
      <tr>
        <td><strong>Data Sources</strong></td>
        <td>Sidebar &rarr; <strong>Data Sources</strong></td>
        <td>Displays 16 official statistical surveys with functional domain filters and live search.</td>
      </tr>
      <tr>
        <td><strong>Course Analytics</strong></td>
        <td>Sidebar &rarr; <strong>Analytics</strong></td>
        <td>Displays competency score radars, domain effort hours, and learning velocity.</td>
      </tr>
      <tr>
        <td><strong>iGOT Learning Path</strong></td>
        <td>Sidebar &rarr; <strong>Learning Path</strong></td>
        <td>Displays recommended modules with interactive quiz player and study workspace.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">9</span> Alternative: 1-Command Docker Deployment</h3>
  <p>If you have Docker Desktop installed, deploy the entire stack with a single command:</p>
  <div class="code-title">Terminal / Shell (from project root)</div>
  <pre class="code-block">docker compose up --build -d</pre>
  <p style="font-size: 11px; color: #475569;">Access frontend at <strong>http://localhost:5173</strong> or <strong>http://localhost:80</strong>, and backend at <strong>http://localhost:8000</strong>.<br>To stop: <code>docker compose down</code></p>
</div>

<div class="section-block">
  <h3 class="section-header"><span class="step-num">10</span> Troubleshooting & FAQs</h3>
  <table class="data-table">
    <thead>
      <tr>
        <th>Issue</th>
        <th>Root Cause</th>
        <th>Resolution</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Port 8000 or 5173 in use</strong></td>
        <td>Previous process still bound to port.</td>
        <td>
          Windows PowerShell: <code>Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force</code><br>
          Linux/macOS: <code>kill $(lsof -t -i:8000)</code>
        </td>
      </tr>
      <tr>
        <td><strong>PowerShell execution policy</strong></td>
        <td>Restricted script execution in Windows.</td>
        <td>Run: <code>Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass</code></td>
      </tr>
      <tr>
        <td><strong>CORS error in browser</strong></td>
        <td>Frontend port mismatch.</td>
        <td>Verify <code>STATSKILL_CORS_ORIGINS</code> in <span class="path-badge">backend/.env</span> includes <code>http://localhost:5173</code>.</td>
      </tr>
      <tr>
        <td><strong>ModuleNotFoundError</strong></td>
        <td>Virtual environment not activated.</td>
        <td>Activate <code>.venv</code> first, then run <code>pip install -r backend/requirements.txt</code>.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="footer-note">
  <span>StatSkill AI · Smart India Hackathon (SIH 2024) · Problem Statement SIH26101</span>
  <span>Ministry of Statistics and Programme Implementation (MoSPI) · Government of India</span>
</div>

</body>
</html>
"""

def generate_pdf():
    docs_dir = BASE_DIR / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    html_path = docs_dir / "LOCAL_SETUP_GUIDE.html"
    pdf_path_root = BASE_DIR / "LOCAL_SETUP_GUIDE.pdf"
    pdf_path_docs = docs_dir / "LOCAL_SETUP_GUIDE.pdf"
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Generated HTML source at: {html_path}")
    
    edge_paths = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ]
    edge_exe = None
    for p in edge_paths:
        if p.exists():
            edge_exe = p
            break
            
    if not edge_exe:
        print("Microsoft Edge executable not found. Cannot compile PDF.")
        return False
        
    print(f"Using browser executable: {edge_exe}")
    abs_html = str(html_path.resolve())
    abs_pdf = str(pdf_path_root.resolve())
    
    cmd = [
        str(edge_exe),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        abs_html
    ]
    
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode == 0 and pdf_path_root.exists() and pdf_path_root.stat().st_size > 0:
        import shutil
        shutil.copy2(pdf_path_root, pdf_path_docs)
        print(f"SUCCESS: Generated PDF at: {pdf_path_root} ({pdf_path_root.stat().st_size} bytes)")
        print(f"Copied to: {pdf_path_docs}")
        return True
    else:
        print(f"Edge execution failed: {proc.stderr}")
        return False

if __name__ == "__main__":
    success = generate_pdf()
    sys.exit(0 if success else 1)
