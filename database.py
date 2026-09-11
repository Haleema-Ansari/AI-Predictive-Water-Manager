import sqlite3

def create_database():

    connection = sqlite3.connect("prediction_history.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            soil_moisture REAL NOT NULL,
            temperature REAL NOT NULL,
            air_humidity REAL NOT NULL,
            pump_required INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

create_database()    