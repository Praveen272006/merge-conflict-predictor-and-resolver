import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_commit_changes(repo_name, sha):
    url = f"https://api.github.com/repos/{repo_name}/commits/{sha}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("GitHub API error:", response.status_code)
        return {}

    return response.json()