import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def post_comment(repo_name, pr_number, comment):
    """
    Post comment to GitHub Pull Request
    """

    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "body": comment
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("✅ Comment posted successfully")
    else:
        print("❌ Failed to post comment:", response.status_code, response.text)