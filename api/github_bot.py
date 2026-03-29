import os
import requests
from dotenv import load_dotenv
import requests
import re

def extract_lines(patch):
    matches = re.findall(r'\@\@ -\d+,\d+ \+(\d+),(\d+) \@\@', patch)

    lines = []
    for start, length in matches:
        lines.append((int(start), int(start)+int(length)))

    return lines

def get_commit_files(repo, sha, token):

    url = f"https://api.github.com/repos/{repo}/commits/{sha}"

    headers = {
        "Authorization": f"token {token}"
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    risky = []

    for f in data["files"]:
        risky.append({
            "file": f["filename"],
            "changes": f["changes"],
            "patch": f.get("patch", "")
        })

    return risky

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

def post_commit_comment(repo_full_name, commit_sha, message):

    url = f"https://api.github.com/repos/{repo_full_name}/commits/{commit_sha}/comments"

    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "body": message
    }

    response = requests.post(url, headers=headers, json=data)

    print("GitHub response:", response.status_code)