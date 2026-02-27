import pandas as pd

commit_df = pd.read_csv("../data/commit_data.csv")
merge_df = pd.read_csv("../data/merge_commits.csv")

# combine datasets
df = commit_df.merge(merge_df, on="commit_hash")

# heuristic conflict labeling
df["conflict"] = (
    (df["is_merge_commit"] == 1) &
    (df["files_changed"] > 2) &
    (df["total_changes"] > 20)
).astype(int)

df.to_csv("../data/final_dataset.csv", index=False)

print("✅ Conflict labels generated!")