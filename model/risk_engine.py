import os
import joblib

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "conflict_model.pkl")

model = joblib.load(model_path)

def predict_risk(files_changed, total_changes, ratio,
                 large_change, multi_file, merge):

    probs = model.predict_proba([[
        files_changed,
        total_changes,
        ratio,
        large_change,
        multi_file,
        merge
    ]])

    # ---- FIX FOR SINGLE CLASS MODEL ----
    if probs.shape[1] == 1:
        prob = float(probs[0][0])
    else:
        prob = float(probs[0][1])

    # Risk level
    if prob > 0.7:
        level = "HIGH"
    elif prob > 0.4:
        level = "MEDIUM"
    else:
        level = "LOW"

    return prob, level