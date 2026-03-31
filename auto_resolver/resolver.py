# auto_resolver/resolver.py

import re
from difflib import SequenceMatcher


def extract_conflicts(text):
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

            i += 1

            while i < len(lines) and not lines[i].startswith(">>>>>>>"):
                incoming_version.append(lines[i])
                i += 1

            conflicts.append({
                "line": start_line,
                "head": "\n".join(head_version).strip(),
                "incoming": "\n".join(incoming_version).strip()
            })

        i += 1

    return conflicts


# =========================
# 🔥 SMART MERGE ENGINE
# =========================
def smart_merge(head, incoming):

    # If identical
    if head == incoming:
        return head, "Both branches are identical."

    # Split into lines
    head_lines = head.split("\n")
    incoming_lines = incoming.split("\n")

    merged_lines = []

    max_len = max(len(head_lines), len(incoming_lines))

    for i in range(max_len):

        h = head_lines[i] if i < len(head_lines) else ""
        inc = incoming_lines[i] if i < len(incoming_lines) else ""

        # If same → keep
        if h.strip() == inc.strip():
            merged_lines.append(h)
            continue

        # 🔥 VARIABLE AWARE MERGE
        tokens_h = re.findall(r'\w+', h)
        tokens_i = re.findall(r'\w+', inc)

        # Choose line with better semantic clarity (longer meaningful tokens)
        if len("".join(tokens_i)) > len("".join(tokens_h)):
            merged_lines.append(inc)
        else:
            merged_lines.append(h)

    merged_code = "\n".join(merged_lines)

    return merged_code, "Merged using semantic comparison of both branches."


# =========================
# 🔥 MAIN SUGGESTION ENGINE
# =========================
def suggest_resolution(conflict):

    head = conflict["head"]
    incoming = conflict["incoming"]

    merged, reason = smart_merge(head, incoming)

    return merged, reason


# =========================
# 🔥 MAIN RESOLVER
# =========================
def resolve_conflicts(text):

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