def generate_resolution(risky_lines):

    suggestions = []

    for r in risky_lines[:5]:

        old_code = r.get("old_code", "")
        new_code = r.get("new_code", "")

        if old_code and new_code:
            fix = new_code
            reason = "Updated logic"
        elif new_code:
            fix = new_code
            reason = "New code"
        else:
            fix = old_code
            reason = "Removed code"

        suggestions.append({
            "file": r["file"],
            "line": r["line"],
            "old": old_code or "N/A",
            "new": new_code or "N/A",
            "fix": fix,
            "reason": reason
        })

    return suggestions