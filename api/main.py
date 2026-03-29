from fastapi import FastAPI, Request
from model.risk_engine import predict_risk
from api.github_bot import post_commit_comment
from model.explainer import explain_risk
from model.line_analyzer import detect_risky_lines
from api.github_fetcher import get_commit_changes

app = FastAPI()


# =====================================================
# PREDICT API
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
    all_risky = []

    # 🔥 LOOP THROUGH COMMITS
    for commit in commits:
        sha = commit["id"]

        # ✅ FIXED (3 VALUES)
        f, c, commit_details = get_commit_changes(repo_name, sha)

        files_changed += f
        total_changes += c

        # ✅ LINE ANALYSIS
        risky = detect_risky_lines(commit_details)
        all_risky.extend(risky)

    # =====================================================
    # FEATURES
    # =====================================================
    ratio = total_changes / max(files_changed, 1)

    large_change = 1 if total_changes > 200 else 0
    multi_file = 1 if files_changed > 3 else 0
    merge = 1

    # =====================================================
    # PREDICTION
    # =====================================================
    prob, level = predict_risk(
        files_changed,
        total_changes,
        ratio,
        large_change,
        multi_file,
        merge
    )

    # =====================================================
    # EXPLANATION
    # =====================================================
    reasons = explain_risk({
        "files_changed": files_changed,
        "total_changes": total_changes,
        "multi_file_change": multi_file,
        "merge_activity": merge
    })

    reason_text = "\n".join([f"- {r}" for r in reasons]) if reasons else "- No strong signals"

    # =====================================================
    # RISKY AREAS + RESOLUTION
    # =====================================================
    risk_area_text = ""
    resolution_text = ""

    for r in all_risky:

        file = r["file"]
        line = r["line"]
        old_code = r.get("old_code")
        new_code = r.get("new_code")

        risk_area_text += f"\n- {file} (Line {line}) → Code modified"

        # 🔥 SMART RESOLUTION
        if old_code and new_code:

            if old_code.replace(" ", "") == new_code.replace(" ", ""):
                fix = new_code
                reason = "Only formatting change → safe merge"

            elif len(new_code) > len(old_code):
                fix = new_code
                reason = "New logic more descriptive → prefer new"

            else:
                fix = old_code
                reason = "Old logic stable → keep original"

        else:
            fix = new_code or old_code
            reason = "Single side change"

        resolution_text += f"""
📂 File: {file}
📍 Line: {line}

🔴 Old Code:
{old_code}

🟢 New Code:
{new_code}

✅ Final Suggested Code:
{fix}

💡 Reason:
{reason}

---
"""

    if not risk_area_text:
        risk_area_text = "\n- No risky files detected"

    # =====================================================
    # AUTO RESOLVER TRIGGER
    # =====================================================
    trigger_auto = (
        level == "HIGH"
        or ratio > 120
        or total_changes > 400
    )

    auto_fix_message = ""

    if trigger_auto and resolution_text:
        auto_fix_message = f"""
---
### ⚡ AI Conflict Resolution (Exact Fixes)
{resolution_text}
"""

    # =====================================================
    # FINAL COMMENT
    # =====================================================
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

    # =====================================================
    # POST COMMENT
    # =====================================================
    for commit in commits:
        sha = commit["id"]
        post_commit_comment(repo_name, sha, message)

    return {
        "status": "success",
        "risk_level": level,
        "probability": float(prob)
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