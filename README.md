# UbuntuMed

**Smart medicine stock help for public clinics**

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

We are **not** replacing the systems clinics already use.  
We are adding a smart helper on top of them.

Our program will:

- Learn from past medicine use.
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

1. Clinics record stock, medicine use, and expiry dates.
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

## Tech stack (planned)

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

## Data we plan to use

- Medicine stock levels
- Medicine use records
- Expiry dates and batch numbers
- Clinic locations
- Number of patients
- Seasonal illness patterns
- Delivery times from suppliers
- Medicine transfer records
- Simple text questions from staff


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

