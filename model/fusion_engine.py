def calculate_conflict_score(features):

    w1, w2, w3, w4, w5 = 0.2, 0.25, 0.2, 0.15, 0.2

    CF = features.get("commit_frequency", 0)
    CD = features.get("change_density", 0)
    FMF = features.get("file_modification_frequency", 0)
    RA = features.get("repository_activity", 0)
    DI = features.get("developer_interaction", 0)

    score = (w1 * CF) + (w2 * CD) + (w3 * FMF) + (w4 * RA) + (w5 * DI)

    return score