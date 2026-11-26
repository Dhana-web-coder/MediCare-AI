import sqlite3
import pandas as pd

DB_NAME = "medicare.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patient_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender TEXT,
            symptoms TEXT,
            prediction TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_patient(age, gender, symptoms, prediction):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        INSERT INTO patient_history
        (age, gender, symptoms, prediction)
        VALUES (?, ?, ?, ?)
    """, (age, gender, symptoms, prediction))
    conn.commit()
    conn.close()


def get_patient_history():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT * FROM patient_history", conn
    )
    conn.close()
    return df


def create_appointment_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            doctor_name TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            status TEXT DEFAULT 'Booked'
        )
    """)
    conn.commit()
    conn.close()


def save_appointment(patient_name, doctor_name,
                     appointment_date, appointment_time):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        INSERT INTO appointments
        (patient_name, doctor_name, appointment_date,
         appointment_time, status)
        VALUES (?, ?, ?, ?, 'Booked')
    """, (patient_name, doctor_name,
          appointment_date, appointment_time))
    conn.commit()
    conn.close()


def get_appointments():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT * FROM appointments", conn
    )
    conn.close()
    return df


def cancel_appointment(appointment_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        UPDATE appointments
        SET status = 'Cancelled'
        WHERE id = ?
    """, (appointment_id,))
    conn.commit()
    conn.close()