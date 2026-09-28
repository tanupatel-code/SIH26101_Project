# StatSkill AI — Architecture & Framework Specification
**Problem Statement ID:** 26101  
**Project:** StatSkill AI (Official Statistical System Competency Platform)  
**Target Cadres:** Junior Statistical Officers (JSO), Senior Statistical Officers (SSO), Statistical Investigators, Directors (ISS)

---

## 1. The Closed-Loop Capacity Building Architecture

The StatSkill AI platform implements a closed-loop intelligence lifecycle designed specifically for capacity building in India's National Statistical System:

```
    ┌────────────────┐
    │  1. ASSESS     │ ◄─── Officer uploads official manuals / takes diagnostic quizzes
    └───────┬────────┘
            ▼
    ┌────────────────┐
    │  2. DIAGNOSE   │ ◄─── Multi-signal computation of scores against MoSPI benchmarks
    └───────┬────────┘
            ▼
    ┌────────────────┐
    │ 3. PERSONALISE │ ◄─── Dynamic FRAC gap matching against iGOT Karmayogi catalog
    └───────┬────────┘
            ▼
    ┌────────────────┐
    │   4. LEARN     │ ◄─── Interactive learning on NSSTA accredited courses
    └───────┬────────┘
            ▼
    ┌────────────────┐
    │  5. REASSESS   │ ◄─── Targeted Bloom's Taxonomy MCQs generated directly from manuals
    └───────┬────────┘
            ▼
    ┌────────────────┐
    │  6. IMPROVE    │ ◄─── Closed-loop score & dashboard updates; audit trail logged
    └───────┬────────┘
            └─────────────── Loop back to ASSESS for continuous progression
```

---

## 2. Multi-Signal Competency Formulation

Competency in each domain is evaluated using a 4-signal weighted mathematical model:

$$\text{DomainScore} = 0.50 \times \text{Quiz} + 0.25 \times \text{Course} + 0.15 \times \text{SelfAssessment} + 0.10 \times \text{Effort}$$

Where:
- **$\text{Quiz}$**: Normalized assessment score out of 5 ($\frac{\text{score}}{20}$)
- **$\text{Course}$**: Verified course completion grade out of 5
- **$\text{SelfAssessment}$**: Peer/Self rating on a 1–5 scale
- **$\text{Effort}$**: Learning hours logged against the domain ($\min(5.0, \frac{\text{hours}}{8.0})$)

### Benchmark Deficit & Readiness
$$\text{Gap} = \max(0.0, \text{Benchmark} - \text{DomainScore})$$
$$\text{Readiness} = \min\left(100\%, \frac{\text{DomainScore}}{\text{Benchmark}} \times 100\%\right)$$

---

## 3. Official Statistical Domains (MoSPI / NSSTA FRAC Alignment)

1. **Statistical Methods & Sampling (`statisticalMethods`)**
   - Benchmark: `3.5 / 5.0` | Weight: `1.15`
   - FRAC Code: `FRAC-STAT-METH-02`
2. **National Accounts & Macro Deflators (`nationalAccounts`)**
   - Benchmark: `3.5 / 5.0` | Weight: `1.10`
   - FRAC Code: `FRAC-STAT-SNA-01`
3. **Price Statistics & Index Compilation (`priceIndices`)**
   - Benchmark: `3.5 / 5.0` | Weight: `1.05`
   - FRAC Code: `FRAC-STAT-PRICE-03`
4. **Data Quality & Survey Validation (`dataQuality`)**
   - Benchmark: `3.5 / 5.0` | Weight: `1.05`
   - FRAC Code: `FRAC-STAT-DQ-01`
5. **GIS & Spatial Statistics (`gis`)**
   - Benchmark: `3.0 / 5.0` | Weight: `1.00`
   - FRAC Code: `FRAC-STAT-GIS-04`
6. **Python for Statistical Automation (`python`)**
   - Benchmark: `3.0 / 5.0` | Weight: `1.00`
   - FRAC Code: `FRAC-STAT-PY-02`
7. **Machine Learning & AI in Governance (`machineLearning`)**
   - Benchmark: `3.0 / 5.0` | Weight: `0.95`
   - FRAC Code: `FRAC-STAT-AI-01`

---

## 4. AI MCQ Generation Pipeline

```
  [ Upload Document: PDF / DOCX / TXT ]
                 │
                 ▼
  [ Document Parser & Cleaner ] ──► Normalized UTF-8 text + Whitespace Stripping
                 │
                 ▼
  [ Semantic Chunker ] ──────────► Overlapping chunks (1200 chars / 200 overlap)
                 │
                 ▼
  [ Concept Detector ] ──────────► Official statistical terms (SNA, CPI, SRS, Moran's I)
                 │
        ┌────────┴────────┐
        ▼                 ▼
  [ Online Cloud LLM ]   [ Local Statistical Heuristics Engine ]
  (Gemini / OpenAI API)  (Zero-downtime NSSTA question bank fallback)
        └────────┬────────┘
                 ▼
  [ Bloom's Taxonomy Assignment ] ──► Recall, Understanding, Application, Analysis
                 │
                 ▼
  [ Rigorous 4-Option Schema ] ────► Exactly 1 correct answer + Pedagogical Explanation
```
