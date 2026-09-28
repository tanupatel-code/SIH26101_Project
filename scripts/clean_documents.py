import json
from pathlib import Path

DATASET_PATH = Path("backend/statskill.json")

def clean_documents():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Curated official MoSPI documents for USR-001 (Ananya Verma)
    curated_officer_docs = [
        {
            "id": "DOC-001",
            "name": "NSSO_Field_Operations_Sampling_Manual.pdf",
            "category": "Survey Methodology",
            "size": "342 KB",
            "uploadDate": "12 Mar 2026",
            "wordCount": 1420,
            "chunksCount": 8,
            "summary": "National Sample Survey Office (NSSO) Field Operations & Sampling Manual for household and enterprise socio-economic surveys. Outlines stratified multi-stage design, primary sampling units, and sample weighting.",
            "extractedText": "National Sample Survey Office (NSSO) Field Operations & Sampling Manual for household and enterprise socio-economic surveys. Outlines stratified multi-stage design, primary sampling units, and sample weighting.",
            "shared": True,
            "addedThisMonth": False,
        },
        {
            "id": "DOC-002",
            "name": "SNA_2008_National_Accounts_Compilation_Guidelines.pdf",
            "category": "National Accounts",
            "size": "1120 KB",
            "uploadDate": "18 Mar 2026",
            "wordCount": 2680,
            "chunksCount": 14,
            "summary": "Central Statistics Office (CSO) methodology guidelines on Gross Domestic Product (GDP), Gross Value Added (GVA), and institutional sector accounts aligned with the UN System of National Accounts 2008.",
            "extractedText": "Central Statistics Office (CSO) methodology guidelines on Gross Domestic Product (GDP), Gross Value Added (GVA), and institutional sector accounts aligned with the UN System of National Accounts 2008.",
            "shared": True,
            "addedThisMonth": False,
        },
        {
            "id": "DOC-003",
            "name": "Consumer_Price_Index_Base_Revision_Handbook.pdf",
            "category": "Price Indices",
            "size": "512 KB",
            "uploadDate": "25 Mar 2026",
            "wordCount": 1840,
            "chunksCount": 9,
            "summary": "Technical manual for compilation of Consumer Price Index (Rural, Urban, Combined) with base year revision procedures, item basket selection, and Laspeyres price index calculation.",
            "extractedText": "Technical manual for compilation of Consumer Price Index (Rural, Urban, Combined) with base year revision procedures, item basket selection, and Laspeyres price index calculation.",
            "shared": False,
            "addedThisMonth": True,
        },
        {
            "id": "DOC-004",
            "name": "National_Quality_Assurance_Framework_NQAF_Standard.pdf",
            "category": "Data Quality",
            "size": "280 KB",
            "uploadDate": "02 Apr 2026",
            "wordCount": 960,
            "chunksCount": 5,
            "summary": "Guidelines for implementing the National Quality Assurance Framework (NQAF) in official survey microdata, validation protocols, logical consistency checks, and outlier treatment.",
            "extractedText": "Guidelines for implementing the National Quality Assurance Framework (NQAF) in official survey microdata, validation protocols, logical consistency checks, and outlier treatment.",
            "shared": True,
            "addedThisMonth": True,
        },
        {
            "id": "DOC-005",
            "name": "Bhuvan_Geospatial_Sampling_Frame_Integration.pdf",
            "category": "GIS & Spatial",
            "size": "890 KB",
            "uploadDate": "05 Apr 2026",
            "wordCount": 1540,
            "chunksCount": 7,
            "summary": "Standard operating procedure for integrating ISRO Bhuvan satellite imagery and spatial GIS layers with National Sample Survey urban frame survey (UFS) blocks.",
            "extractedText": "Standard operating procedure for integrating ISRO Bhuvan satellite imagery and spatial GIS layers with National Sample Survey urban frame survey (UFS) blocks.",
            "shared": False,
            "addedThisMonth": True,
        },
        {
            "id": "DOC-006",
            "name": "STATSKILL-AI_SIH26101_Methodology_Deck.pptx",
            "category": "GIS & Spatial",
            "size": "4648 KB",
            "uploadDate": "10 Apr 2026",
            "wordCount": 746,
            "chunksCount": 5,
            "summary": "StatSkill AI technical architecture presentation covering closed-loop competency diagnostics, iGOT Karmayogi course integration, and AI quiz generation.",
            "extractedText": "StatSkill AI technical architecture presentation covering closed-loop competency diagnostics, iGOT Karmayogi course integration, and AI quiz generation.",
            "shared": False,
            "addedThisMonth": True,
        },
        {
            "id": "DOC-007",
            "name": "PLFS_Annual_Report_2023_24_Statistical_Tables.xlsx",
            "category": "Survey Methodology",
            "size": "720 KB",
            "uploadDate": "14 Apr 2026",
            "wordCount": 1120,
            "chunksCount": 6,
            "summary": "Periodic Labour Force Survey (PLFS) key statistical indicators, labor force participation rates (LFPR), and worker population ratio (WPR) microdata tables.",
            "extractedText": "Periodic Labour Force Survey (PLFS) key statistical indicators, labor force participation rates (LFPR), and worker population ratio (WPR) microdata tables.",
            "shared": True,
            "addedThisMonth": True,
        },
    ]

    # Clean USR-001
    users = data.get("users", [])
    if users:
        users[0]["documents"] = curated_officer_docs

    # Check and deduplicate all other users
    for user in users[1:]:
        docs = user.get("documents", [])
        seen_names = set()
        unique_docs = []
        for d in docs:
            name = d.get("name")
            if name and name not in seen_names:
                seen_names.add(name)
                unique_docs.append(d)
        user["documents"] = unique_docs

    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Successfully cleaned and deduplicated all documents in statskill.json!")

if __name__ == "__main__":
    clean_documents()
