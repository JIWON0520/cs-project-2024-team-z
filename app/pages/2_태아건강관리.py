import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_is_fitted
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from datetime import datetime
import sqlite3
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import random

class WeightedMajorityVoteClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, classifiers, weights=None):
        self.classifiers = classifiers
        self.weights = weights if weights else [1] * len(classifiers)

    def fit(self, X, y):
        for clf in self.classifiers:
            clf.fit(X, y)
        return self

    def predict(self, X):
        check_is_fitted(self, 'classifiers')
        predictions = np.asarray([clf.predict(X) for clf in self.classifiers])
        weighted_votes = np.zeros((len(X), np.max(predictions) + 1))
        for index, (clf_predictions, weight) in enumerate(zip(predictions, self.weights)):
            for i, prediction in enumerate(clf_predictions):
                weighted_votes[i, prediction] += weight
        return np.argmax(weighted_votes, axis=1)

    def predict_proba(self, X):
        check_is_fitted(self, 'classifiers')
        probas = np.asarray([clf.predict_proba(X) * weight for clf, weight in zip(self.classifiers, self.weights)])
        return np.sum(probas, axis=0) / np.sum(self.weights)

model_filename = '../models/FHRModel.pkl'
wmv_clf = joblib.load(model_filename)

features = [
    'LB', 'AC', 'FM', 'UC', 'DL', 'DS', 'DP', 'ASTV', 'MSTV', 'ALTV', 'MLTV',
    'Width', 'Min', 'Max', 'Nmax', 'Nzeros', 'Mode', 'Mean', 'Median', 'Variance', 'Tendency'
]

def setup_database():
    conn = sqlite3.connect('database/fhr_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS plot_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            plot BLOB NOT NULL,
            predictions TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_plot_to_db(username, plot, predictions):
    conn = sqlite3.connect('database/fhr_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO plot_history (username, date, plot, predictions)
        VALUES (?, ?, ?, ?)
    ''', (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), plot, predictions))
    conn.commit()
    conn.close()

def get_plot_history(username):
    conn = sqlite3.connect('database/fhr_data.db')
    df = pd.read_sql('''
        SELECT date, plot FROM plot_history
        WHERE username = ?
        ORDER BY date DESC
    ''', conn, params=(username,))
    conn.close()
    return df

def display_gallery(history_df):
    images = []
    captions = []
    for idx, row in history_df.iterrows():
        image = Image.open(BytesIO(row['plot']))
        images.append(image)
        captions.append(f"Date: {row['date']}")

    if images:
        st.image(images, caption=captions, width=300)

def main():
    setup_database()

    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.sidebar.warning("로그인을 먼저 해주세요.")
        st.stop()

    USER = st.session_state['user']
    username = USER[0]
    st.title("📟 태아 심박동 모니터링")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)

            if all(col in data.columns for col in features):
                X = data[features]
                predictions = wmv_clf.predict(X)
                data['Anomaly'] = predictions
                st.write("Data with Predictions:")
                st.write(data)

                anomaly_class = data.loc[0, 'Anomaly']
                messages = {
                    1: "아기가 잘있어요!🥰",
                    2: "아기가 위험한것같아요!😲",
                    3: "아기가 위험해요!😟"
                }
                message = messages.get(anomaly_class, "알 수 없는 상태")
                st.markdown(f"<h1 style='text-align: center; color: black;'>{message}</h1>", unsafe_allow_html=True)

                image_dir = './images/fhr_plots'
                try:
                    images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
                    if images:
                        random_image = random.choice(images)
                        st.image(random_image, caption="Fetal Heart Rate Plot")
                        # Save random image to DB
                        with open(random_image, 'rb') as f:
                            random_image_bytes = f.read()
                        save_plot_to_db(username, random_image_bytes, data.to_json())
                    else:
                        st.error("No images found in the specified directory.")
                except Exception as e:
                    st.error(f"Failed to load images from {image_dir}: {str(e)}")
            else:
                st.error("Uploaded file does not contain the required features.")
        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")
    else:
        st.info("Please upload a CSV file.")

    if st.button("이전 기록"):
        history_df = get_plot_history(username)
        display_gallery(history_df)

if __name__ == "__main__":
    main()
