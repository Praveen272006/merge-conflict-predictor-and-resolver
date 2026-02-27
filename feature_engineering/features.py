import pandas as pd

df = pd.read_csv("../data/final_dataset.csv")

# ----- Feature Engineering -----

# Change intensity
df["change_ratio"] = df["lines_added"] / (df["lines_deleted"] + 1)

# Large change indicator
df["large_change"] = (df["total_changes"] > 50).astype(int)

# Multi-file modification
df["multi_file_change"] = (df["files_changed"] > 2).astype(int)

# Merge activity
df["merge_activity"] = df["is_merge_commit"]

# Save engineered dataset
df.to_csv("../data/features.csv", index=False)

print("✅ Features Generated Successfully")