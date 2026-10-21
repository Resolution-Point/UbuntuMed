
from pathlib import Path
from datetime import date, timedelta

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

BASE = Path(__file__).parent

inventory = pd.read_csv(
    BASE / "UbuntuMed_Inventory.CSV" / "ubuntumed_inventory.csv"
)

data = pd.read_csv(
    BASE / "ubuntumed_chatbot_training_dataset.csv"
)

print("Dataset loaded successfully!")
print("Number of questions:", len(data))
print("Intents:", data["intent"].unique())

# --------------------------------------------------
# 2. TRAIN THE CHATBOT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    data["text"],
    data["intent"],
    test_size=0.2,
    random_state=42,
    stratify=data["intent"]
)

chatbot = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000))
])

chatbot.fit(X_train, y_train)

predictions = chatbot.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\nModel test accuracy: {accuracy:.2%}")

# --------------------------------------------------
# 3. CHATBOT RESPONSES
# --------------------------------------------------

responses = {
    "check_stock": "I'll check the available medicine stock.",
    "forecast_demand": "Demand forecasting is not connected yet.",
    "check_expiry": "I'll check medicine expiry dates.",
    "request_transfer": "Medicine transfer suggestions are not connected yet.",
    "detect_anomaly": "Stock anomaly detection is not connected yet."
}

medicine_aliases = {
    "arv": "ARVs",
    "arvs": "ARVs",
    "flu": "Flu medicine",
    "paracetamol": "Paracetamol",
    "amoxicillin": "Amoxicillin"
}

# --------------------------------------------------
# 4. FIND CLINIC AND MEDICINE
# --------------------------------------------------

def find_clinic(question_lower):
    clinics = sorted(
        inventory["clinic"].dropna().unique(),
        key=len,
        reverse=True
    )

    return next(
        (clinic for clinic in clinics
         if clinic.lower() in question_lower),
        None
    )


def find_medicine(question_lower):
    medicines = sorted(
        inventory["medicine"].dropna().unique(),
        key=len,
        reverse=True
    )

    exact = next(
        (medicine for medicine in medicines
         if medicine.lower() in question_lower),
        None
    )

    if exact:
        return exact

    words = (
        question_lower
        .replace("?", " ")
        .replace(",", " ")
        .replace(".", " ")
        .split()
    )

    for word in words:
        if word in medicine_aliases:
            return medicine_aliases[word]

    return None

# --------------------------------------------------
# 5. CHATBOT LOOP
# --------------------------------------------------

print("\nUbuntuMed Chatbot is ready!")
print("Type 'exit' to stop.\n")

while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        print("UbuntuMed: Goodbye!")
        break

    if not question:
        continue

    intent = chatbot.predict([question])[0]

    print("Predicted intent:", intent)

    question_lower = question.lower()
    clinic = find_clinic(question_lower)

    # --------------------------------------------------
    # 6. CHECK MEDICINE STOCK
    # --------------------------------------------------

    if intent == "check_stock":
        medicine = find_medicine(question_lower)

        if not clinic or not medicine:
            print(
                "UbuntuMed: Please include a clinic name "
                "and medicine name."
            )
            continue

        result = inventory[
            (inventory["clinic"] == clinic) &
            (inventory["medicine"].str.lower() == medicine.lower())
        ]

        if not result.empty:
            quantity = result["quantity"].sum()

            print(
                f"UbuntuMed: {clinic} has {quantity} "
                f"units of {medicine}."
            )
        else:
            print("UbuntuMed: No matching stock record found.")

    # --------------------------------------------------
    # 7. CHECK MEDICINE EXPIRY
    # --------------------------------------------------

    elif intent == "check_expiry":
        records = inventory.copy()

        records["expiry_date"] = pd.to_datetime(
            records["expiry_date"],
            errors="coerce"
        ).dt.date

        if clinic:
            records = records[records["clinic"] == clinic]

        today = date.today()
        cutoff_date = today + timedelta(days=30)

        expired = records[
            records["expiry_date"].notna() &
            (records["expiry_date"] < today)
        ]

        expiring = records[
            records["expiry_date"].notna() &
            (records["expiry_date"] >= today) &
            (records["expiry_date"] <= cutoff_date)
        ]

        if expired.empty and expiring.empty:
            print(
                "UbuntuMed: No expired medicines or medicines "
                "expiring within 30 days were found."
            )
            continue

        if not expired.empty:
            print("\nUbuntuMed: EXPIRED MEDICINES")

            for _, row in expired.iterrows():
                print(
                    f"- {row['clinic']}: {row['medicine']}, "
                    f"{row['quantity']} units; expired "
                    f"on {row['expiry_date']}."
                )

        if not expiring.empty:
            print("\nUbuntuMed: MEDICINES EXPIRING WITHIN 30 DAYS")

            for _, row in expiring.iterrows():
                days_left = (row["expiry_date"] - today).days

                print(
                    f"- {row['clinic']}: {row['medicine']}, "
                    f"{row['quantity']} units; expires "
                    f"on {row['expiry_date']} "
                    f"({days_left} days left)."
                )

    # --------------------------------------------------
    # 8. OTHER FEATURES NOT CONNECTED YET
    # --------------------------------------------------

    else:
        print(
            "UbuntuMed:",
            responses.get(
                intent,
                "Sorry, I don't understand that question yet."
            )
        )
