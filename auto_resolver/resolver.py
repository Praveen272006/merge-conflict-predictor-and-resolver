# auto_resolver/resolver.py

def extract_conflicts(text):
    """
    Extracts conflict blocks and returns structured data.
    """

    lines = text.split("\n")
    conflicts = []

    i = 0
    while i < len(lines):
        if lines[i].startswith("<<<<<<<"):
            start_line = i + 1
            head_version = []
            incoming_version = []

            i += 1
            while i < len(lines) and not lines[i].startswith("======="):
                head_version.append(lines[i])
                i += 1

            i += 1  # skip =======

            while i < len(lines) and not lines[i].startswith(">>>>>>>"):
                incoming_version.append(lines[i])
                i += 1

            conflicts.append({
                "line": start_line,
                "head": "\n".join(head_version),
                "incoming": "\n".join(incoming_version)
            })

        i += 1

    return conflicts


def suggest_resolution(conflict):
    """
    Basic smart suggestion engine.
    """

    head = conflict["head"].strip()
    incoming = conflict["incoming"].strip()

    # Simple heuristic
    if head == incoming:
        return head, "Both versions identical. Safe to keep either."

    if len(incoming) > len(head):
        return incoming, "Incoming change has more logic. Consider using it."

    return head, "HEAD version simpler. Keep original logic."


def resolve_conflicts(text):
    """
    Main resolver.
    """

    conflicts = extract_conflicts(text)

    if not conflicts:
        return {
            "has_conflict": False,
            "solutions": []
        }

    solutions = []

    for conflict in conflicts:
        suggestion, reason = suggest_resolution(conflict)

        solutions.append({
            "line": conflict["line"],
            "head": conflict["head"],
            "incoming": conflict["incoming"],
            "suggested_fix": suggestion,
            "reason": reason
        })

    return {
        "has_conflict": True,
        "solutions": solutions
    }