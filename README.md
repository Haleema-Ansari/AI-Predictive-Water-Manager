# AI Predictive Water Manager — ML Model

This repository contains the Machine Learning component of the **AI Predictive Water Manager** project.

## Objective

The ML model predicts whether the water pump should be **ON or OFF** based on:

* Soil Moisture
* Temperature
* Air Humidity

This is a **Binary Classification** problem.

### Prediction Meaning

* `1` → Pump ON / Water Required
* `0` → Pump OFF / Water Not Required

## Model

The final model used is a **Random Forest Classifier**.

The trained model is saved as:

`water_pump_model.joblib`

The model achieved:

* Test Accuracy: **100%**
* Cross-Validation Mean Accuracy: **99.83%**
* Tuned Random Forest CV Accuracy: **99.875%**

## Files

### `water_pump_model.joblib`

Contains the trained Random Forest ML model.

### `model.py`

Contains the prediction function used to make predictions from sensor values.

### `requirements.txt`

Contains the required Python libraries and their versions.

### `Untitled.ipynb`

Contains the ML workflow including:

* Data loading
* Data inspection
* Data analysis
* Train/Test split
* Model training
* Model comparison
* Cross-validation
* Feature importance
* Hyperparameter tuning
* Final model saving

### `dataset/dataset_clean_final.csv`

Cleaned dataset used for model development and evaluation.

## Installation

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Using the Model

Import the prediction function:

```python
from model import predict_pump
```

Call the function with sensor values:

```python
result = predict_pump(400, 28, 60)
print(result)
```

Example output:

```json
{
    "pump_required": 1,
    "status": "Pump ON"
}
```

## Input

The model expects:

```text
soil_moisture
temperature
air_humidity
```

Example:

```text
Soil Moisture = 400
Temperature = 28
Air Humidity = 60
```

## Output

```text
pump_required = 1 → Pump ON
pump_required = 0 → Pump OFF
```

## Backend Integration

The backend can import the prediction function from `model.py` and pass the sensor readings received from the hardware/IoT system.

Flow:

```text
Sensors / ESP32
       ↓
Backend API
       ↓
model.py
       ↓
Random Forest Model
       ↓
Pump ON / OFF Prediction
       ↓
Frontend Dashboard
```

## Important Note

The `soil_moisture` value should be provided in the same scale as the training data (approximately **315–985 raw sensor values**).

If the hardware provides soil moisture as a percentage (0–100%), a proper calibration/conversion must be established before sending the value to the model.
