# model/line_analyzer.py

def detect_risky_lines(commit_details):
    """
    commit_details must be the FULL GitHub commit API response
    (not webhook raw payload).

    Expected format:
    {
        "files": [
            {
                "filename": "code/one.py",
                "patch": "@@ -1,3 +1,4 @@\n- return x + y\n+ return x - y"
            }
        ]
    }

    Returns:
    [
        {
            "file": "code/one.py",
            "line": 2,
            "issue": "Logic modified",
            "code": "return x - y"
        }
    ]
    """

    risky = []

    files = commit_details.get("files", [])

    for file in files:

        filename = file.get("filename")
        patch = file.get("patch")

        if not patch:
            continue

        lines = patch.split("\n")
        current_line_number = 0

        for line in lines:

            # Detect hunk header
            if line.startswith("@@"):
                # Example: @@ -1,3 +1,4 @@
                parts = line.split(" ")
                new_info = parts[2]  # +start,count
                start_line = int(new_info.split(",")[0][1:])
                current_line_number = start_line
                continue

            # Detect modified line (removed)
            if line.startswith("-") and not line.startswith("---"):
                risky.append({
                    "file": filename,
                    "line": current_line_number,
                    "issue": "Old logic removed",
                    "code": line[1:].strip()
                })

            # Detect added line
            elif line.startswith("+") and not line.startswith("+++"):
                risky.append({
                    "file": filename,
                    "line": current_line_number,
                    "issue": "New logic added",
                    "code": line[1:].strip()
                })

                current_line_number += 1

            else:
                current_line_number += 1

    return risky