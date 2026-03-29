def generate_resolution(commit_details):

    results = []

    files = commit_details.get("files", [])

    for file in files:

        filename = file.get("filename")
        patch = file.get("patch")

        if not patch:
            continue

        lines = patch.split("\n")
        line_no = 0

        for line in lines:

            if line.startswith("@@"):
                parts = line.split(" ")
                line_no = int(parts[2].split(",")[0][1:])
                continue

            if line.startswith("+") and not line.startswith("+++"):

                code = line[1:].strip()

                issue = detect_issue(code)
                fix = suggest_fix(code, issue)
                explanation = explain_fix(issue)

                results.append({
                    "file": filename,
                    "line": line_no,
                    "issue": issue,
                    "code": code,
                    "fix": fix,
                    "explanation": explanation
                })

            line_no += 1

    return results[:5]


def detect_issue(code):

    if "print(" in code:
        return "Debug statement in code"

    if "==" in code:
        return "Possible comparison issue"

    if "for" in code:
        return "Loop logic modification"

    if "=" in code:
        return "Variable modification"

    return "General code change"


def suggest_fix(code, issue):

    if issue == "Debug statement in code":
        return "Remove print() in production"

    if issue == "Possible comparison issue":
        return "Check equality condition"

    if issue == "Loop logic modification":
        return "Verify loop logic"

    if issue == "Variable modification":
        return "Ensure consistency across branches"

    return "Review manually"


def explain_fix(issue):

    explanations = {
        "Debug statement in code":
            "Debug logs should not be in production",

        "Possible comparison issue":
            "Wrong comparisons may break logic",

        "Loop logic modification":
            "Loops may cause unexpected behavior",

        "Variable modification":
            "Variable changes may cause merge conflicts",

        "General code change":
            "Code updated, review needed"
    }

    return explanations.get(issue, "Review required")