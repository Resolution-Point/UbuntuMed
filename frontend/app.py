from flask import Flask, render_template

@app.route("/")
def index():
    # ... your backend logic ...
    return render_template("index.html", records=processed_records, recommendations=purchase_recommendations)