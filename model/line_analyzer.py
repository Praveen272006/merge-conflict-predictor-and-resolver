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

        old_code = None

        for line in lines:

            if line.startswith("@@"):
                parts = line.split(" ")
                new_info = parts[2]
                line_number = int(new_info.split(",")[0][1:])
                continue

            if line.startswith("-") and not line.startswith("---"):
                old_code = line[1:].strip()

            elif line.startswith("+") and not line.startswith("+++"):

                new_code = line[1:].strip()

                risky.append({
                    "file": filename,
                    "line": line_number,
                    "old_code": old_code,
                    "new_code": new_code
                })

                old_code = None
                line_number += 1

            else:
                line_number += 1

    return risky