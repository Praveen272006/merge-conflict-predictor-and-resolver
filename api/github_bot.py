import requests
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def post_commit_comment(repo, commit_sha, comment):

    url = f"https://api.github.com/repos/{repo}/commits/{commit_sha}/comments"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {"body": comment}

    res = requests.post(url, headers=headers, json=data)

    print("Commit Comment Status:", res.status_code)