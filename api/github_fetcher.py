import requests
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_commit_changes(repo_name, sha):
    """
    Returns:
    files_changed, total_changes, full_commit_data
    """

    url = f"https://api.github.com/repos/{repo_name}/commits/{sha}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("GitHub API error:", response.status_code)
        return 0, 0, {}

    data = response.json()

    files = data.get("files", [])

    files_changed = len(files)

    total_changes = 0
    for f in files:
        total_changes += f.get("additions", 0) + f.get("deletions", 0)

    return files_changed, total_changes, data