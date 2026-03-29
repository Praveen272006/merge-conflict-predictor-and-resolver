from fastapi import FastAPI, Request
from api.github_fetcher import get_commit_changes
from api.github_bot import post_commit_comment

from model.risk_engine import predict_risk
from model.fusion_engine import calculate_conflict_score
from model.explainer import explain_prediction
from model.dev_graph import build_dev_graph
from model.resolution_engine import generate_resolution
from model.signals import calculate_signals

app = FastAPI()


@app.post("/github-webhook")
async def github_webhook(request: Request):

    payload = await request.json()

    repo_name = payload["repository"]["full_name"]
    commits = payload.get("commits", [])

    if not commits:
        return {"msg": "No commits"}

    latest_sha = commits[-1]["id"]

    total_changes = 0
    total_files = 0

    # =========================
    # PROCESS COMMITS
    # =========================
    for commit in commits:
        data = get_commit_changes(repo_name, commit["id"])
        files = data.get("files", [])

        total_files += len(files)

        for f in files:
            total_changes += f.get("changes", 0)

    # =========================
    # FEATURES
    # =========================
    features = {
        "commit_frequency": len(commits),
        "change_density": total_changes,
        "file_modification_frequency": total_files,
        "repository_activity": len(commits),
        "developer_interaction": len(commits)
    }

    prob, risk = predict_risk(features)
    score = calculate_conflict_score(features)
    reasons = explain_prediction(features)

    graph = build_dev_graph(commits)
    signals = calculate_signals(commits, total_files, total_changes)

    # =========================
    # RESOLUTION
    # =========================
    latest_data = get_commit_changes(repo_name, latest_sha)
    resolutions = generate_resolution(latest_data)

    # =========================
    # RISKY AREAS
    # =========================
    risky_text = ""

    for r in resolutions:
        risky_text += f"• {r['file']} (Line {r['line']}) → {r['issue']}\n"

    if not risky_text:
        risky_text = "• No risky lines"

    # =========================
    # RESOLUTION OUTPUT
    # =========================
    resolution_text = ""

    for r in resolutions:

        resolution_text += f"""
📄 File: {r['file']}
📍 Line: {r['line']}
⚠️ Issue: {r['issue']}

💻 Code for Branch A:
{r['old_code']}


💻 Code for Branch B:
{r['new_code']}


🛠 Suggested Fix:
{r['fix']}


💡 Explanation:
{r['explanation']}

----------------------------------
"""

    graph_text = "\n".join(graph[:5]) if graph else "• Single developer"

    # =========================
    # FINAL COMMENT
    # =========================
    comment = f"""
🚀 AI Merge Conflict Analysis

🔥 Risk Level: {risk}
📊 Probability: {round(prob,2)}
⚡ Conflict Score: {round(score,2)}

----------------------------------

⚠️ Why Risk:
{reasons}

----------------------------------

📂 Risky Areas:
{risky_text}

----------------------------------

👥 Developer Interaction:
{graph_text}

----------------------------------

🛠 Conflict Resolution Suggestions:
{resolution_text}

----------------------------------

📊 Signals:
• Files Changed: {signals['files_changed']}
• Total Changes: {signals['total_changes']}
• Change Ratio: {signals['ratio']}
• Large Change: {signals['large_change']}
• Multi File Commit: {signals['multi_file']}
• Merge Commit: {signals['merge']}
"""

    post_commit_comment(repo_name, latest_sha, comment)

    return {"status": "success"}