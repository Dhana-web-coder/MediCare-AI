import joblib
import pandas as pd

# Load trained model
data = joblib.load("healthcare_model.pkl")

model = data["model"]
features = data["feature_columns"]

# Sample patient details
patient = {
    "age": 35,
    "blood_pressure": 120,
    "cholesterol_level": 180,
    "fever_Yes": 1,
    "cough_Yes": 1,
    "fatigue_Yes": 0,
    "difficulty_breathing_Yes": 0,
    "gender_male": 1
}

# Convert input into DataFrame
input_data = pd.DataFrame([patient], columns=features)

# Predict
prediction = model.predict(input_data)

print("Healthcare Prediction:", prediction[0])
from recommendation import health_recommendation

health_recommendation(str(prediction[0]))