import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_commit_changes(repo_name, sha):
    url = f"https://api.github.com/repos/{repo_name}/commits/{sha}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    total_changes = 0
    files_changed = 0

    for file in data.get("files", []):
        total_changes += file.get("changes", 0)
        files_changed += 1

    return files_changed, total_changes