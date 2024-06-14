# 2024 C&S Project Results

## Overview

Our project integrates a user-centric X+AI Service for monitoring maternal and fetal health, utilizing a mobile application platform powered by PyTorch AI models and a MySQL database backend. 

### Key Components
- **User Interface**: Targeted towards expectant mothers, allowing real-time data collection via mobile devices.
- **AI Models**: Utilize PyTorch for analyzing fetal heart rate (FHR) and maternal health data to predict health indicators and potential risks.
- **Database**: MySQL is employed to store collected sensor data and AI-generated insights, enhancing predictive accuracy.
- **Application**: Developed using Streamlit, providing a seamless user interface for interactive data visualization and management.

## Features

### Login/Register System
- **Functionality**: Users can register and login using a username and password.
- **Data Handling**: User-specific data such as due dates and baby nicknames are stored securely in our SQL database.

### Health Monitoring
- **Pregnant Women Health Check**: Inputs for systolic/diastolic blood pressure, blood sugar, heart rate, and body temperature. Health status is categorized into three levels: Low, Middle, High.
- **Fetal Health Check**: Analyzes sensor data from a CSV file containing 22 features to assess fetal health.

### Predictive Models
- **MHR (Maternal Heart Rate)**: Implemented using a Random Forest Classifier.
- **FHR (Fetal Heart Rate)**: An ensemble model combining Logistic Regression, Decision Tree Classifier, and SVC, informed by literature on early diagnosis from fetal cardiotocography datasets.

### Hospital Reservation System
- **Functionality**: Allows users to locate nearby obstetrics and gynecology hospitals and clinics via an integrated Google Maps interface, view contact details and ratings, and make reservations easily.

### Calendar and Diary
- **Personal Scheduler**: Users can view and manage their hospital appointments and personal notes.
- **Diary**: Provides a platform for writing and storing personal diaries, with entries reflecting scheduled appointments and personal experiences.

## Achievements
- **Application Functionality**: 100% completion of the planned features including health checks, hospital finder, and calendar system.
- **Model Accuracy**: Achieved 83% for MHR and 91.9% for FHR against a target based on literature benchmarks of 85% and 100%, respectively.

## Future Directions
- **Model Improvement**: Aiming to enhance AI model performance for near-perfect predictions.
- **Hospital Collaboration**: To expand our reservation system into a fully functional network linked with actual hospitals.
- **Real-time Data Collection**: Integrating IoT devices for live data feeds to further improve predictive accuracy.

## Project Limitations
- The project currently operates in a demo phase with simulated data inputs, necessitating future adaptations for live operational environments.

