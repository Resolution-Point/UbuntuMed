from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)
API_URL = 'http://127.0.0.1:8000'

@app.route('/')
def dashboard():
    records = []
    recommendations = []
    stock_labels = []
    stock_data_chart = []
    expiry_chart_data = [15, 5, 2] # Mock data: [Valid, Expiring Soon, Expired]

    try:
        # Fetch data from your FastAPI backend
        response = requests.get(f'{API_URL}/stock')
        if response.status_code == 200:
            data = response.json().get('stock_data', [])

            for i, item in enumerate(data):
                # 1. Translate FastAPI data into what the HTML table expects
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

                # 2. Create Recommendations if stock is low
                if item['status'] in ['Low', 'Stockout']:
                    recommendations.append({
                        'name': item['medicine'],
                        'current_stock': item['quantity'],
                        'threshold': 100,
                        'recommended_buy': 500
                    })

                # 3. Prepare data for the Bar Chart
                if len(stock_labels) < 8: # Limit to 8 bars for the chart
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
    # This handles the form submission from the HTML.
    # For the demo, we just redirect back to the dashboard.
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)