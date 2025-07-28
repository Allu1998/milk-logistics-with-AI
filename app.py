# Added 'send_from_directory' to serve the HTML file
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings
from datetime import date, timedelta, datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import os

warnings.filterwarnings("ignore")
SUPPLIERS_FILE = 'suppliers.xlsx'

def load_suppliers():
    if os.path.exists(SUPPLIERS_FILE):
        return pd.read_excel(SUPPLIERS_FILE).to_dict('records')
    return []

def save_suppliers(suppliers_list):
    pd.DataFrame(suppliers_list).to_excel(SUPPLIERS_FILE, index=False)

# --- (All data and model setup code remains the same) ---
csv_data = """Date,ProductID,QuantitySold
2025-07-01,101,150
2025-07-02,101,155
2025-07-03,101,160
2025-07-04,101,175
2025-07-05,101,180
2025-07-06,101,140
2025-07-07,101,152
"""
df_arima = pd.read_csv(pd.io.common.StringIO(csv_data)); df_arima['Date'] = pd.to_datetime(df_arima['Date']); df_arima.set_index('Date', inplace=True)
time_series_data = df_arima[['QuantitySold']]
model = ARIMA(time_series_data, order=(2,1,1)); model_fit = model.fit(); forecast = model_fit.forecast(steps=7)
forecast_data = {str(k.date()): round(v, 2) for k, v in forecast.items()}
inventory_data = {"101": {"name": "Whole Milk", "current_stock": 1000, "safety_stock": 1200}, "102": {"name": "Skim Milk", "current_stock": 800, "safety_stock": 600}}
vehicle_history_data = [{'mileage': 20000, 'age_years': 1, 'days_until_service': 150}, {'mileage': 60000, 'age_years': 3, 'days_until_service': 45}, {'mileage': 80000, 'age_years': 4, 'days_until_service': 15}, {'mileage': 10000, 'age_years': 5, 'days_until_service': 25}, {'mileage': 30000, 'age_years': 2, 'days_until_service': 110}]
X_train = np.array([[v['mileage'], v['age_years']] for v in vehicle_history_data]); y_train = np.array([v['days_until_service'] for v in vehicle_history_data])
maintenance_model = LinearRegression(); maintenance_model.fit(X_train, y_train)
current_vehicle_fleet = [{'id': 'V01', 'model': 'Refrigerated Van', 'mileage': 25000, 'age_years': 1}, {'id': 'V02', 'model': 'Refrigerated Van', 'mileage': 75000, 'age_years': 4}, {'id': 'V03', 'model': 'Pickup Truck', 'mileage': 95000, 'age_years': 5}]


# --- API Setup ---
# The new 'static_folder' argument tells Flask where to find the HTML file
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# --- NEW: Route to serve the dashboard.html file ---
@app.route("/")
def serve_dashboard():
    return send_from_directory('.', 'dashboard.html')

# --- (All other API endpoints for data remain the same) ---
@app.route("/forecast")
def get_forecast(): return jsonify(forecast_data)
@app.route("/inventory")
def get_inventory(): return jsonify(inventory_data)
@app.route("/schedule")
def get_schedule():
    total_demand = sum(forecast_data.values()); current_stock = inventory_data["101"]["current_stock"]
    recommendation = "No immediate pickup needed.";
    if current_stock < total_demand: pickup_date = date.today() + timedelta(days=2); recommendation = f"Urgent: Schedule new milk pickup for {pickup_date.strftime('%Y-%m-%d')}."
    return jsonify({"recommendation": recommendation})
@app.route("/maintenance")
def get_maintenance_predictions():
    for vehicle in current_vehicle_fleet: features = np.array([[vehicle['mileage'], vehicle['age_years']]]); predicted_days = maintenance_model.predict(features); vehicle['predicted_service_in_days'] = int(predicted_days[0])
    return jsonify(current_vehicle_fleet)
@app.route("/suppliers", methods=["GET"])
def get_suppliers():
    suppliers_list = load_suppliers()
    for supplier in suppliers_list:
        if 'quantity_liters' in supplier and 'price_per_liter' in supplier: supplier["earnings"] = round(supplier["quantity_liters"] * supplier["price_per_liter"], 2)
    return jsonify(suppliers_list)
@app.route("/suppliers", methods=["POST"])
def add_supplier():
    suppliers_list = load_suppliers()
    next_id = max([s['id'] for s in suppliers_list]) + 1 if suppliers_list else 1
    data = request.json
    new_supplier = { "id": next_id, "supplier_name": data.get("supplier_name"), "address": data.get("address"), "quantity_liters": data.get("quantity_liters"), "price_per_liter": data.get("price_per_liter"), "submitted_by": data.get("submitted_by"), "timestamp": datetime.now().isoformat() }
    suppliers_list.append(new_supplier)
    save_suppliers(suppliers_list)
    if new_supplier["quantity_liters"]: inventory_data["101"]["current_stock"] += new_supplier["quantity_liters"]
    return jsonify({"message": "Supplier added successfully", "supplier": new_supplier}), 201
@app.route("/suppliers/<int:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id):
    suppliers_list = load_suppliers()
    supplier_to_update = next((s for s in suppliers_list if s["id"] == supplier_id), None)
    if supplier_to_update is None: return jsonify({"error": "Supplier not found"}), 404
    data = request.json
    supplier_to_update["supplier_name"] = data.get("supplier_name", supplier_to_update["supplier_name"])
    supplier_to_update["address"] = data.get("address", supplier_to_update["address"])
    supplier_to_update["quantity_liters"] = data.get("quantity_liters", supplier_to_update["quantity_liters"])
    supplier_to_update["price_per_liter"] = data.get("price_per_liter", supplier_to_update["price_per_liter"])
    save_suppliers(suppliers_list)
    return jsonify({"message": "Supplier updated successfully", "supplier": supplier_to_update})

if __name__ == '__main__':
    app.run(debug=True, port=5000)