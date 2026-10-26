from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)

API_URL = 'https://ubuntumed-api.onrender.com'

@app.route('/')
def dashboard():
    records = []
    recommendations = []
    stock_labels = []
    stock_data_chart = []
    expiry_chart_data = [15, 5, 2]  # Mock: [Valid, Expiring Soon, Expired]

    try:
        # timeout=60 allows the free-tier backend to wake up (takes ~50s)
        response = requests.get(f'{API_URL}/stock', timeout=60)
        if response.status_code == 200:
            data = response.json().get('stock_data', [])

            for i, item in enumerate(data):
                status = "VALID"
                if item['status'] == 'Stockout':
                    status = "EXPIRED"
                elif item['status'] == 'Low':
                    status = "EXPIRING SOON"

                records.append({
                    'id': i + 1,
                    'name': item['medicine'],
                    'batch': f"BATCH-{100+i}",
                    'quantity': item['quantity'],
                    'price': 25.50,
                    'expiry_date': item['expiry'],
                    'status': status
                })

                if item['status'] in ['Low', 'Stockout']:
                    recommendations.append({
                        'name': item['medicine'],
                        'current_stock': item['quantity'],
                        'threshold': 100,
                        'recommended_buy': 500
                    })

                if len(stock_labels) < 8:
                    stock_labels.append(f"{item['clinic']} - {item['medicine']}")
                    stock_data_chart.append(item['quantity'])

    except Exception as e:
        print(f"Error connecting to FastAPI: {e}")

    return render_template('index.html',
                           records=records,
                           recommendations=recommendations,
                           stock_labels=stock_labels,
                           stock_data=stock_data_chart,
                           expiry_chart_data=expiry_chart_data)

@app.route('/add', methods=['POST'])
def add_stock():
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)