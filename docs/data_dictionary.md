# UbuntuMed — Data Dictionary

This document explains the variables (columns) present in the datasets used for the UbuntuMed prototype and Machine Learning models.

## Core Dataset: `ubuntumed_test_data.csv` (and Kaggle operational data)

| Column Name     | Data Type         | Description                                       | Example      |
| :-------------- | :---------------- | :------------------------------------------------ | :----------- |
| `date`          | Date (YYYY-MM-DD) | The date the medicine was dispensed or recorded.  | `2026-10-15` |
| `clinic`        | String            | The name of the healthcare facility.              | `Clinic A`   |
| `medicine`      | String            | The name of the medication.                       | `ARVs`       |
| `quantity_used` | Integer           | The number of units dispensed on that date.       | `150`        |
| `stock_on_hand` | Integer           | The total number of units remaining in inventory. | `450`        |
| `expiry_date`   | Date (YYYY-MM-DD) | The date the current batch of medicine expires.   | `2027-01-30` |

## Machine Learning Output Variables

| Variable Name      | Data Type | Description                                                                             | Used In                |
| :----------------- | :-------- | :-------------------------------------------------------------------------------------- | :--------------------- |
| `predicted_demand` | Integer   | The AI model's forecast of how many units will be needed next month.                    | Demand Forecasting     |
| `anomaly`          | Integer   | Flag indicating if a week's usage was normal or abnormal. `1` = Normal, `-1` = Anomaly. | Isolation Forest Model |
| `detected_intent`  | String    | The classified category of a user's chatbot question.                                   | NLP Chatbot            |
