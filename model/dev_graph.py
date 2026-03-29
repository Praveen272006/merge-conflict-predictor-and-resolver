from collections import defaultdict

def build_dev_graph(commits):
    """
    Build developer interaction graph
    """

    file_dev_map = defaultdict(set)

    for commit in commits:

        author = commit.get("author", {}).get("name", "unknown")
        files = commit.get("modified", [])

        for filename in files:
            file_dev_map[filename].add(author)

    graph = []

    for file, devs in file_dev_map.items():
        devs = list(devs)

        # Multi developer conflict
        if len(devs) > 1:
            for i in range(len(devs)):
                for j in range(i + 1, len(devs)):
                    graph.append(f"{devs[i]} ⇄ {devs[j]} (file: {file})")

        # Single developer activity
        else:
            graph.append(f"{devs[0]} → modified {file}")

    return graph