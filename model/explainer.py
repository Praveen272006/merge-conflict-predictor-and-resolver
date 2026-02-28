def explain_risk(features):
    reasons = []

    if features["files_changed"] > 5:
        reasons.append("Many files modified")

    if features["total_changes"] > 300:
        reasons.append("Large code changes")

    if features["multi_file_change"]:
        reasons.append("Multi-file commit increases conflict chance")

    if features["merge_activity"]:
        reasons.append("Recent merge activity detected")

    return reasons