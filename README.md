# AI Predictive Water Manager

An AI-powered irrigation management system that uses sensor readings and a Machine Learning model to predict whether the water pump should be **ON or OFF**.

## Project Objective

The main objective of this project is to develop an intelligent water management system that analyzes environmental and soil conditions and predicts whether irrigation is required.

The system performs **binary classification**:

* `1` → Pump ON / Water Required
* `0` → Pump OFF / Water Not Required

The prediction is based on:

* Soil Moisture
* Temperature
* Air Humidity

---

## System Architecture

```text
Sensors
   ↓
ESP32 / Microcontroller
   ↓
FastAPI
   ↓
Machine Learning Model
   ↓
Pump ON / OFF Prediction
   ↓
SQLite Prediction History
   ↓
Frontend Dashboard
```

---

## Machine Learning Model

The project uses a **Random Forest Classifier** from Scikit-Learn.

### Model Selection

Three classification models were evaluated:

| Model               | Accuracy |
| ------------------- | -------: |
| Logistic Regression |   99.83% |
| Decision Tree       |   99.83% |
| Random Forest       |     100% |

Random Forest was selected as the final model.

### Cross-Validation

The initial Random Forest model achieved a mean 5-fold cross-validation accuracy of approximately:

**99.83%**

After hyperparameter tuning using GridSearchCV:

**Best CV Accuracy: 99.875%**

The tuned model achieved:

**Test Accuracy: 100%**

---

## Important Feature Finding

Feature importance analysis showed that **soil moisture is the dominant feature** in the current dataset.

Approximate feature importance:

* Soil Moisture → 97.80%
* Air Humidity → 1.11%
* Temperature → 1.09%

This indicates that pump prediction in the current dataset is primarily driven by soil moisture.

---

## Dataset

The dataset contains **3000 records** and four columns:

* Soil Moisture
* Temperature
* Air Humidity
* Pump Data

There are no missing values or duplicate rows in the cleaned dataset.

The target variable is:

`Pump Data`

---

## Project Structure

```text
AI-Predictive-Water-Manager/
│
├── app.py
├── model.py
├── water_pump_model.joblib
├── database.py
├── requirements.txt
├── README.md
├── Untitled.ipynb
│
└── dataset/
    └── dataset_clean_final.csv
```

### File Description

| File                      | Purpose                                              |
| ------------------------- | ---------------------------------------------------- |
| `app.py`                  | FastAPI application and API endpoints                |
| `model.py`                | Loads the trained model and performs predictions     |
| `water_pump_model.joblib` | Trained Random Forest model                          |
| `database.py`             | Creates the SQLite prediction history database       |
| `requirements.txt`        | Required Python dependencies                         |
| `Untitled.ipynb`          | Machine Learning development and evaluation notebook |
| `dataset_clean_final.csv` | Cleaned dataset                                      |

---

# FastAPI API

The trained model is integrated into FastAPI for real-time predictions.

## Start the API

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the FastAPI application:

```bash
uvicorn app:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### 1. Home

**GET `/`**

Used to check whether the API is running.

Example response:

```json
{
  "message": "AI Predictive Water Manager API is running"
}
```

---

### 2. Prediction

**POST `/predict`**

Receives sensor readings and returns the ML prediction.

### Input

```json
{
  "soil_moisture": 420,
  "temperature": 29,
  "air_humidity": 58
}
```

### Output

```json
{
  "date": "11-09-2026",
  "time": "18:42:17",
  "soil_moisture": 420,
  "temperature": 29,
  "air_humidity": 58,
  "pump_required": 1,
  "status": "Pump ON"
}
```

The date and time represent the **time when FastAPI received the sensor reading**.

The timestamp is stored along with the prediction in the SQLite database.

---

### 3. Prediction History

**GET `/history`**

Returns previously stored sensor readings and predictions.

Example:

```json
[
  {
    "id": 1,
    "date": "11-09-2026",
    "time": "18:42:17",
    "soil_moisture": 420,
    "temperature": 29,
    "air_humidity": 58,
    "pump_required": 1,
    "status": "Pump ON"
  }
]
```

---

## Prediction Function

The ML model can also be used directly through `model.py`.

Example:

```python
from model import predict_pump

result = predict_pump(
    soil_moisture=420,
    temperature=29,
    air_humidity=58
)

print(result)
```

Output:

```python
{
    "pump_required": 1,
    "status": "Pump ON"
}
```

---

## Database

The project uses **SQLite** to store prediction history.

The database records:

* ID
* Date
* Time
* Soil Moisture
* Temperature
* Air Humidity
* Pump Required
* Pump Status

The database file is generated automatically when the application is initialized.

`prediction_history.db` is a runtime-generated file and should not be committed to GitHub.

---

## Frontend Integration

The frontend dashboard can communicate with the FastAPI backend.

The dashboard can display:

* Current soil moisture
* Current temperature
* Current air humidity
* Current pump status
* Last reading date
* Last reading time
* Prediction history

The frontend can use:

```text
POST /predict
```

for new sensor readings and:

```text
GET /history
```

to display previous predictions.

---

## Hardware Integration

The intended hardware flow is:

```text
Soil Moisture Sensor
        +
Temperature Sensor
        +
Humidity Sensor
        ↓
      ESP32
        ↓
   FastAPI /predict
        ↓
   ML Prediction
        ↓
     Pump ON/OFF
```

The ESP32 sends sensor values to the FastAPI prediction endpoint.

---

## Technologies Used

### Programming & Data Science

* Python
* Pandas
* NumPy
* Scikit-Learn
* Matplotlib
* Joblib

### Machine Learning

* Logistic Regression
* Decision Tree
* Random Forest
* GridSearchCV
* Cross-Validation

### Backend

* FastAPI
* Uvicorn
* Pydantic

### Database

* SQLite

### Development

* Jupyter Notebook
* VS Code

---

## Model Input

The model expects three features:

```text
soil_moisture
temperature
air_humidity
```

The soil moisture values in the current dataset are raw sensor-scale readings rather than percentage values.

---

## Model Output

```text
0 → Pump OFF
1 → Pump ON
```

The API additionally provides a human-readable status:

```text
Pump ON
Pump OFF
```

---

## Future Improvements

Possible future improvements include:

* Real-time ESP32 sensor integration
* Live frontend dashboard
* Automatic pump control
* Larger real-world sensor dataset
* Continuous model retraining with new sensor data
* Cloud deployment
* Real-time monitoring and alerts
* More advanced time-series prediction


## Important Note

The `soil_moisture` value should be provided in the same scale as the training data (approximately **315–985 raw sensor values**).

If the hardware provides soil moisture as a percentage (0–100%), a proper calibration/conversion must be established before sending the value to the model.
