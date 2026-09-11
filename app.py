from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_pump
from datetime import datetime
from database import create_database
import sqlite3

app = FastAPI()


class SensorData(BaseModel):
    soil_moisture: float
    temperature: float
    air_humidity: float


@app.get("/")
def home():
    return {"message": "AI Predictive Water Manager API is running"}


@app.post("/predict")
def predict(data: SensorData):

    # Generate exact receive time
    now = datetime.now()

    # ML prediction
    result = predict_pump(
        data.soil_moisture,
        data.temperature,
        data.air_humidity
    )

    # Save prediction history
    connection = sqlite3.connect("prediction_history.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO prediction_history (
            date,
            time,
            soil_moisture,
            temperature,
            air_humidity,
            pump_required,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        now.strftime("%d-%m-%Y"),
        now.strftime("%H:%M:%S"),
        data.soil_moisture,
        data.temperature,
        data.air_humidity,
        result["pump_required"],
        result["status"]
    ))

    connection.commit()
    connection.close()

    # Return current reading + exact receive time + prediction
    return {
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%H:%M:%S"),
        "soil_moisture": data.soil_moisture,
        "temperature": data.temperature,
        "air_humidity": data.air_humidity,
        "pump_required": result["pump_required"],
        "status": result["status"]
    }


@app.get("/history")
def get_history():

    connection = sqlite3.connect("prediction_history.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            date,
            time,
            soil_moisture,
            temperature,
            air_humidity,
            pump_required,
            status
        FROM prediction_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    history = []

    for record in records:
        history.append({
            "id": record[0],
            "date": record[1],
            "time": record[2],
            "soil_moisture": record[3],
            "temperature": record[4],
            "air_humidity": record[5],
            "pump_required": record[6],
            "status": record[7]
        })

    return history