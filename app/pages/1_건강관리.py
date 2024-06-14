import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import joblib

def setup_database():
    with sqlite3.connect('database/health_data.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS health_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                measurement_type TEXT,
                value REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def insert_data(username, measurement_type, value):
    with sqlite3.connect('database/health_data.db') as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO health_data (username, measurement_type, value)
            VALUES (?, ?, ?)
        ''', (username, measurement_type, value))
        conn.commit()

def fetch_data(username, measurement_type):
    with sqlite3.connect('database/health_data.db') as conn:
        return pd.read_sql(f'''
            SELECT value, timestamp FROM health_data
            WHERE username = ? AND measurement_type = ?
            ORDER BY timestamp
        ''', conn, params=(username, measurement_type))

def plot_trends(username, measurement_type):
    df = fetch_data(username, measurement_type)
    if df.empty:
        st.write("No data available to plot.")
        return
    plt.figure(figsize=(10, 4))
    plt.plot(pd.to_datetime(df['timestamp']), df['value'], marker='o', linestyle='-')
    plt.title(f'{measurement_type.replace("_", " ").capitalize()} Trend', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.grid(True)
    st.pyplot(plt)

def load_model_scaler():
    try:
        rf_model = joblib.load('../models/MHRModel.pkl')
        scaler = joblib.load('../models/MHRScaler.pkl')
    except FileNotFoundError:
        st.error("Model or scaler file not found.")
        return None, None
    return rf_model, scaler

def predict_risk(username, rf_model, scaler):
    with sqlite3.connect('database/health_data.db') as conn:
        df = pd.read_sql(f'''
            SELECT measurement_type, value, MAX(timestamp) AS max_time
            FROM health_data
            WHERE username = ?
            GROUP BY measurement_type
        ''', conn, params=(username,))
    if df.shape[0] < 5:
        st.warning("Insufficient data to predict risk.")
        return

    # Extracting latest values
    latest_values = df.sort_values('max_time', ascending=False).groupby('measurement_type').first()['value'].reindex([
        'systolic_bp', 'diastolic_bp', 'blood_sugar', 'heart_rate', 'temperature'])
    input_data = latest_values.values.reshape(1, -1)
    if np.any(np.isnan(input_data)):
        st.warning("Complete data not available for prediction.")
        return

    input_data_scaled = scaler.transform(input_data)
    risk_prediction = rf_model.predict(input_data_scaled)[0]
    st.success(f"Predicted Risk Level: {'Low' if risk_prediction == 0 else 'Medium' if risk_prediction == 1 else 'High'}")

def display_data_entry_and_trends(username):
    st.title(":heartbeat: 산모 건강 관리")

    with st.form("Data Entry"):
        systolic = st.number_input("Systolic Blood Pressure (mm Hg)", min_value=50, max_value=200)
        diastolic = st.number_input("Diastolic Blood Pressure (mm Hg)", min_value=30, max_value=150)
        bs = st.number_input("Blood Sugar (mg/dL)", min_value=0, max_value=50)
        hr = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200)
        temp = st.number_input("Body Temperature (°F)", min_value=95, max_value=104)
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        insert_data(username, 'systolic_bp', systolic)
        insert_data(username, 'diastolic_bp', diastolic)
        insert_data(username, 'blood_sugar', bs)
        insert_data(username, 'heart_rate', hr)
        insert_data(username, 'temperature', temp)
        st.success("Data added successfully!")

    rf_model, scaler = load_model_scaler()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Predict Risk"):
            predict_risk(username, rf_model, scaler)
    with col2:
        if st.button("View Trends"):
            for mt in ['systolic_bp', 'diastolic_bp', 'blood_sugar', 'heart_rate', 'temperature']:
                plot_trends(username, mt)

if __name__ == "__main__":
    setup_database()
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.sidebar.warning("로그인을 먼저 해주세요.")
        st.stop()
    username = st.session_state['user'][0]  # Assuming username is stored at index 0
    display_data_entry_and_trends(username)
