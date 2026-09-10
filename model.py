
import joblib 
import pandas as pd
model = joblib.load("water_pump_model.joblib")

def predict_pump(soil_moisture, temperature, air_humidity):
    input_data = pd.DataFrame([{
        "Soil Moisture": soil_moisture,
        "Temperature": temperature,
        "Air Humidity": air_humidity
    }])

    prediction = model.predict(input_data)[0]

    return {
        "pump_required": int(prediction),
        "status": "Pump ON" if prediction == 1 else "Pump OFF"
    }
