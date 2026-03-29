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

            # Extract correct line number
            if line.startswith("@@"):
                try:
                    parts = line.split(" ")
                    line_no = int(parts[2].split(",")[0][1:])
                except:
                    line_no = 0
                continue

            # Skip diff headers
            if line.startswith("+++") or line.startswith("---"):
                continue

            # =========================
            # 🔴 REMOVED CODE
            # =========================
            if line.startswith("-"):

                code = line[1:]

                if code.strip() == "":
                    issue = "Whitespace occurred"
                    code_display = "whitespace"
                    fix = "Remove unnecessary blank lines"
                    explanation = "Extra whitespace may cause formatting inconsistencies"
                else:
                    issue = "Old logic removed"
                    code_display = code
                    fix = "Verify that removed logic is not required elsewhere"
                    explanation = "Deleting code may break dependent functionality or features"

                results.append({
                    "file": filename,
                    "line": line_no,
                    "type": "REMOVED",
                    "code": code_display,
                    "issue": issue,
                    "fix": fix,
                    "explanation": explanation
                })

            # =========================
            # 🟢 ADDED CODE
            # =========================
            elif line.startswith("+"):

                code = line[1:]

                if code.strip() == "":
                    issue = "Whitespace occurred"
                    code_display = "whitespace"
                    fix = "Avoid adding unnecessary blank lines"
                    explanation = "Unnecessary whitespace can reduce readability and consistency"
                else:
                    issue = "New logic added"
                    code_display = code
                    fix = "Ensure compatibility with existing logic and test thoroughly"
                    explanation = "New code may introduce conflicts or unexpected behavior"

                results.append({
                    "file": filename,
                    "line": line_no,
                    "type": "ADDED",
                    "code": code_display,
                    "issue": issue,
                    "fix": fix,
                    "explanation": explanation
                })

            line_no += 1

    return results