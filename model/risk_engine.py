def predict_risk(features):

    score = (
        features["commit_frequency"] * 0.2 +
        features["change_density"] * 0.3 +
        features["file_modification_frequency"] * 0.2 +
        features["repository_activity"] * 0.1 +
        features["developer_interaction"] * 0.2
    )

    prob = min(score / 100, 1.0)

    if prob < 0.3:
        risk = "LOW"
    elif prob < 0.7:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return prob, risk