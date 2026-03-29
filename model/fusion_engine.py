def compute_conflict_score(features):

    CF = features.get("commit_frequency", 1)
    CD = features.get("change_density", 1)
    FMF = features.get("file_mod_freq", 1)
    RA = features.get("repo_activity", 1)
    DI = features.get("dev_interaction", 1)

    w1, w2, w3, w4, w5 = 0.2, 0.25, 0.2, 0.15, 0.2

    score = (w1 * CF) + (w2 * CD) + (w3 * FMF) + (w4 * RA) + (w5 * DI)

    return round(score, 2)