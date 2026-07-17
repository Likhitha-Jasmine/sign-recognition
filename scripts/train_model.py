import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

DATASET_PATH = "dataset"
MODEL_PATH = "models/sign_model.pkl"

X = []
y = []

# Read dataset
for label in os.listdir(DATASET_PATH):
    label_path = os.path.join(DATASET_PATH, label)

    if not os.path.isdir(label_path):
        continue

    for file in os.listdir(label_path):
        if file.endswith(".csv"):
            file_path = os.path.join(label_path, file)
            data = pd.read_csv(file_path, header=None).values.flatten()

            # Ensure fixed length = 126
            if len(data) == 63:
                data = np.concatenate([data, np.zeros(63)])

            X.append(data)
            y.append(label)

X = np.array(X)
y = np.array(y)

print("Dataset loaded:", X.shape)

# Train classifier
model = RandomForestClassifier(n_estimators=200)
model.fit(X, y)

print("Training complete")

# Save model
os.makedirs("../models", exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("Model saved at", MODEL_PATH)