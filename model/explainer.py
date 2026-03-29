def explain_prediction(features):

    reasons = []

    if features["change_density"] > 50:
        reasons.append("• Large code changes")

    if features["file_modification_frequency"] > 5:
        reasons.append("• Many files modified")

    if features["commit_frequency"] > 3:
        reasons.append("• Frequent commits")

    if not reasons:
        reasons.append("• Normal activity")

    return "\n".join(reasons)