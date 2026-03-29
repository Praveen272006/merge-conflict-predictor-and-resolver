def predict_risk(features):

    CF = features.get("commit_frequency", 0)
    CD = features.get("change_density", 0)
    FMF = features.get("file_modification_frequency", 0)
    RA = features.get("repository_activity", 0)
    DI = features.get("developer_interaction", 0)

    score = (CF * 0.2) + (CD * 0.3) + (FMF * 0.2) + (RA * 0.1) + (DI * 0.2)

    prob = min(score / 100, 1.0)

    if prob < 0.3:
        risk = "LOW"
    elif prob < 0.7:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return prob, risk