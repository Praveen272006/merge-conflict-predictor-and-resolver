from fastapi import FastAPI, Request
from api.github_fetcher import get_commit_changes
from model.line_analyzer import detect_risky_lines
from model.risk_engine import predict_risk
from model.fusion_engine import calculate_conflict_score
from model.explainer import explain_prediction
from model.dev_graph import build_dev_graph
from api.github_bot import post_commit_comment

app = FastAPI()


@app.post("/github-webhook")
async def github_webhook(request: Request):

    payload = await request.json()

    repo_name = payload["repository"]["full_name"]
    commits = payload.get("commits", [])

    if not commits:
        return {"msg": "No commits"}

    all_risky = []
    total_changes = 0
    total_files = 0

    # ✅ IMPORTANT FIX → always use correct commit SHA
    latest_commit_sha = commits[-1]["id"]

    for commit in commits:

        sha = commit["id"]
        commit_data = get_commit_changes(repo_name, sha)

        risky = detect_risky_lines(commit_data)
        all_risky.extend(risky)

        files = commit_data.get("files", [])
        total_files += len(files)

        for f in files:
            total_changes += f.get("changes", 0)

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

    risky_text = "\n".join(
        [f"{r['file']} (Line {r['line']})" for r in all_risky[:5]]
    ) or "No risky lines"

    graph_text = "\n".join(graph[:5]) if graph else "Single developer"

    comment = f"""
🚀 AI Merge Conflict Analysis

🔥 Risk: {risk}
📊 Probability: {round(prob,2)}
⚡ Score: {round(score,2)}

Why:
{reasons}

Risky Areas:
{risky_text}

Developer Graph:
{graph_text}
"""

    # ✅ FINAL COMMENT POST
    post_commit_comment(repo_name, latest_commit_sha, comment)

    return {"status": "comment posted"}