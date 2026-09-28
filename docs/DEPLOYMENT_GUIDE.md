# StatSkill AI — Production Deployment Guide
**Problem Statement ID:** 26101  
**Project:** StatSkill AI (Official Statistical System Competency Platform)  
**Target Environment:** Cloud VPS (Ubuntu/Debian), Container Platforms (Docker/Kubernetes), or Windows Server.

---

## 1. Quick Start: 1-Command Containerized Deployment

StatSkill AI provides full container orchestration out of the box with Docker Compose.

### Prerequisites
- Docker Engine $\ge 24.0$
- Docker Compose $\ge 2.20$

### Execution
From the project root:
```bash
docker compose up --build -d
```

### Deployed Services
| Service | Container Name | Port | Description |
| :--- | :--- | :---: | :--- |
| **Backend API** | `statskill_backend` | `8000` | FastAPI server, auto-restarts, persistent uploads & JSON |
| **Frontend Web** | `statskill_frontend` | `80` (and `5173`) | Nginx reverse proxy serving optimized Vite SPA bundle |

### Verifying Deployment
Visit:
- **Web Application:** `http://localhost` or `http://localhost:5173`
- **Interactive API Documentation:** `http://localhost/docs` or `http://localhost:8000/docs`
- **Health Probe:** `http://localhost/health`

Run the built-in smoke test:
```bash
python scripts/verify_deployment.py --url http://localhost:8000
```

---

## 2. Bare-Metal Linux VPS Deployment (Ubuntu / Debian)

If deploying directly to a cloud virtual machine without Docker:

### Step 2.1: System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nodejs npm nginx curl
```

### Step 2.2: Backend Systemd Service
Create `/etc/systemd/system/statskill-backend.service`:
```ini
[Unit]
Description=StatSkill AI FastAPI Backend Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/statskill/backend
Environment="PATH=/var/www/statskill/backend/venv/bin"
Environment="STATSKILL_ADMIN_KEY=your-secure-admin-key"
Environment="STATSKILL_CORS_ORIGINS=https://statskill.yourdomain.gov.in"
ExecStart=/var/www/statskill/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable statskill-backend
sudo systemctl start statskill-backend
sudo systemctl status statskill-backend
```

### Step 2.3: Frontend Build & Nginx Configuration
```bash
cd /var/www/statskill/frontend
npm ci
npm run build
```

Configure Nginx (`/etc/nginx/sites-available/statskill`):
```nginx
server {
    listen 80;
    server_name statskill.yourdomain.gov.in;

    client_max_body_size 50M;

    # Static SPA assets
    location / {
        root /var/www/statskill/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API Proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000/health;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8000/openapi.json;
    }
}
```

Enable site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/statskill /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 3. Windows Server / Local Developer Deployment

Use the dedicated automated launchers:
- **Backend:** Double-click `START_BACKEND.bat`
- **Frontend:** Double-click `START_FRONTEND.bat`
- **Automated Verification:** Double-click `scripts\run_all_tests.bat`

---

## 4. Environment Variables Reference

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `STATSKILL_ADMIN_KEY` | `dev-admin-key` | Secret key required in `X-Admin-Key` header for administrative endpoints |
| `STATSKILL_CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Allowed CORS origins (comma-separated) |
| `STATSKILL_DATA_FILE` | `backend/statskill.json` | Path to persistent user & competency dataset |
| `STATSKILL_DEMO_FILE` | `backend/demo.json` | Path to seeded demo user credentials |
| `GEMINI_API_KEY` | *(None)* | Optional Google Gemini key for real-time online document MCQ generation |
| `OPENAI_API_KEY` | *(None)* | Optional OpenAI key for real-time online document MCQ generation |

> [!NOTE]
> If neither `GEMINI_API_KEY` nor `OPENAI_API_KEY` is provided, the platform automatically activates the high-fidelity **Local Statistical Concept Intelligence Engine**, generating domain-accurate questions from official MoSPI/NSSTA statistical concepts with zero latency and zero downtime.

---

## 5. Security & SSL/TLS Configuration (Let's Encrypt)

To secure the platform with HTTPS on public domains:
```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d statskill.yourdomain.gov.in
```
Certbot will automatically install SSL certificates and configure auto-renewal via systemd timers.
