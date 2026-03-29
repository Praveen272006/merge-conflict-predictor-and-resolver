def detect_risky_lines(commit_details):

    risky = []
    files = commit_details.get("files", [])

    for file in files:

        filename = file.get("filename")
        patch = file.get("patch")

        if not patch:
            continue

        lines = patch.split("\n")
        line_no = 0

        for line in lines:

            if line.startswith("@@"):
                parts = line.split(" ")
                line_no = int(parts[2].split(",")[0][1:])
                continue

            if line.startswith("+") and not line.startswith("+++"):
                risky.append({
                    "file": filename,
                    "line": line_no
                })

            line_no += 1

    return risky