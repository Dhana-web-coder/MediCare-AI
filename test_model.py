import joblib
import pandas as pd

# Load trained model
data = joblib.load("../healthcare_model.pkl")

model = data["model"]
columns = data["feature_columns"]

# Sample patient
patient = pd.DataFrame([{
    "fever": "Yes",
    "cough": "Yes",
    "fatigue": "Yes",
    "difficulty_breathing": "No",
    "age": 25,
    "gender": "female",
    "blood_pressure": "Normal",
    "cholesterol_level": "Normal"
}])

# Convert categorical data
patient = pd.get_dummies(patient)

# Match training columns
patient = patient.reindex(columns=columns, fill_value=0)

# Predict
result = model.predict(patient)

print("Predicted Disease:", result[0])
print("ML TEST SUCCESS")