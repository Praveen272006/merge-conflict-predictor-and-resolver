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

            # 🔴 REMOVED
            if line.startswith("-"):
                code = line[1:]

                if code.strip() == "":
                    code = "[empty line]"

                results.append({
                    "file": filename,
                    "line": line_no,
                    "type": "REMOVED",
                    "code": code,
                    "issue": "Old logic removed",
                    "fix": "Ensure removed logic is not required",
                    "explanation": "Removing code may break existing functionality"
                })

            # 🟢 ADDED
            elif line.startswith("+"):
                code = line[1:]

                if code.strip() == "":
                    code = "[empty line]"

                results.append({
                    "file": filename,
                    "line": line_no,
                    "type": "ADDED",
                    "code": code,
                    "issue": "New logic added",
                    "fix": "Verify compatibility with existing code",
                    "explanation": "New code may introduce conflicts"
                })

            line_no += 1

    return results