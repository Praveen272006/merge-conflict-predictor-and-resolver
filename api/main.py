from fastapi import FastAPI, Request
from api.github_fetcher import get_commit_changes
from api.github_bot import post_commit_comment

from model.line_analyzer import detect_risky_lines
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

    latest_commit_sha = commits[-1]["id"]

    all_risky = []
    total_changes = 0
    total_files = 0

    for commit in commits:

        sha = commit["id"]
        commit_data = get_commit_changes(repo_name, sha)

        risky = detect_risky_lines(commit_data)
        all_risky.extend(risky)

        files = commit_data.get("files", [])
        total_files += len(files)

        for f in files:
            total_changes += f.get("changes", 0)

    # Features
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

    # 🔥 RESOLUTION
    commit_data_latest = get_commit_changes(repo_name, latest_commit_sha)
    resolutions = generate_resolution(commit_data_latest)

    resolution_text = ""
    for r in resolutions:
        resolution_text += f"""
📄 File: {r['file']}
📍 Line: {r['line']}
⚠️ Issue: {r['issue']}
🔴 Current Code: {r['code']}
🟢 Suggested Fix: {r['fix']}
💡 Explanation: {r['explanation']}
----------------------------------
"""

    risky_text = "\n".join(
        [f"• {r['file']} (Line {r['line']})" for r in all_risky[:5]]
    ) or "• No risky lines"

    graph_text = "\n".join(graph[:5]) if graph else "• Single developer"

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

    post_commit_comment(repo_name, latest_commit_sha, comment)

    return {"status": "success"}