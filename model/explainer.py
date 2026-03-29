def explain_prediction(features):

    reasons = []

    if features["commit_frequency"] > 3:
        reasons.append("• High commit frequency")

    if features["change_density"] > 50:
        reasons.append("• Large code changes")

    if features["file_modification_frequency"] > 5:
        reasons.append("• Many files modified")

    if features["developer_interaction"] > 1:
        reasons.append("• Multiple developers involved")

    if not reasons:
        reasons.append("• Normal development activity")

    return "\n".join(reasons)