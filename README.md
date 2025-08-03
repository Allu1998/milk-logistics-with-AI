# Milk Logistics AI

A web-based platform to optimize dairy supply chain operations using AI-driven demand forecasting, inventory management, supplier management, and predictive vehicle maintenance.

---

## Features

- **Demand Forecasting:**  
  Uses ARIMA time series model to predict milk demand for the next 7 days based on historical supplier data.

- **Inventory Management:**  
  Tracks current and safety stock for milk products. Automatically updates inventory when new supplier data is added or uploaded.

- **Supplier Management:**  
  Add suppliers manually or via Excel/CSV upload. Calculates supplier earnings and persists data.

- **Predictive Maintenance:**  
  Uses Linear Regression to predict days until each vehicle needs service, based on mileage and age.

- **Scheduling Recommendation:**  
  Suggests optimal times for milk pickup based on forecasted demand and current stock.

---

## Technology Stack

- **Backend:** Python, Flask, Pandas, NumPy, scikit-learn, statsmodels, openpyxl
- **Frontend:** HTML, JavaScript, Chart.js
- **Data Storage:** Excel/CSV files
- **APIs:** RESTful endpoints

---

## Setup Instructions

1. **Clone the Repository**
    ```
    git clone <your-repo-url>
    cd milk_logistics_ai
    ```

2. **Install Python Dependencies**
    ```
    pip install flask flask-cors pandas numpy scikit-learn statsmodels openpyxl
    ```

3. **Run the Backend**
    ```
    python app.py
    ```
    The Flask server will start at `http://127.0.0.1:5000/`.

4. **Open the Dashboard**
    - Open `dashboard.html` in your web browser.

---

## Usage

- **Refresh All Data:**  
  Click the "Refresh All Data" button to update all dashboard sections.

- **Add Supplier:**  
  Use the form to add a new supplier manually.

- **Upload Supplier File:**  
  Upload an Excel (.xlsx) or CSV (.csv) file to replace all supplier data and update inventory.

- **View Forecast:**  
  The "Demand Forecast (Next 7 Days)" section displays predicted milk demand.

- **View Inventory:**  
  The inventory section shows current and safety stock levels.

- **View Maintenance:**  
  The predictive maintenance section shows which vehicles need servicing soon.

---

## How Demand Forecasting Works

- The system uses all supplier delivery records as historical sales data.
- When new supplier data is added or uploaded, the ARIMA model is retrained automatically.
- The `/forecast` endpoint always returns predictions based on the latest data.

---

## Project Structure

```
milk_logistics_ai/
│
├── app.py              # Flask backend with all API endpoints and AI logic
├── dashboard.html      # Frontend dashboard
├── suppliers.xlsx      # Supplier data (Excel)
├── vehicles.xlsx       # Vehicle data (Excel)
└── README.md           # Project documentation
```

---

## Extending the Project

- Add authentication and user roles
- Integrate with real-time IoT sensors for live inventory
- Deploy on a cloud platform for scalability
- Add advanced analytics and reporting

