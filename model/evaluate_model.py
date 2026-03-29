import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("../data/features.csv")

features = [
    "files_changed",
    "total_changes",
    "change_ratio",
    "large_change",
    "multi_file_change",
    "merge_activity"
]

X = df[features]
y = df["conflict"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Load trained model
model = joblib.load("conflict_model.pkl")

# Predictions
y_pred = model.predict(X_test)

# ---- Confusion Matrix ----
ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
plt.title("Merge Conflict Prediction - Confusion Matrix")
plt.show()

# ---- Feature Importance ----
importances = model.feature_importances_

plt.figure()
plt.bar(features, importances)
plt.title("Feature Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()