def generate_resolution(risky_lines):

    suggestions = []

    for r in risky_lines[:5]:
        suggestions.append(
            f"• Review logic near line {r['line']} in {r['file']}"
        )

    return "\n".join(suggestions) if suggestions else "• No fixes needed"