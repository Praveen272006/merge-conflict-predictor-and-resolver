from collections import defaultdict

def build_dev_graph(commits):

    file_dev_map = defaultdict(set)

    for commit in commits:
        author = commit.get("author", {}).get("name", "unknown")
        files = commit.get("modified", [])

        for f in files:
            file_dev_map[f].add(author)

    graph = []

    for file, devs in file_dev_map.items():
        devs = list(devs)

        if len(devs) > 1:
            graph.append(f"{devs[0]} ⇄ {devs[1]} (file: {file})")
        else:
            graph.append(f"{devs[0]} → {file}")

    return graph