from git import Repo
import pandas as pd
import os

repos_dir = "../repositories"

merge_data = []

for repo_name in os.listdir(repos_dir):

    repo_path = os.path.join(repos_dir, repo_name)

    if not os.path.isdir(repo_path):
        continue

    print(f"Analyzing merges in {repo_name}")

    repo = Repo(repo_path)

    for commit in repo.iter_commits():

        parent_count = len(commit.parents)

        merge_data.append({
            "repo": repo_name,
            "commit_hash": commit.hexsha,
            "is_merge_commit": 1 if parent_count > 1 else 0
        })

df = pd.DataFrame(merge_data)

df.to_csv("../data/merge_commits.csv", index=False)

print("✅ Merge commit dataset created!")