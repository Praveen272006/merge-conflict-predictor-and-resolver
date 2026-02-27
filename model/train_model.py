import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

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

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

joblib.dump(model, "conflict_model.pkl")

print("✅ Model Saved")