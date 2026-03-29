import os
import subprocess

repos = [
    "https://github.com/scikit-learn/scikit-learn.git",
    "https://github.com/pallets/flask.git",
    "https://github.com/fastapi/fastapi.git",
    "https://github.com/pandas-dev/pandas.git",
    "https://github.com/django/django.git"
]

base_dir = "../repositories"

os.makedirs(base_dir, exist_ok=True)

for repo in repos:
    name = repo.split("/")[-1].replace(".git", "")
    path = os.path.join(base_dir, name)

    if not os.path.exists(path):
        print(f"Cloning {name}...")
        subprocess.run(["git", "clone", repo, path])
    else:
        print(f"{name} already exists")

print("✅ All repositories ready!")