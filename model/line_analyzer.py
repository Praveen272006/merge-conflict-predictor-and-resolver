def detect_risky_lines(commits):
    risky_locations = []

    for commit in commits:
        for file in commit.get("modified", []):
            if file.endswith(".py"):
                risky_locations.append({
                    "file": file,
                    "reason": "Python source modified (possible logic overlap)"
                })

    return risky_locations