# UbuntuMed

**Smart medicine stock help for public clinics**

> *"Ubuntu" — I am because we are. Better medicine availability for all.*

## What is this project?

This is a student project for the module **AI for Business Analysis with Python**.  
We are building a computer program that helps public clinics manage medicine better.  
It predicts which medicines will be needed, warns when stock may run out, and suggests moving extra medicine to another clinic before it expires.

## The problem 

Public clinics sometimes run out of important medicines like HIV medicine (ARVs), TB medicine, and blood pressure tablets.  
At the same time, other clinics throw away medicines because they expire.  
Nurses are very busy. They cannot always check stock, predict future needs, or move medicine between clinics quickly.  
Patients then miss doses or travel far to find medicine.

## Our solution

We are **not** replacing the systems clinics already use (such as SVS and RxSolution).  
We are adding a smart helper on top of them.

Our program will:

- Learn from real medicine use and stock data.
- Predict how much medicine each clinic will need.
- Warn about possible stockouts.
- Warn about medicines that will expire soon.
- Suggest moving medicine between nearby clinics.
- Find strange changes in medicine use.
- Let staff ask simple questions in a chat.
- Show a simple dashboard for managers.

## Who it helps

- Clinic nurses
- Clinic managers
- District health managers
- Patients who need chronic medicine
- Local government health budgets

## How it works

1. Clinics record stock, medicine use, and expiry dates (via SVS, RxSolution, or paper records).
2. Our program cleans and organizes the data.
3. It looks for patterns in past medicine use.
4. It predicts how much medicine each clinic will need.
5. It checks stock levels and expiry dates.
6. It suggests which clinic should send medicine to which clinic.
7. It sends warnings before a stockout or expiry problem.
8. Staff can ask questions like:  
   *"How many ARVs are left at Clinic A?"*  
   *"What is the TB medicine forecast for next month?"*
9. Managers can approve or reject suggestions.

## Main features

- Medicine demand prediction
- Stockout warnings
- Expiry warnings
- Redistribution suggestions
- Unusual pattern detection
- Simple chatbot
- Manager dashboard

## Data — we are using REAL data

We are committed to using **real South African public health data** wherever possible.

### Data sources we are pursuing

| Source | What it provides | Status |
|---|---|---|
| Mabizela et al. (2023) study | 392 medicines, 8 facilities in KwaZulu-Natal; stockout, overstocking, and expiry statistics | Contacting authors |
| District Health Barometer (Health Systems Trust) | District-level medicine availability indicators (CSV) | Downloaded 2018/19 |
| Stop Stockouts Project reports | Facility-level stockout survey data | Reviewing published reports |
| National Surveillance Centre (NSC) | Real-time medicine availability dashboards (SVS + RxSolution) | Requesting access via university |
| Department of Health | Potential anonymised SVS/RxSolution extracts | Preparing formal request |

### Data we need

- Medicine stock levels (per facility)
- Medicine use / dispensing records
- Expiry dates and batch numbers
- Clinic locations and catchment data
- Seasonal illness patterns
- Supplier delivery times
- Medicine redistribution records
- Staff queries (for chatbot training)

### Privacy and ethics

All data used will be anonymised. No patient-level data will be used.  
We will comply with POPIA (Protection of Personal Information Act).  
Any data request will be made through the university with proper academic justification.

## Tech stack

| Tool | Why we use it |
|---|---|
| Python | Main programming language |
| pandas | Clean and organize data |
| NumPy | Work with numbers and arrays |
| Prophet / statsmodels (ARIMA) | Learn past patterns and predict future medicine needs |
| scikit-learn | Help choose the best way to move medicine |
| TensorFlow / Keras | Find unusual patterns in medicine use |
| spaCy | Understand simple questions in the chatbot |
| Streamlit | Build a simple web dashboard |
| Plotly | Make charts and graphs |
| SQLite | Small local database for the prototype |
| GitHub | Store code, track tasks, and work as a team |

## Project goals

- Reduce medicine stockouts
- Reduce expired medicine waste
- Save money for public health
- Save nurses time
- Help patients get medicine without delays

## How we will know it works

- Forecast error below 15%
- Stockouts reduced by at least 20% in tests
- Expiry waste reduced by at least 15% in tests
- Chatbot understands at least 85% of test questions
- At least 80% of test users say it is helpful



## Folder structure (planned)

