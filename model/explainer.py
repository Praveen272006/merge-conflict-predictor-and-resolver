def explain_prediction(features):
    """
    Generate human-readable explanation for risk prediction
    """

    reasons = []

    if features["commit_frequency"] > 3:
        reasons.append("• High commit frequency detected")

    if features["change_density"] > 50:
        reasons.append("• Large number of code changes")

    if features["file_modification_frequency"] > 5:
        reasons.append("• Multiple files modified")

    if features["repository_activity"] > 3:
        reasons.append("• High repository activity")

    if features["developer_interaction"] > 1:
        reasons.append("• Multiple developers involved")

    # fallback
    if not reasons:
        reasons.append("• Recent merge activity detected")

    return "\n".join(reasons)