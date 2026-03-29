def detect_risky_lines(commit_details):

    risky = []

    files = commit_details.get("files", [])

    for file in files:

        filename = file.get("filename")
        patch = file.get("patch")

        if not patch:
            continue

        lines = patch.split("\n")
        line_number = 0

        old_code = ""
        new_code = ""

        for line in lines:

            if line.startswith("@@"):
                parts = line.split(" ")
                line_number = int(parts[2].split(",")[0][1:])
                continue

            if line.startswith("-") and not line.startswith("---"):
                old_code = line[1:]

            if line.startswith("+") and not line.startswith("+++"):
                new_code = line[1:]

                risky.append({
                    "file": filename,
                    "line": line_number,
                    "old_code": old_code,
                    "new_code": new_code
                })

            line_number += 1

    return risky