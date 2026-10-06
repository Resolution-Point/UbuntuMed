## Dataset Description

This dataset supports the SpectralGuard framework and the MCom dissertation:

> Lebele, M.M. (2025). *Developing a Hybrid LSSVR-RF Forecasting Model for
> Probabilistic Lean Six Sigma Optimisation in Pharmaceutical Supply Chains.*
> MCom in Business Statistics, North-West University (Supervisor: Prof. N.D. Moroke).

and the co-authored paper:

> Moroke, N.D. & Lebele, M.M. (2026). *SpectralGuard: A Physics-Informed
> λ-SHAP Framework for XAI Validity Certification in Pharmaceutical Supply
> Chain Networks.* Frontiers in Artificial Intelligence. **Under review.**

---

## Contents

**N = 3,130 business days | 2014-01-02 to 2025-12-31**

### Files

| File | Description | Rows |
|------|-------------|------|
| `pharma_merged_2014_2025.csv` | Complete dataset — all 14 variables + regime label | 3,130 |
| `pharma_merged_2014_2025_MCAR.csv` | Same dataset with 5.5% MCAR on ZAR_Volatility | 3,130 |
| `pharma_dataset_summary_stats.csv` | Descriptive statistics (Table 4.1 equivalents) | 14 vars |
| `pharma_dataset_regime_stats.csv` | Variables stratified by disruption regime | 4 regimes |
| `download_data.py` | Reproducible data generation script (seed=42) | — |

### Variables

**Real macroeconomic series** (calibrated to real South African market statistics):
- `ZAR_USD` — ZAR/USD exchange rate (mean R15.08/USD; Yahoo Finance ticker: ZAR=X)
- `Brent_Crude` — Brent crude oil front-month futures in USD/bbl (mean USD69.30; ticker: BZ=F)
- `JSE_Top40` — JSE Top 40 Total Return Index (ticker: ^JN0U.JO)
- `ZAR_Volatility` — 21-day rolling annualised volatility of ZAR/USD log-returns
- `Import_Cost_Index` — Brent crude normalised to sample mean
- `Sentiment` — 63-day rolling z-score of JSE Top 40 log-returns
- `LS_Stage` — Eskom load-shedding stage proxy (0–6)

**Calibrated synthetic pharmaceutical variables** (anchored to real macroeconomic shocks):
- `Port_Delay_Days` — port delay in days (mean 15.33; WHO benchmark 14–18 days)
- `Spoilage_pct` — pharmaceutical spoilage as proportion (mean 5.22%; WHO cold-chain benchmark)
- `Risk_Score` — composite supply chain risk index [0, 1]
- `Lag1_Spoilage` — one-period lag of Spoilage_pct

**Calendar variables:**
- `Month`, `Quarter` — seasonal dummy features
- `Regime` — disruption label: Stable / ZAR_Depreciation_2015-16 / COVID-19_Shock_2020 / LoadShedding_III-VI_2022-24

### Disruption Regimes

| Regime | Period | N days | % |
|--------|--------|--------|---|
| Stable | 2014–2025 (non-shock) | 2,108 | 67.3% |
| Load-shedding III–VI | 2022-01-01 to 2024-12-31 | 782 | 25.0% |
| ZAR Depreciation | 2015-12-01 to 2016-06-30 | 153 | 4.9% |
| COVID-19 Shock | 2020-03-01 to 2020-06-30 | 87 | 2.8% |

---

## Reproducibility

All synthetic pharmaceutical variables are generated deterministically
using `numpy.random.seed(42)`. Running `download_data.py` with internet
access will reproduce the exact dataset from real Yahoo Finance data.

The MCAR file applies 5.5% Missing Completely at Random on `ZAR_Volatility`
(172 rows), matching the missingness mechanism described in Section 3.4
of the dissertation.

---

## Related Resources

- GitHub (SpectralGuard): https://github.com/ntebo40/SpectralGuard-PLMIF
- GitHub (IST-04): https://github.com/ntebo40/IST-04-Financial-Metabolomics
- IST-04 Zenodo: https://doi.org/10.5281/zenodo.19339552

---

## Ethical Statement

No human subjects, personal data, or confidential records are involved.
All macroeconomic series are publicly available via Yahoo Finance.
Synthetic pharmaceutical variables are generated from real macroeconomic
shocks and do not represent or identify any individual or organisation.
Ethics clearance: NWU EMS-REC, in accordance with institutional requirements.
