def calculate_conflict_score(features):

    return (
        features["commit_frequency"] * 0.2 +
        features["change_density"] * 0.25 +
        features["file_modification_frequency"] * 0.2 +
        features["repository_activity"] * 0.15 +
        features["developer_interaction"] * 0.2
    )