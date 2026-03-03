from fastapi import FastAPI, Request
from model.risk_engine import predict_risk
from api.github_bot import post_commit_comment
from model.explainer import explain_risk
from model.line_analyzer import detect_risky_lines
from api.github_fetcher import get_commit_changes

# =====================================================
# CREATE FASTAPI APP
# =====================================================
app = FastAPI()


# =====================================================
# PREDICT API (Manual Testing)
# =====================================================
@app.post("/predict")
def predict(
    files_changed: int,
    total_changes: int,
    ratio: float,
    large_change: int,
    multi_file: int,
    merge: int
):
    prob, level = predict_risk(
        files_changed,
        total_changes,
        ratio,
        large_change,
        multi_file,
        merge
    )

    reasons = explain_risk({
        "files_changed": files_changed,
        "total_changes": total_changes,
        "multi_file_change": multi_file,
        "merge_activity": merge
    })

    return {
        "conflict_probability": float(prob),
        "risk_level": level,
        "reasons": reasons
    }


# =====================================================
# GITHUB WEBHOOK
# =====================================================
@app.post("/github-webhook")
async def github_webhook(request: Request):

    payload = await request.json()

    repo_name = payload.get("repository", {}).get("full_name")
    commits = payload.get("commits", [])

    if not repo_name or not commits:
        return {"status": "no data"}

    files_changed = 0
    total_changes = 0
    all_risky_areas = []

    # -------------------------------------------------
    # PROCESS EACH COMMIT
    # -------------------------------------------------
    for commit in commits:

        sha = commit["id"]

        # 🔥 IMPORTANT: Fetch full commit details from GitHub API
        commit_details = get_commit_changes(repo_name, sha)

        # Count file + change stats
        commit_files = commit_details.get("files", [])
        files_changed += len(commit_files)

        for f in commit_files:
            total_changes += f.get("additions", 0)
            total_changes += f.get("deletions", 0)

        # Detect risky lines from full patch data
        risky_areas = detect_risky_lines(commit_details)
        all_risky_areas.extend(risky_areas)

    ratio = total_changes / max(files_changed, 1)

    large_change = 1 if total_changes > 200 else 0
    multi_file = 1 if files_changed > 3 else 0
    merge = 1

    # -------------------------------------------------
    # RISK PREDICTION
    # -------------------------------------------------
    prob, level = predict_risk(
        files_changed,
        total_changes,
        ratio,
        large_change,
        multi_file,
        merge
    )

    # -------------------------------------------------
    # EXPLAINABILITY
    # -------------------------------------------------
    reasons = explain_risk({
        "files_changed": files_changed,
        "total_changes": total_changes,
        "multi_file_change": multi_file,
        "merge_activity": merge
    })

    reason_text = (
        "\n".join([f"- {r}" for r in reasons])
        if reasons else "- No strong risk signals detected"
    )

    # -------------------------------------------------
    # BUILD RISK + RESOLUTION TEXT
    # -------------------------------------------------
    risk_area_text = ""
    resolution_text = ""

    for r in all_risky_areas:
        file = r.get("file")
        line = r.get("line")
        issue = r.get("issue")
        code = r.get("code")

        risk_area_text += f"\n- {file} (Line {line}) → {issue}"

        # Basic intelligent resolution
        suggested_fix = code.strip()

        resolution_text += f"""
📂 File: {file}
📍 Line: {line}

⚠ Issue:
{issue}

Current Code:
{code}

✅ Suggested Fix:
{suggested_fix}

Explanation:
This line was modified in the latest commit.
Verify consistency with related logic before merging.
"""

    if not risk_area_text:
        risk_area_text = "\n- No risky files detected"

    # -------------------------------------------------
    # AUTO RESOLVER POLICY
    # -------------------------------------------------
    HIGH_RATIO_THRESHOLD = 120
    HIGH_CHANGE_THRESHOLD = 400

    trigger_auto = (
        level == "HIGH"
        or ratio > HIGH_RATIO_THRESHOLD
        or total_changes > HIGH_CHANGE_THRESHOLD
    )

    auto_fix_message = ""

    if trigger_auto and resolution_text:
        auto_fix_message = f"""
---
### ⚡ Conflict Resolution Suggestions
{resolution_text}
"""

    # -------------------------------------------------
    # COMMENT MESSAGE
    # -------------------------------------------------
    message = f"""
🤖 **AI Merge Conflict Analysis**

### 🔥 Risk Level: **{level}**
### 📊 Probability: **{prob:.2f}**

---

### ⚠️ Why risk is {level}:
{reason_text}

---

### 📂 Risky Areas
{risk_area_text}

---

### 📈 Signals
- Files Changed: {files_changed}
- Total Changes: {total_changes}
- Change Ratio: {ratio:.2f}
- Large Change: {large_change}
- Multi File Commit: {multi_file}

{auto_fix_message}

⚡ Generated by **Merge Conflict Predictor AI**
"""

    # -------------------------------------------------
    # POST COMMENT
    # -------------------------------------------------
    for commit in commits:
        sha = commit["id"]
        post_commit_comment(repo_name, sha, message)

    return {
        "status": "analyzed",
        "risk_level": level,
        "probability": float(prob),
        "ratio": ratio,
        "auto_resolver_triggered": trigger_auto
    }


# =====================================================
# HEALTH CHECK
# =====================================================
@app.get("/")
def home():
    return {
        "status": "running",
        "service": "AI Merge Conflict Predictor"
    }