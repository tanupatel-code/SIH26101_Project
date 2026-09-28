# StatSkill AI — REST API & Type Specification
**Problem Statement ID:** 26101  
**Base URL:** `http://localhost:8000` (or reverse proxied `/api`)  
**Specification Standard:** OpenAPI 3.0 / FastAPI  

---

## 1. System & Health Endpoints

### `GET /health`
- **Description:** Deployment liveness and readiness probe.
- **Response `200 OK`:**
  ```json
  {
    "status": "ok",
    "version": "3.0.0",
    "platform": "StatSkill AI — Official Statistical System Platform"
  }
  ```

### `GET /api/meta`
- **Description:** System scale, platform statistics, and cadre information.
- **Response `200 OK`:**
  ```json
  {
    "platform": "StatSkill AI",
    "totalUsers": 50,
    "frameworkDomains": 7,
    "igotCourseCatalogCount": 6
  }
  ```

### `GET /api/competencies/framework`
- **Description:** Official MoSPI / NSSTA FRAC competency definitions, benchmarks, and weights.

---

## 2. Authentication Endpoints

### `POST /api/auth/login`
- **Request Body (`application/json`):**
  ```json
  {
    "email": "ananya.verma@demo.gov.in",
    "password": "Demo@12345"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "access_token": "a1b2c3...",
    "token_type": "bearer",
    "data": { ... }
  }
  ```
- **Error Responses:** `401 Unauthorized` (bad password), `422 Unprocessable Entity` (missing fields).

### `POST /api/auth/register`
- **Request Body (`application/json`):**
  ```json
  {
    "name": "Dr. Ramesh Kumar",
    "email": "ramesh.k@mospi.gov.in",
    "password": "SecurePassword123",
    "role": "Senior Statistical Officer",
    "department": "National Accounts Division",
    "projectId": "SIH26101"
  }
  ```

### `POST /api/auth/logout`
- **Headers:** `Authorization: Bearer <token>`
- **Response `200 OK`:** `{"ok": true}`

### `GET /api/me` & `GET /api/me/data`
- **Headers:** `Authorization: Bearer <token>`
- **Response `200 OK`:** Full user profile, competency score tree, critical gaps, learning path, and dynamic iGOT recommendations.

---

## 3. Officer Document Vault & AI MCQ Generation

### `POST /api/documents/upload`
- **Request Content-Type:** `multipart/form-data`
- **Form Param:** `file: UploadFile` (PDF, DOCX, TXT, MD, PPTX)
- **Response `200 OK`:** Document record with `id`, `filename`, `chunks_count`, `preview`.

### `GET /api/documents`
- **Headers:** `Authorization: Bearer <token>`
- **Response `200 OK`:** List of all documents in officer's vault.

### `POST /api/mcq/generate`
- **Request Body (`application/json`):**
  ```json
  {
    "document_id": "USR-001_c5492d50_NSSO_Sampling_Manual.txt",
    "num_questions": 5,
    "difficulty": "Intermediate",
    "bloom_level": "Application",
    "domain": "statisticalMethods"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "questions": [
      {
        "id": "MCQ-001",
        "question": "What is the primary role of multiplier weights in stratified multi-stage NSSO surveys?",
        "options": [
          "To inflate sample values to represent the entire target population",
          "To eliminate sampling variance completely",
          "To reduce data entry errors",
          "To calculate non-response bias"
        ],
        "correct_index": 0,
        "bloom_level": "Application",
        "domain": "statisticalMethods",
        "explanation": "In NSSO design, inverse selection probabilities (multipliers) project sample aggregates to population totals."
      }
    ]
  }
  ```

---

## 4. Assessment Engine & Closed-Loop Reassessment

### `GET /api/assessments/available`
- **Response `200 OK`:** Curated official diagnostic quizzes.

### `POST /api/assessments/submit`
- **Headers:** `Authorization: Bearer <token>`
- **Request Body (`application/json`):**
  ```json
  {
    "quiz_id": "QUIZ-SNA-01",
    "title": "National Accounts & GDP Compilation Assessment",
    "domain": "nationalAccounts",
    "answers": [
      {
        "question_id": "MCQ-001",
        "selected_option": 0,
        "correct_option": 0,
        "is_correct": true
      }
    ]
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "score": 100.0,
    "passed": true,
    "feedback": "Outstanding performance in National Accounts.",
    "updatedUser": { ... }
  }
  ```

---

## 5. iGOT Karmayogi Ecosystem Integration

### `GET /api/igot/courses`
- **Query Params:** `domain` (optional), `level` (optional)
- **Response `200 OK`:** Course catalog with NSSTA accreditation and FRAC codes.

### `GET /api/igot/recommendations`
- **Headers:** `Authorization: Bearer <token>`
- **Response `200 OK`:** Dynamically prioritized courses targeting the officer's current diagnosed competency gaps.

### `POST /api/igot/enroll`
- **Headers:** `Authorization: Bearer <token>`
- **Request Body (`application/json`):**
  ```json
  {
    "course_id": "iGOT-NSSTA-STAT-101"
  }
  ```
- **Response `200 OK`:** Updated enrollment status, with +4 hours credited to officer's learning record.

---

## 6. Administrative Management

### `GET /api/admin/users`
- **Headers:** `X-Admin-Key: <STATSKILL_ADMIN_KEY>`
- **Response `200 OK`:** Full user roster.

### `PUT /api/admin/users/{user_id}`
- **Headers:** `X-Admin-Key: <STATSKILL_ADMIN_KEY>`
- **Request Body:** Partial profile or competency patch dictionary.
