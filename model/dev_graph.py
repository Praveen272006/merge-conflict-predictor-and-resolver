from collections import defaultdict

dev_map = defaultdict(set)

def update_dev_graph(commits):
    for commit in commits:
        author = commit.get("author", {}).get("name", "unknown")

        for file in commit.get("modified", []):
            filename = file.get("filename")
            dev_map[filename].add(author)

def get_conflict_risk_from_graph():
    risk_files = []

    for file, devs in dev_map.items():
        if len(devs) > 1:
            risk_files.append({
                "file": file,
                "developers": list(devs)
            })

    return risk_files