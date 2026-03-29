import re
import difflib


# =========================
# TOKENIZER
# =========================
def tokenize(line):
    return re.findall(r'\w+', line)


# =========================
# VARIABLE MAPPING
# =========================
def detect_variable_mapping(a, b):
    tokens_a = tokenize(a)
    tokens_b = tokenize(b)

    mapping = {}
    for x, y in zip(tokens_a, tokens_b):
        if x != y:
            mapping[x] = y

    return mapping


# =========================
# APPLY MAPPING
# =========================
def apply_mapping(line, mapping):
    for k, v in mapping.items():
        line = re.sub(rf"\b{k}\b", v, line)
    return line


# =========================
# SMART MERGE (LINE)
# =========================
def smart_merge(line_a, line_b):

    a = line_a.strip()
    b = line_b.strip()

    if a == b:
        return a

    mapping = detect_variable_mapping(a, b)

    if len(b) >= len(a):
        return apply_mapping(b, mapping)
    else:
        return apply_mapping(a, mapping)


# =========================
# BLOCK MERGE
# =========================
def merge_blocks(old_block, new_block):

    merged_lines = []
    max_len = max(len(old_block), len(new_block))

    for i in range(max_len):

        old_line = old_block[i] if i < len(old_block) else ""
        new_line = new_block[i] if i < len(new_block) else ""

        if old_line and new_line:
            merged_lines.append(smart_merge(old_line, new_line))
        elif new_line:
            merged_lines.append(new_line)
        elif old_line:
            merged_lines.append(old_line)

    # REMOVE DUPLICATES
    final = []
    seen = set()

    for line in merged_lines:
        if line and line not in seen:
            seen.add(line)
            final.append(line)

    return "\n".join(final)


# =========================
# VISUAL DIFF
# =========================
def generate_diff(old_code, new_code):

    old_lines = old_code.split("\n")
    new_lines = new_code.split("\n")

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        lineterm=""
    )

    return "\n".join(diff)


# =========================
# MAIN ENGINE (ONE OUTPUT PER FILE)
# =========================
def generate_resolution(commit_data):

    resolutions = []
    files = commit_data.get("files", [])

    for file in files:

        filename = file.get("filename")
        patch = file.get("patch")

        if not patch:
            continue

        lines = patch.split("\n")

        old_all = []
        new_all = []

        line_start = None
        line_end = None

        for line in lines:

            if line.startswith("@@"):
                parts = line.split(" ")
                new_info = parts[2]
                start_line = int(new_info.split(",")[0].replace("+", ""))

                if line_start is None:
                    line_start = start_line

                line_end = start_line
                continue

            if line.startswith("-") and not line.startswith("---"):
                old_all.append(line[1:].strip())

            elif line.startswith("+") and not line.startswith("+++"):
                new_all.append(line[1:].strip())

            else:
                if line_end is not None:
                    line_end += 1

        if old_all or new_all:

            old_code = "\n".join(old_all) if old_all else "[no code]"
            new_code = "\n".join(new_all) if new_all else "[no code]"

            merged = merge_blocks(old_all, new_all)
            diff_text = generate_diff(old_code, new_code)

            resolutions.append({
                "file": filename,
                "line": f"{line_start}-{line_end}",
                "issue": "Conflicting logic",
                "old_code": old_code,
                "new_code": new_code,
                "fix": merged,
                "diff": diff_text,
                "explanation": "AI combined all changes and generated the best merged solution"
            })

    return resolutions