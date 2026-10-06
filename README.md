# UbuntuMed

**Smart medicine stock help for public clinics**

> _"Ubuntu" — I am because we are. Better medicine availability for all._

---

## What is UbuntuMed?

UbuntuMed is an AI-powered tool that helps public clinics and private pharmacies:

- **Predict** how much medicine each facility will need.
- **Warn** when stock is about to run out or expire.
- **Recommend** moving extra medicine between facilities before it is wasted.
- **Answer** simple questions in plain language through a chatbot.

We are **not** replacing existing systems like SVS or RxSolution.
We are adding a smart, predictive layer on top of them.

---

## Why This Matters

| Problem                                                                              | Evidence                              |
| ------------------------------------------------------------------------------------ | ------------------------------------- |
| Stockouts affected 85.6% of medicines                                                | Mabizela et al. (2023), KwaZulu-Natal |
| Overstocking affected 50.6% of medicines                                             | Same study                            |
| Expiry-related wastage affected 15.2%                                                | Same study                            |
| Overstocking and short-dated stock explained 68% of real redistribution transactions | Same study                            |
| AI-based platforms in Uganda reduced stockouts and overstocking by over 40%          | BMJ rapid response (2025)             |

---

## Architecture

[React Frontend]
|
| REST API
v
[FastAPI Backend]
| | |
v v v
[Postgres] [ML Models] [Chatbot NLP]

- **Backend:** FastAPI (Python)
- **Frontend:** React + Vite + Tailwind CSS
- **ML Models:** Prophet/ARIMA, TensorFlow autoencoder, spaCy intent classifier
- **Database:** SQLite for development, PostgreSQL for production
- **Deployment:** Render (backend), Vercel (frontend)

---

## Repository Structure

ubuntumed/
├── backend/ # FastAPI application
│ ├── app/
│ │ ├── api/ # API routes
│ │ ├── core/ # Config, database
│ │ ├── models/ # SQLAlchemy models
│ │ ├── schemas/ # Pydantic schemas
│ │ ├── services/ # Business logic
│ │ ├── ml/ # ML model loading and inference
│ │ └── utils/ # Helpers
│ └── tests/ # Backend tests
├── frontend/ # React application
│ └── src/
│ ├── components/
│ ├── pages/
│ ├── services/ # API calls
│ ├── hooks/
│ └── context/
├── data/
│ ├── raw/ # Original datasets (DHB, Zenodo, Kaggle)
│ ├── processed/ # Cleaned data
│ └── external/ # Reference stats, POPIA docs
├── notebooks/ # Jupyter notebooks for EDA
├── ml_training/ # Training scripts + saved models
├── docs/ # Project documentation
└── .github/ # GitHub templates + workflows

---

## Data Sources

| Dataset                                 | What It Provides                                                                 | Source                            |
| --------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------- |
| **District Health Barometer (2018/19)** | Real district-level medicine availability indicators                             | openAFRICA / Health Systems Trust |
| **Zenodo PLMIF**                        | Supply chain risk variables (port delays, spoilage, risk score) for South Africa | Zenodo                            |
| **Kaggle Pharmacy Dataset**             | Weekly demand, stock-on-hand, and stockout flags                                 | Kaggle                            |

See `docs/data_sources.md` for full details.

---

## Tech Stack

| Tool                | Purpose                              |
| ------------------- | ------------------------------------ |
| Python              | Main language                        |
| FastAPI             | Backend API                          |
| React + Vite        | Frontend                             |
| Tailwind CSS        | UI styling                           |
| pandas / NumPy      | Data processing                      |
| Prophet / ARIMA     | Demand forecasting                   |
| scikit-learn        | Optimisation and classification      |
| TensorFlow / Keras  | Anomaly detection                    |
| spaCy               | Chatbot NLP                          |
| SQLite / PostgreSQL | Database                             |
| Docker              | Containerisation                     |
| GitHub              | Version control and project tracking |

---

## Team Workflow

**Every task follows this chain:**

1. Pick an **Issue** from the GitHub Project board.
2. Create a **branch**: `feature/<issue-number>-short-description`.
3. **Commit** with meaningful messages: `feat(forecast): add Prophet model (#5)`.
4. Open a **Pull Request** and link the issue (`Closes #5`).
5. Get a **review** from another member.
6. **Merge** to `dev`, then to `main` at the end of the sprint.

**Rules:**

- No direct pushes to `main` or `dev`.
- Every PR needs at least one review.
- Every Sunday, we update `docs/contributions.md`.

---

## Getting Started (Local Development)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000
API docs at http://localhost:8000/docs

cd frontend
npm install
npm run dev
Frontend runs at http://localhost:5173

Docker (Full Stack)
docker-compose up --build

---

Documentation
All project documents are in docs/:

proposal.md — Project proposal

problem_definition.md — Problem statement

requirements.md — Functional and non-functional requirements

data_sources.md — Dataset descriptions and sources

data_dictionary.md — Column definitions for each dataset

architecture.md — System architecture

contributions.md — Weekly contribution log

deployment.md — Deployment instructions

---

---

#### File 5: `docs/architecture.md`

```markdown
# UbuntuMed — System Architecture

## Overview

UbuntuMed is a three-layer system:

1. **Presentation Layer (Frontend)** — React web app for clinic managers and nurses.
2. **Application Layer (Backend)** — FastAPI server that handles business logic and serves ML predictions.
3. **Data & Model Layer** — Databases, cleaned datasets, and trained ML models.

## Diagram

+---------------------------+
| React Frontend (Vercel) |
| Dashboard | Chatbot | UI |
+-------------+-------------+
|
| HTTPS / REST
v
+---------------------------+
| FastAPI Backend (Render) |
| /stock /forecast |
| /anomaly /redistribute |
| /chatbot |
+------+----------+---------+
| | |
v v v
+-----------+ +--------+ +-----------+
| Postgres | | ML | | NLP |
| Database | | Models | | Chatbot |
+-----------+ +--------+ +-----------+
```

## Components

### Frontend

- **Framework:** React + Vite
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **State:** React Context / hooks
- **API calls:** Axios

### Backend

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Auth:** JWT (future)
- **CORS:** Enabled for frontend URL

### ML Models

- **Forecasting:** Prophet / ARIMA (saved as `.pkl`)
- **Anomaly Detection:** Autoencoder (saved as `.h5`)
- **Redistribution:** scikit-learn logic (function-based)
- **Chatbot NLP:** spaCy / scikit-learn intent classifier (`.pkl`)

### Data

- **Raw:** DHB, Zenodo PLMIF, Kaggle pharmacy
- **Processed:** Cleaned and feature-engineered CSVs
- **Database:** SQLite (dev) / PostgreSQL (prod)

## Data Flow

1. Raw datasets are cleaned by `data_cleaning.py`.
2. Cleaned data is stored in `data/processed/` and loaded into the database.
3. ML training scripts read cleaned data and save models to `ml_training/saved_models/`.
4. FastAPI loads models at startup.
5. Frontend calls API endpoints and displays results.

## Deployment

| Layer    | Platform           | URL                           |
| -------- | ------------------ | ----------------------------- |
| Frontend | Vercel             | `ubuntumed.vercel.app`        |
| Backend  | Render             | `ubuntumed-api.onrender.com`  |
| Database | Supabase / Railway | (connection string in `.env`) |

## Security & Privacy

- POPIA compliance: no patient-level data.
- All data anonymised at facility level.
- HTTPS only in production.
- Environment variables for secrets.
- CORS restricted to frontend URL.
