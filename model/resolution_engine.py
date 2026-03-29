def smart_merge(line_a, line_b):
    """
    AI-based smart merge between two conflicting lines
    """

    a = line_a.strip()
    b = line_b.strip()

    # Same → return
    if a == b:
        return a

    # Prefer meaningful variable names
    keywords = ["quantity", "total", "amount", "price"]

    for k in keywords:
        if k in a and k not in b:
            return a
        if k in b and k not in a:
            return b

    # Replace abbreviations
    if "qty" in b:
        return b.replace("qty", "quantity")
    if "qty" in a:
        return a.replace("qty", "quantity")

    # Prefer longer line (more descriptive)
    return a if len(a) > len(b) else b


def generate_resolution(commit_data):
    """
    Generate clean AI-based conflict resolution
    """

    resolutions = []

    files = commit_data.get("files", [])

    for file in files:

        filename = file.get("filename")
        patch = file.get("patch")

        if not patch:
            continue

        lines = patch.split("\n")

        line_number = 0
        prev_removed = None

        for line in lines:

            # Detect hunk start
            if line.startswith("@@"):
                parts = line.split(" ")
                new_file_info = parts[2]  # +start,count
                line_number = int(new_file_info.split(",")[0].replace("+", ""))
                continue

            # -------------------------
            # REMOVED LINE
            # -------------------------
            if line.startswith("-") and not line.startswith("---"):
                removed_code = line[1:].strip()

                if removed_code == "":
                    removed_code = "whitespace"

                prev_removed = removed_code

            # -------------------------
            # ADDED LINE
            # -------------------------
            elif line.startswith("+") and not line.startswith("+++"):
                added_code = line[1:].strip()

                if added_code == "":
                    added_code = "whitespace"

                # 🔥 IF BOTH EXIST → CONFLICT → MERGE
                if prev_removed and prev_removed != "whitespace" and added_code != "whitespace":

                    merged_code = smart_merge(prev_removed, added_code)

                    resolutions.append({
                        "file": filename,
                        "line": line_number,
                        "type": "MERGED",
                        "issue": "Conflicting logic",
                        "code": merged_code,
                        "fix": f"Solution: {merged_code}",
                        "explanation": "AI compared both versions and selected the best, most meaningful code"
                    })

                else:
                    # Normal addition
                    resolutions.append({
                        "file": filename,
                        "line": line_number,
                        "type": "ADDED",
                        "issue": "New logic added",
                        "code": added_code,
                        "fix": "Verify compatibility",
                        "explanation": "New code introduced"
                    })

                prev_removed = None

            # -------------------------
            # NORMAL LINE
            # -------------------------
            else:
                line_number += 1
                prev_removed = None

    return resolutions