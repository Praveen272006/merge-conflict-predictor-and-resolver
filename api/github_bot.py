import os
import requests
from dotenv import load_dotenv

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