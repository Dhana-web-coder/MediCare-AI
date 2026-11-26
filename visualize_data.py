import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/Cleaned_Dataset.csv")

# Count diseases
disease_counts = df["disease"].value_counts().head(15)

# Create horizontal bar chart
plt.figure(figsize=(10, 7))
disease_counts.sort_values().plot(kind="barh")

plt.title("Top 15 Disease Distribution")
plt.xlabel("Number of Records")
plt.ylabel("Disease")

plt.tight_layout()
plt.show()
# Check duplicate records
print("\nDuplicate Records:")
print(df.duplicated().sum())

# Check data types
print("\nData Types:")
print(df.dtypes)

# Check disease categories
print("\nDisease Categories:")
print(df["disease"].unique())

# Check gender categories
print("\nGender Categories:")
print(df["gender"].unique())
print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

print("\nDisease Categories:")
print(df["disease"].unique())

print("\nGender Categories:")
print(df["gender"].unique())