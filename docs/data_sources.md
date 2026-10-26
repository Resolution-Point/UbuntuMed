# UbuntuMed — Data Sources

This document outlines the datasets used in the UbuntuMed project, their origins, and how they are utilized within our AI prototype.

## 1. District Health Barometer (DHB) 2018/19

- **Source:** Health Systems Trust (South Africa) / openAFRICA
- **Format:** CSV Files & PDF Report
- **Description:** Real, district-level data on South African public health facilities.
- **Usage in UbuntuMed:**
  - We extracted indicators related to the availability of tracer medicines, stockout rates, and ideal clinic status.
  - This data provides the real-world context and baseline for our problem definition (demonstrating where medicine availability is lowest).
- **Why we chose it:** It is real South African government health data, proving our project addresses a genuine local problem.

## 2. Zenodo PLMIF Pharmaceutical Supply Chain Dataset

- **Source:** Zenodo Open Access Repository
- **Format:** CSV
- **Description:** A dataset containing macroeconomic and pharmaceutical variables for South Africa (2014–2025). It includes variables like `Port_Delay_Days`, `Spoilage_pct`, and `Risk_Score`.
- **Usage in UbuntuMed:**
  - Used to understand the supply-side risks that cause stockouts.
  - It provides the context for _why_ medicine might arrive late or expired (e.g., port delays).

## 3. Kaggle Pharmacy Demand Dataset

- **Source:** Kaggle (Simulated Operational Data)
- **Format:** CSV
- **Description:** Contains weekly dispensing records, stock-on-hand, and medicine types.
- **Usage in UbuntuMed:**
  - This is the primary dataset used to train our Machine Learning models (Random Forest for forecasting and Isolation Forest for anomaly detection).
  - It provides the structured features needed to predict future medicine demand.

## 4. Prototype Test Data (Generated)

- **Source:** Custom Python Script (`generate_data.py`)
- **Description:** A synthetic dataset created specifically for our web application demonstration.
- **Usage in UbuntuMed:**
  - It simulates daily usage, current stock, and expiry dates across 4 clinics (Clinic A, B, C, D) and 4 medicines.
  - It powers the FastAPI backend and the Flask dashboard during the live demo.

## Privacy & Ethics

- No patient-level data or personally identifiable information (PII) is used in this project.
- All data operates at the facility or district level, in compliance with POPIA guidelines.
