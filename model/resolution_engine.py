def generate_resolution(risky_lines):
    """
    Generate clean AI-based resolution suggestions
    """

    suggestions = []

    for r in risky_lines[:5]:  # limit output

        old_code = r.get("old_code", "").strip()
        new_code = r.get("new_code", "").strip()

        # Skip useless entries
        if not old_code and not new_code:
            continue

        # Smart decision
        if old_code and new_code:
            fix = new_code
            reason = "Updated logic detected"
        elif new_code:
            fix = new_code
            reason = "New code added"
        else:
            fix = old_code
            reason = "Code removal detected"

        suggestions.append({
            "file": r["file"],
            "line": r["line"],
            "old": old_code or "N/A",
            "new": new_code or "N/A",
            "fix": fix,
            "reason": reason
        })

    return suggestions