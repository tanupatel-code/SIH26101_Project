import json
import sys
from pathlib import Path

# Add backend to path for services
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from services.competency_service import ensure_competency_shape

statskill_path = backend_dir / "statskill.json"
data = json.loads(statskill_path.read_text(encoding="utf-8"))

users = data.get("users", [])
aarav_id = "USR-PUB-001"

# Check if already present
aarav_idx = next((i for i, u in enumerate(users) if u.get("id") == aarav_id), None)

aarav_record = {
    "id": aarav_id,
    "employeeCode": "PUB-LRN-2026-001",
    "profile": {
        "name": "Aarav Sharma",
        "email": "aarav.sharma@learner.in",
        "password": "Learner@12345",
        "role": "Citizen Data Analyst & Research Scholar",
        "department": "National Open Statistical Learning",
        "projectId": "PUBLIC-LEARNER",
        "accountType": "general"
    },
    "dashboard": {
        "overallCompetency": 68,
        "overallCompetencyLabel": "68/100",
        "rank": "Citizen Scholar",
        "level": 64,
        "xp": 3450,
        "criticalSkillGaps": 2,
        "moderateSkillGaps": 3,
        "strongSkills": 2,
        "learningProgress": 42,
        "assessmentsCompleted": 4,
        "assessmentsTotal": 6,
        "assessmentAverage": 79,
        "learningHours": 48,
        "completedModules": 1,
        "activeModule": "Open Statistical Data Exploration & Python Analytics"
    },
    "competencyScores": {
        "statisticalMethods": 3.4,
        "nationalAccounts": 2.4,
        "priceIndices": 2.6,
        "dataQuality": 3.2,
        "gis": 2.8,
        "python": 4.2,
        "machineLearning": 2.9
    },
    "assessmentHistory": [
        {
            "id": "PUB-ASM-01",
            "domain": "statisticalMethods",
            "title": "Open Statistical Data & Survey Literacy",
            "score": 82,
            "maxScore": 100,
            "attempt": 1,
            "status": "Completed",
            "date": "2026-08-15"
        },
        {
            "id": "PUB-ASM-02",
            "domain": "python",
            "title": "Python for Microdata Analysis (Pandas/NumPy)",
            "score": 89,
            "maxScore": 100,
            "attempt": 1,
            "status": "Completed",
            "date": "2026-08-28"
        },
        {
            "id": "PUB-ASM-03",
            "domain": "gis",
            "title": "Bhuvan Geospatial Statistics & Demographics",
            "score": 68,
            "maxScore": 100,
            "attempt": 1,
            "status": "Completed",
            "date": "2026-09-05"
        },
        {
            "id": "PUB-ASM-04",
            "domain": "dataQuality",
            "title": "Open Data Quality Validation & Error Detection",
            "score": 78,
            "maxScore": 100,
            "attempt": 2,
            "status": "Completed",
            "date": "2026-09-18"
        }
    ],
    "learningPath": {
        "track": "Citizen Data Science & Open Statistics Learning Track",
        "totalModules": 4,
        "modulesCompleted": 1,
        "hoursCompleted": 8.0,
        "estimatedTotalHours": 32,
        "estimatedCompletion": "24 days",
        "modules": [
            {
                "step": 1,
                "title": "Foundations of National Statistical Datasets",
                "status": "Completed",
                "state": "done",
                "progress": 100,
                "duration": "8 hrs",
                "lessons": "6 / 6",
                "domain": "statisticalMethods"
            },
            {
                "step": 2,
                "title": "Open Statistical Data Exploration & Python Analytics",
                "status": "In Progress",
                "state": "active",
                "progress": 42,
                "duration": "10 hrs",
                "lessons": "4 / 8",
                "domain": "python"
            },
            {
                "step": 3,
                "title": "Bhuvan Geospatial Visualizations for Demographics",
                "status": "Locked",
                "state": "locked",
                "progress": 0,
                "duration": "8 hrs",
                "lessons": "0 / 7",
                "domain": "gis"
            },
            {
                "step": 4,
                "title": "Citizen Research Project & Capstone Assessment",
                "status": "Locked",
                "state": "locked",
                "progress": 0,
                "duration": "6 hrs",
                "lessons": "0 / 3",
                "domain": "statisticalMethods"
            }
        ]
    },
    "courses": [
        {
            "id": "CRS-PUB-01",
            "title": "Open Government Data (OGD) APIs & Pipelines",
            "domain": "python",
            "score": 85,
            "hours": 12,
            "progress": 100,
            "status": "Completed"
        },
        {
            "id": "CRS-PUB-02",
            "title": "Statistical Computing with Python & Pandas",
            "domain": "python",
            "score": 78,
            "hours": 14,
            "progress": 65,
            "status": "In Progress"
        },
        {
            "id": "CRS-PUB-03",
            "title": "NSS & PLFS Microdata Extraction Basics",
            "domain": "statisticalMethods",
            "score": 72,
            "hours": 10,
            "progress": 40,
            "status": "In Progress"
        },
        {
            "id": "CRS-PUB-04",
            "title": "Data Quality Verification for Open Data Portals",
            "domain": "dataQuality",
            "score": 80,
            "hours": 8,
            "progress": 50,
            "status": "In Progress"
        }
    ],
    "assignments": [
        {
            "id": "ASG-PUB-01",
            "domain": "python",
            "title": "Microdata Cleaning Notebook Assignment",
            "type": "Assignment",
            "score": 88,
            "maxScore": 100,
            "status": "Completed",
            "attempts": 1,
            "dueDate": "2026-10-15"
        },
        {
            "id": "ASG-PUB-02",
            "domain": "statisticalMethods",
            "title": "Sample Survey Variance Estimator",
            "type": "Assignment",
            "score": 76,
            "maxScore": 100,
            "status": "Completed",
            "attempts": 2,
            "dueDate": "2026-11-01"
        }
    ],
    "documents": [
        {
            "id": "DOC-PUB-01",
            "name": "Open Statistical Data Handbook – Citizen Guide.pdf",
            "category": "Learning Materials",
            "size": "1.8 MB",
            "shared": False,
            "addedThisMonth": True,
            "summary": "Step-by-step introduction for researchers, students, and citizens on accessing and interpreting MoSPI survey statistics."
        },
        {
            "id": "DOC-PUB-02",
            "name": "PLFS Unit-level Data Extraction Notebook.pdf",
            "category": "Research Notes",
            "size": "1.2 MB",
            "shared": True,
            "addedThisMonth": True,
            "summary": "Technical methodology notes on extracting raw household records and computing labor metrics using Python."
        },
        {
            "id": "DOC-PUB-03",
            "name": "Python Pandas for Survey Analysis Guide.pdf",
            "category": "Learning Materials",
            "size": "2.1 MB",
            "shared": False,
            "addedThisMonth": False,
            "summary": "Guide to weighting variables, strata grouping, and summary table compilation."
        },
        {
            "id": "DOC-PUB-04",
            "name": "Open Government Data (OGD) API Documentation.pdf",
            "category": "Technical Specifications",
            "size": "0.9 MB",
            "shared": True,
            "addedThisMonth": True,
            "summary": "National data gateway API schema, query parameters, rate limits, and JSON endpoints."
        }
    ],
    "certificates": [
        {
            "id": "CERT-PUB-01",
            "title": "Open Statistical Data Analyst Certification",
            "issuer": "National Statistical System Learning Academy",
            "issued": "15 Feb 2026",
            "expires": "15 Feb 2028",
            "status": "Active",
            "color": "green"
        },
        {
            "id": "CERT-PUB-02",
            "title": "Python for Official Microdata",
            "issuer": "StatSkill Open Learning",
            "issued": "20 May 2026",
            "expires": "20 May 2028",
            "status": "Active",
            "color": "green"
        },
        {
            "id": "CERT-PUB-03",
            "title": "Bhuvan Geospatial Statistics Specialist",
            "issuer": "ISRO-Bhuvan & MoSPI Joint Academy",
            "issued": "—",
            "expires": "—",
            "status": "In Progress",
            "color": "blue",
            "progress": 45
        }
    ],
    "notifications": [
        {
            "id": "NOTIF-PUB-01",
            "title": "Open Statistical Data Exploration — 42% complete",
            "time": "1h ago",
            "color": "cyan"
        },
        {
            "id": "NOTIF-PUB-02",
            "title": "New assessment scheduled: Open Data Quality Verification",
            "time": "4h ago",
            "color": "amber"
        },
        {
            "id": "NOTIF-PUB-03",
            "title": "Python for Microdata score verified: 89%",
            "time": "1d ago",
            "color": "green"
        }
    ],
    "rawInputs": {
        "selfAssessment": {
            "statisticalMethods": [3.5, 3.5],
            "nationalAccounts": [2.4, 2.4],
            "priceIndices": [2.6, 2.6],
            "dataQuality": [3.2, 3.2],
            "gis": [2.8, 2.8],
            "python": [4.2, 4.2],
            "machineLearning": [2.9, 2.9]
        },
        "learningHours": {
            "statisticalMethods": 12,
            "nationalAccounts": 4,
            "priceIndices": 4,
            "dataQuality": 8,
            "gis": 6,
            "python": 14,
            "machineLearning": 0
        }
    }
}

ensure_competency_shape(aarav_record)

if aarav_idx is not None:
    users[aarav_idx] = aarav_record
    print("Updated existing Aarav record.")
else:
    users.append(aarav_record)
    print("Appended new Aarav record.")

data["users"] = users
data["userCount"] = len(users)

statskill_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Successfully saved {len(users)} users to statskill.json")
