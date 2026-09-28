# Official Statistical Data Sources of India
**Ministry of Statistics and Programme Implementation (MoSPI)**  
**Problem Statement ID:** 26101 (StatSkill AI)  
**Coordinating Agency:** National Statistical Office (NSO)  

This document outlines the core official statistical data sources powering India's National Statistical System, their survey design methodologies, microdata catalogs, and learning applications.

---

## 1. National Sample Survey Office (NSSO)

### 1.1 Periodic Labour Force Survey (PLFS)
- **Division:** Survey Design and Research Division (SDRD) & Field Operations Division (FOD)
- **Frequency:** Quarterly (Urban) & Annual (Rural + Urban)
- **Core Indicators:** Labour Force Participation Rate (LFPR), Worker Population Ratio (WPR), Unemployment Rate (UR)
- **Sampling Scheme:** Rotational panel design with 2-stage stratification.
- **Microdata Portal:** [https://microdata.gov.in/nada43/index.php/catalog/PLFS](https://microdata.gov.in/nada43/index.php/catalog/PLFS)
- **Key Variables:** Usual Principal & Subsidiary Status, Current Weekly Status (CWS), NIC/NCO classifications, Multiplier weights.

### 1.2 Household Consumption Expenditure Survey (HCES)
- **Division:** NSSO Data Quality Assurance Division (DQAD)
- **Frequency:** Quinquennial
- **Core Indicators:** Monthly Per Capita Consumption Expenditure (MPCE), poverty lines, weighting diagrams for CPI.
- **Sampling Scheme:** Stratified multi-stage sampling with household decile classifications.
- **Microdata Portal:** [https://microdata.gov.in/nada43/index.php/catalog/HCES](https://microdata.gov.in/nada43/index.php/catalog/HCES)

### 1.3 Annual Survey of Unincorporated Sector Enterprises (ASUSE)
- **Division:** NSSO Economic Surveys
- **Frequency:** Annual
- **Core Indicators:** Informal economy GVA, unorganized manufacturing/services enterprises, employment intensity.

---

## 2. Central Statistics Office (CSO) & National Accounts

### 2.1 National Accounts Statistics (NAS) & GDP Compilation
- **Division:** National Accounts Division (NAD)
- **Frequency:** Quarterly & Annual
- **Standard:** UN System of National Accounts (SNA 2008)
- **Core Indicators:** GDP at Market Prices, GVA at Basic Prices, Supply and Use Tables (SUT), Gross Fixed Capital Formation (GFCF).
- **Portal:** [https://mospi.gov.in/national-accounts-division-nad](https://mospi.gov.in/national-accounts-division-nad)

### 2.2 Annual Survey of Industries (ASI)
- **Division:** Economic Statistics Division (ESD)
- **Frequency:** Annual
- **Coverage:** Registered factories under Sections 2m(i) & 2m(ii) of Factories Act, 1948.
- **Core Indicators:** Invested capital, net value added, employment, fuels consumed.
- **Microdata Portal:** [https://microdata.gov.in/nada43/index.php/catalog/ASI](https://microdata.gov.in/nada43/index.php/catalog/ASI)

---

## 3. Price Statistics Division (PSD)

### 3.1 Consumer Price Index (CPI Rural, Urban, Combined)
- **Frequency:** Monthly (Released on 12th of every month)
- **Base Year:** 2012 = 100
- **Formula:** Modified Laspeyres Price Index
- **Core Indicators:** Headline CPI, Consumer Food Price Index (CFPI), State-wise price indices.
- **Portal:** [https://cpi.np.gov.in/](https://cpi.np.gov.in/)

### 3.2 Index of Industrial Production (IIP)
- **Base Year:** 2011-12 = 100
- **Sectors:** Mining (14.37%), Manufacturing (77.63%), Electricity (7.99%).

---

## 4. Open Portals & Capacity Building Infrastructure

### 4.1 Open Government Data (OGD) Platform India (`data.gov.in`)
- Machine-readable open data formats (.csv, REST API, JSON).
- Integration point for Python data pipelines and automated analysis.

### 4.2 iGOT Karmayogi Digital Platform
- Mission Karmayogi capacity building infrastructure.
- FRAC (Framework for Roles, Activities, and Competencies) accredited courses by NSSTA.
- Portal: [https://igotkarmayogi.gov.in/](https://igotkarmayogi.gov.in/)
