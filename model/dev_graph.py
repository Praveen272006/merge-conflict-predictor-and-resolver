from collections import defaultdict

def build_dev_graph(commits):
    file_dev_map = defaultdict(set)

    for commit in commits:
        author = commit.get("author", {}).get("name", "unknown")

        for file in commit.get("modified", []):
            filename = file.get("filename")
            file_dev_map[filename].add(author)

    graph = []

    for file, devs in file_dev_map.items():
        devs = list(devs)
        if len(devs) > 1:
            for i in range(len(devs)):
                for j in range(i + 1, len(devs)):
                    graph.append(f"{devs[i]} --- {file} --- {devs[j]}")

    return graph