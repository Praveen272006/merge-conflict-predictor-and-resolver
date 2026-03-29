def calculate_conflict_score(features):
    """
    Calculate conflict score using weighted factors
    """

    # weights (you can tune these)
    w1 = 0.2  # commit frequency
    w2 = 0.25 # change density
    w3 = 0.2  # file modification
    w4 = 0.15 # repo activity
    w5 = 0.2  # developer interaction

    CF = features.get("commit_frequency", 0)
    CD = features.get("change_density", 0)
    FMF = features.get("file_modification_frequency", 0)
    RA = features.get("repository_activity", 0)
    DI = features.get("developer_interaction", 0)

    score = (w1 * CF) + (w2 * CD) + (w3 * FMF) + (w4 * RA) + (w5 * DI)

    return score