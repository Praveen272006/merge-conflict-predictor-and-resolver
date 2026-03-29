def compute_conflict_score(
    files_changed,
    total_changes,
    ratio,
    commit_frequency,
    repo_activity,
    dev_conflicts
):
    """
    Behavioral Conflict Fusion Engine
    """

    w1 = 0.2   # Commit Frequency
    w2 = 0.25  # Change Density
    w3 = 0.2   # File Modification
    w4 = 0.15  # Repo Activity
    w5 = 0.2   # Developer Interaction

    CF = commit_frequency
    CD = ratio
    FMF = total_changes / 100
    RA = repo_activity
    DI = len(dev_conflicts)

    score = (
        (w1 * CF) +
        (w2 * CD) +
        (w3 * FMF) +
        (w4 * RA) +
        (w5 * DI)
    )

    return score