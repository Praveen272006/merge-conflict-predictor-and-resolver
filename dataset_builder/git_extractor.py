from git import Repo
import pandas as pd
import os

# Folder containing cloned repositories
repos_dir = "../repositories"

# Limit commits per repository (VERY IMPORTANT FOR SPEED)
MAX_COMMITS = 3000

all_data = []

for repo_name in os.listdir(repos_dir):

    repo_path = os.path.join(repos_dir, repo_name)

    if not os.path.isdir(repo_path):
        continue

    print(f"\n🚀 Processing {repo_name}")

    repo = Repo(repo_path)

    # ----- LOOP THROUGH COMMITS -----
    for i, commit in enumerate(repo.iter_commits()):

        # STOP after limit
        if i >= MAX_COMMITS:
            print(f"✅ {repo_name}: reached {MAX_COMMITS} commits limit")
            break

        # progress display
        if i % 500 == 0:
            print(f"{repo_name}: processed {i} commits")

        stats = commit.stats.total

        all_data.append({
            "repo": repo_name,
            "commit_hash": commit.hexsha,
            "files_changed": len(commit.stats.files),
            "lines_added": stats['insertions'],
            "lines_deleted": stats['deletions'],
            "total_changes": stats['lines']
        })

print("\n💾 Saving combined dataset...")

# ----- SAVE DATASET -----
df = pd.DataFrame(all_data)

df.to_csv("../data/commit_data.csv", index=False)

print("✅ Combined dataset created successfully!")
print(f"📊 Total commits collected: {len(df)}")