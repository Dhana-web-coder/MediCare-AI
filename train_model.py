import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load dataset
df = pd.read_csv("data/Cleaned_Dataset.csv")

# Input features
X = df[
    [
        "fever",
        "cough",
        "fatigue",
        "difficulty_breathing",
        "age",
        "gender",
        "blood_pressure",
        "cholesterol_level",
    ]
]

# Target
y = df["disease"]

# Convert categorical data
X = pd.get_dummies(X)

# Split dataset (without stratify)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model and columns
joblib.dump(
    {
        "model": model,
        "feature_columns": list(X.columns)
    },
    "healthcare_model.pkl"
)

print("\nModel saved successfully!")